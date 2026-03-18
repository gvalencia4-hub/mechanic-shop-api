from application import create_app
from application.models import db, Customer
import unittest


class TestCustomers(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.customer = Customer(
                name="Test Customer",
                email="test@email.com",
                phone="555-123-4567",
                password="test123"
            )

            db.session.add(self.customer)
            db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_customer(self):
        payload = {
            "name": "New Customer",
            "email": "new@email.com",
            "phone": "555-999-0000",
            "password": "newpass123"
        }

        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)

    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_customer(self):
        payload = {
            "name": "Bad Customer"
        }

        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()