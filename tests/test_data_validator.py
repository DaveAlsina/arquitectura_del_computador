import unittest
from data_validator import DataValidator

class TestDataValidator:
    def setup(self):
        self.validator = DataValidator()

    def test_valid_usernames(self):
        usernames = ['username', 'user.name', 'user_name', 'user-name', 'username1', 'username!', 'username']
        for username in usernames:
            with self.subTest(username=username):
                self.assertTrue(self.validator.validate_username(username))

    def test_invalid_usernames(self):
        invalid_usernames = ['user with spaces', 'a', 'userñame']
        for username in invalid_usernames:
            with self.subTest(username=username):
                self.assertFalse(self.validator.validate_username(username))

    def test_valid_passwords(self):
        passwords = ['password', 'password1', 'password with spaces', 'password!']
        for password in passwords:
            with self.subTest(password=password):
                self.assertTrue(self.validator.validate_password(password))

    def test_invalid_passwords(self):
        invalid_passwords = ['pass', 'passwordñ']
        for password in invalid_passwords:
            with self.subTest(password=password):
                self.assertFalse(self.validator.validate_password(password))

    def test_valid_emails(self):
        emails = ['email@example.com', 'user.name@example.co', 'user123@example.net']
        for email in emails:
            with self.subTest(email=email):
                self.assertTrue(self.validator.validate_email(email))

    def test_invalid_emails(self):
        invalid_emails = ['email', 'email@example', 'email@example.123', 'email@example.c']
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(self.validator.validate_email(email))

if __name__ == '__main__':
    unittest.main()
    