from application import create_app
from application.models import db, Mechanic
import unittest


class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.mechanic = Mechanic(
                name="Test Mechanic",
                email="test@shop.com",
                salary=50000
            )

            db.session.add(self.mechanic)
            db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_mechanic(self):
        payload = {
            "name": "New Mechanic",
            "email": "new@shop.com",
            "salary": 60000
        }

        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)

    def test_top_mechanics(self):
        response = self.client.get('/mechanics/top')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()