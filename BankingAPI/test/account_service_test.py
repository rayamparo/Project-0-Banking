import unittest
from unittest.mock import Mock
import src.service.account_service as account_service
import src.dao.account_dao as account_dao

class AccountServiceTest(unittest.TestCase):

    def setUp(self):
        self.mock_account_row = {'owner_id': 5, 'account_id': 2, 'account_type': 'Checkings', 'account_amount': 500.00, 'account_number': '1234567891011'}
        account_dao.get_specific_accounts = Mock(return_value=[(5, 2, 'Checkings', 500.00, '1234567891011'),
                                                                (5, 1, 'Checkings', 700.00, '3333333333333'),
                                                                (5, 4, 'Savings', 4000.00, '111111111111')])
        account_dao.get_one_account = Mock(return_value=[(5, 2, 'Checkings', 500.00, '1234567891011')])
        self.mock_client_id = 5
        self.mock_req_body_client = {'client_name': 'John'}

    # Test for Accounts transform method in account service layer
    def test_db_accounts_transform(self):
        # Ensuring if a dict goes in, a list comes out (This method is used within most of the account service methods
        self.assertIsInstance(account_service.db_accounts_transform(self.mock_account_row), list)

    def test_get_specific_accounts(self):
        self.assertIsInstance(account_service.get_specific_accounts(5), list)

    def test_get_one_account(self):
        self.assertIsInstance(account_service.get_one_account(5, 2), list)
        self.assertEqual(len(account_service.get_one_account(5, 2)), 1)
        self.assertEquals(account_service.get_one_account(5, 2)[0]._owner_id, 5)

