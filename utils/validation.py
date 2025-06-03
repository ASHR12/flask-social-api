"""
Input validation utilities for the Social Media REST API.
"""
def validate_registration(data):
    errors = []
    if not data.get('username') or len(data['username']) < 3:
        errors.append('Username must be at least 3 characters.')
    if not data.get('email') or '@' not in data['email']:
        errors.append('Valid email is required.')
    if not data.get('password') or len(data['password']) < 6:
        errors.append('Password must be at least 6 characters.')
    return errors

def validate_login(data):
    errors = []
    if not data.get('username'):
        errors.append('Username is required.')
    if not data.get('password'):
        errors.append('Password is required.')
    return errors
