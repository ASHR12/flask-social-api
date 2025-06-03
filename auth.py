"""
Authentication logic for the Social Media REST API.
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.models import db, User
from sqlalchemy.exc import IntegrityError
from utils.validation import validate_registration, validate_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = validate_registration(data)
    if errors:
        return jsonify({'errors': errors}), 400
    try:
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            bio=data.get('bio', ''),
            avatar_url=data.get('avatar_url', '')
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully.'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Username or email already exists.'}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = validate_login(data)
    if errors:
        return jsonify({'errors': errors}), 400
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bio': user.bio,
                'avatar_url': user.avatar_url
            }
        }), 200
    return jsonify({'error': 'Invalid username or password.'}), 401
