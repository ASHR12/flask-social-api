import unittest
from main import create_app
from models.models import db, User

class UserSearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Add test users
            user1 = User(username='alice', email='alice@example.com', bio='Bio 1', password_hash='dummy')
            user2 = User(username='bob', email='bob@example.com', bio='Bio 2', password_hash='dummy')
            user3 = User(username='charlie', email='charlie@sample.com', bio='Bio 3', password_hash='dummy')
            db.session.add_all([user1, user2, user3])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_search_by_username(self):
        response = self.client.get('/api/users/search?q=ali')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['username'], 'alice')

    def test_search_by_email(self):
        response = self.client.get('/api/users/search?q=sample')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['username'], 'charlie')

    def test_search_no_results(self):
        response = self.client.get('/api/users/search?q=notfound')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 0)

    def test_search_missing_query(self):
        response = self.client.get('/api/users/search')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
