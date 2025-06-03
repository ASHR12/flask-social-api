"""
Database initialization and seeding for the Social Media REST API.
"""
from flask_sqlalchemy import SQLAlchemy
from models.models import db, User, Post, Comment, Like, Follow
from werkzeug.security import generate_password_hash

def init_db(app, db):
    with app.app_context():
        db.create_all()
        if not User.query.first():
            seed_data()

def seed_data():
    # Create sample users
    u1 = User(username='alice', email='alice@example.com', password_hash=generate_password_hash('password1'), bio='Hi, I am Alice!', avatar_url='https://i.pravatar.cc/150?img=1')
    u2 = User(username='bob', email='bob@example.com', password_hash=generate_password_hash('password2'), bio='Bob here!', avatar_url='https://i.pravatar.cc/150?img=2')
    u3 = User(username='carol', email='carol@example.com', password_hash=generate_password_hash('password3'), bio='Carol in the house.', avatar_url='https://i.pravatar.cc/150?img=3')
    u4 = User(username='dave', email='dave@example.com', password_hash=generate_password_hash('password4'), bio='Dave is here.', avatar_url='https://i.pravatar.cc/150?img=4')
    db.session.add_all([u1, u2, u3, u4])
    db.session.commit()

    # Create sample posts
    p1 = Post(user_id=u1.id, title='Hello World', content='This is my first post!')
    p2 = Post(user_id=u2.id, title='Bob Post', content='Bob is posting something cool.')
    p3 = Post(user_id=u3.id, title='Carol Post', content='Carol shares her thoughts.')
    p4 = Post(user_id=u1.id, title='Another Post', content='Alice again!')
    p5 = Post(user_id=u4.id, title='Dave Post', content='Dave joins the party.')
    p6 = Post(user_id=u2.id, title='Bob Again', content='Bob with another post.')
    db.session.add_all([p1, p2, p3, p4, p5, p6])
    db.session.commit()

    # Sample follows
    db.session.add(Follow(follower_id=u1.id, followed_id=u2.id))
    db.session.add(Follow(follower_id=u1.id, followed_id=u3.id))
    db.session.add(Follow(follower_id=u2.id, followed_id=u1.id))
    db.session.add(Follow(follower_id=u3.id, followed_id=u4.id))
    db.session.commit()

    # Sample likes
    db.session.add(Like(user_id=u1.id, post_id=p2.id))
    db.session.add(Like(user_id=u2.id, post_id=p1.id))
    db.session.add(Like(user_id=u3.id, post_id=p1.id))
    db.session.add(Like(user_id=u4.id, post_id=p3.id))
    db.session.commit()

    # Sample comments
    db.session.add(Comment(user_id=u2.id, post_id=p1.id, content='Nice post!'))
    db.session.add(Comment(user_id=u3.id, post_id=p1.id, content='Welcome!'))
    db.session.add(Comment(user_id=u1.id, post_id=p2.id, content='Thanks Bob!'))
    db.session.commit()
