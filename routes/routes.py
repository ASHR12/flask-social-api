"""
API endpoints for the Social Media REST API.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, User, Post, Comment, Like, Follow
from sqlalchemy.exc import IntegrityError
from datetime import datetime

routes_bp = Blueprint('routes', __name__)

# --- User Profile Endpoints ---
@routes_bp.route('/users/search', methods=['GET'])
def search_users():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Query parameter "q" is required.'}), 400
    users = User.query.filter(
        (User.username.ilike(f"%{query}%")) |
        (User.email.ilike(f"%{query}%"))
    ).all()
    return jsonify([
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'avatar_url': user.avatar_url
        } for user in users
    ])

@routes_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'bio': user.bio,
        'avatar_url': user.avatar_url,
        'followers': user.followers.count(),
        'following': user.following.count(),
        'posts': user.posts.count()
    })

@routes_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_profile(user_id):
    current_user_id = get_jwt_identity()
    if user_id != current_user_id:
        return jsonify({'error': 'Unauthorized.'}), 403
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.bio = data.get('bio', user.bio)
    user.avatar_url = data.get('avatar_url', user.avatar_url)
    db.session.commit()
    return jsonify({'message': 'Profile updated.'})

# --- Post Endpoints ---
@routes_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    if not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content required.'}), 400
    post = Post(
        user_id=get_jwt_identity(),
        title=data['title'],
        content=data['content']
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created.', 'post_id': post.id}), 201

@routes_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'author': post.author.username,
        'title': post.title,
        'content': post.content,
        'timestamp': post.timestamp.isoformat(),
        'likes': post.likes.count(),
        'comments': post.comments.count()
    })

@routes_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized.'}), 403
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify({'message': 'Post updated.'})

@routes_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized.'}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted.'})

# --- Like/Unlike Endpoints ---
@routes_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()
    if Like.query.filter_by(user_id=user_id, post_id=post_id).first():
        return jsonify({'error': 'Already liked.'}), 400
    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Post liked.'})

@routes_bp.route('/posts/<int:post_id>/unlike', methods=['POST'])
@jwt_required()
def unlike_post(post_id):
    user_id = get_jwt_identity()
    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if not like:
        return jsonify({'error': 'Not liked yet.'}), 400
    db.session.delete(like)
    db.session.commit()
    return jsonify({'message': 'Post unliked.'})

# --- Comment Endpoints ---
@routes_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    data = request.get_json()
    if not data.get('content'):
        return jsonify({'error': 'Content required.'}), 400
    comment = Comment(
        user_id=get_jwt_identity(),
        post_id=post_id,
        content=data['content']
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added.', 'comment_id': comment.id}), 201

@routes_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.asc()).all()
    return jsonify([
        {
            'id': c.id,
            'author': c.author.username,
            'content': c.content,
            'timestamp': c.timestamp.isoformat()
        } for c in comments
    ])

# --- Follow/Unfollow Endpoints ---
@routes_bp.route('/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    if user_id == current_user_id:
        return jsonify({'error': 'Cannot follow yourself.'}), 400
    if Follow.query.filter_by(follower_id=current_user_id, followed_id=user_id).first():
        return jsonify({'error': 'Already following.'}), 400
    db.session.add(Follow(follower_id=current_user_id, followed_id=user_id))
    db.session.commit()
    return jsonify({'message': 'Now following user.'})

@routes_bp.route('/users/<int:user_id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()
    follow = Follow.query.filter_by(follower_id=current_user_id, followed_id=user_id).first()
    if not follow:
        return jsonify({'error': 'Not following.'}), 400
    db.session.delete(follow)
    db.session.commit()
    return jsonify({'message': 'Unfollowed user.'})

# --- Feed Endpoint ---
@routes_bp.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    followed_ids = [f.followed_id for f in user.following]
    posts = Post.query.filter(Post.user_id.in_(followed_ids)).order_by(Post.timestamp.desc()).limit(20).all()
    return jsonify([
        {
            'id': p.id,
            'author': p.author.username,
            'title': p.title,
            'content': p.content,
            'timestamp': p.timestamp.isoformat(),
            'likes': p.likes.count(),
            'comments': p.comments.count()
        } for p in posts
    ])

# --- Register all routes ---
def register_routes(app, db, jwt):
    from auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(routes_bp, url_prefix='/api')
