class Account:

    def __init__(self, owner_id, account_id, account_category, account_amount, account_number):
        self._owner_id = owner_id
        self._account_id = account_id
        self._account_category = account_category
        self._account_amount = account_amount
        self._account_number = account_number

    def get_amount(self):
        return self._account_amount

    def set_amount(self, _account_amount):
        self._account_amount = _account_amount


