from unittest import TestCase
from datetime import datetime
from mailbankdata import Transaction
from mailbankdata.core.balance import Balance
from mailbankdata import TransactionType as TType


class TestBalance(TestCase):
    def test_balance(self):
        balance = Balance(15000, 1000000, 1000)
        expected = f'(check: 15000, nat_cred: 1000000, int_cred: 1000)'
        self.assertEqual(str(balance), expected)

    def test_update(self):
        balance = Balance(15000, 1000000, 1000)
        transactions = []
        default_dtime = datetime(1, 1, 1)
        rate = 730
        transactions.append(Transaction(TType.CHECK_TRANSFER, default_dtime, 3000))
        transactions.append(Transaction(TType.INT_CRED_EXPENSE, default_dtime, None, 19.99))
        transactions.append(Transaction(TType.NAT_CRED_EXPENSE, default_dtime, 9500))
        transactions.append(Transaction(TType.NAT_CRED_PAY, default_dtime, 5000))
        transactions.append(Transaction(TType.INT_CRED_PAY, default_dtime, 5*rate, 5, rate))
        balance.update(transactions)
        self.assertEqual(balance.check, 3350)
        self.assertEqual(balance.nat_cred, 995500)
        self.assertEqual(balance.int_cred, 985.01)
