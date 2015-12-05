from app import app
import unittest


class SiteRootControllerTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_returns_site_root_when_not_logged_in(self):
        # Arrange

        # Act
        ret = self.app.get("/")

        # Assert
        self.assertIsNotNone(ret, "Home controller returned None response.")
        self.assertEqual('200 OK', ret.status)
        self.assertIn(b'Login</a>', ret.data)

    def test_home_returns_site_root_when_logged_in(self):
        # Arrange
        with self.app.session_transaction() as session:
            session["user_id"] = 1

        # Act
        ret = self.app.get("/")

        # Assert
        self.assertIsNotNone(ret, "Home controller returned None response.")
        self.assertEqual('200 OK', ret.status)
        self.assertIn(b'Logout</a>', ret.data)
