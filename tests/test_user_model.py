import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
	def test_password_setter(self):
		u = User(password = 'dog')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u = User(password = 'dog')
		with self.assertRaise(AttributeError):
			u.password

	def test_password_verification(self):
		u = User(password = 'dog')
		self.assertTrue(u.verify_password('dog'))
		self.assertFalse(u.verify_password('cat'))

	def test_password_salts_are_random(self):
		u = User(password = 'dog')
		u2 = User(password = 'dog')
		self.assertTrue(u.password_hash != u2.password_hash)
		