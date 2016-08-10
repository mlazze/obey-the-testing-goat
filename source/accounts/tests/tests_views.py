from unittest.mock import patch

from django.test import TestCase


class LoginViewTest(TestCase):
    @patch('accounts.views.authenticate')
    def tests_calls_authenticate_with_assertion_from_post(self, mock_authenticate):
        mock_authenticate.return_value = None

        self.client.post('/accounts/login', {'assertion': 'assert this'})

        mock_authenticate.assert_called_once_with(assertion='assert this')
