import unittest
import json
from config import app, db
from models import Contact
import pytest

class TestContactBook(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        self.ctx = app.app_context()  # Manually create application context
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()  # Pop application context after tests

    def test_get_contacts(self):
        response = self.app.get('/contacts')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['contacts'], list)

    def test_create_contact(self):
        contact_data = {'firstName': 'John', 'lastName': 'Doe', 'email': 'john.doe@example.com'}
        response = self.app.post('/create_contact', json=contact_data)
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Contact created successfully', response.data)

    def test_update_contact(self):
        contact = Contact(first_name='John', last_name='Doe', email='john.doe@example.com')
        db.session.add(contact)
        db.session.commit()
        updated_data = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@example.com'}
        response = self.app.patch(f'/update_contact/{contact.id}', json=updated_data)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact updated successfully', response.data)

    def test_delete_contact(self):
        contact = Contact(first_name='John', last_name='Doe', email='john.doe@example.com')
        db.session.add(contact)
        db.session.commit()
        response = self.app.delete(f'/delete_contact/{contact.id}')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact deleted successfully', response.data)

if __name__ == '__main__':
    unittest.main()

