import unittest
from unittest.mock import Mock
import src.service.client_service as client_service
import src.dao.client_dao as client_dao
import src.dao.account_dao as account_dao

class Client_Service_Tests(unittest.TestCase):
    # Test for get specific client method
    def setUp(self):
        account_dao.get_specific_accounts = Mock(return_value=[(5, 2, 'Checkings', 500.00, '1234567891011'),
                                                               (5, 1, 'Checkings', 700.00, '3333333333333'),
                                                               (5, 4, 'Savings', 4000.00, '111111111111')])
        client_dao.get_all_clients = Mock(return_value=[(4, 'John'), (5, 'Jen'), (1, 'Jimbo')])
        client_dao.get_specific_client = Mock(return_value=[(4, 'John')])

    def test_get_all_clients(self):
        self.assertIsInstance(client_service.get_all_clients(), dict)

    def test_get_specific_client(self):
        self.assertIsInstance(client_service.get_specific_client(4), dict)