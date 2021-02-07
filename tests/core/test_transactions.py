import os
import re
from unittest import TestCase
from datetime import datetime
from mailbankdata import Transaction, TransactionType
from mailbankdata.banks.bco_chile import MAIL_REGEX


class TestTransaction(TestCase):
    def test_exception(self):
        ttype = TransactionType.CHECK_TRANSFER
        with self.assertRaises(AttributeError):
            Transaction(ttype, datetime(1, 1, 1))

    def test_repr(self):
        ttype = TransactionType.CHECK_TRANSFER
        dtime, amount, rate = datetime(1, 1, 1), 195, 735
        transaction = Transaction(ttype, dtime, amount)
        self.assertEqual(transaction.__repr__(), f'({dtime}, {ttype.name}, {amount})')
        usd_trans = Transaction(ttype, dtime, int_amount=amount)
        self.assertEqual(usd_trans.__repr__(), f'({dtime}, {ttype.name}, USD {amount})')
        rate_trans = Transaction(ttype, dtime, amount, amount // rate, rate)
        expected = f'({dtime}, {ttype.name}, {amount}, USD {amount // rate} ({rate}))'
        self.assertEqual(rate_trans.__repr__(), expected)

    def test_from_match(self):
        ttype = TransactionType.INT_CRED_PAY
        regex = MAIL_REGEX[ttype]
        cd = os.path.dirname(__file__)
        html_path = os.path.join(cd, '..', '..', 'resources', 'bco_chile', 'int_cred_pay.html')
        with open(html_path) as f:
            text = f.read()
        result = re.search(regex, text, re.DOTALL)
        dtime = datetime(1, 1, 1)
        transaction = Transaction.from_match(result, dtime, ttype)
        self.assertEqual(transaction.amount, 13698)
        self.assertEqual(transaction.int_amount, 18.87)
        self.assertEqual(transaction.rate, 725.90)
