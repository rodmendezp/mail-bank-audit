import json
from datetime import datetime
from unittest import TestCase
from mailbankdata import Transaction, TransactionType
from mailbankdata.core.json import TransactionEncoder


class TestTransactionJsonEncoder(TestCase):
    def test_encoder(self):
        ttype = TransactionType.CHECK_EXPENSE
        transaction = Transaction(ttype, datetime(1, 1, 1), 195)
        json_dict = {'transaction': transaction}
        json_str = json.dumps(json_dict, cls=TransactionEncoder)
        expected = '{"transaction": {"amount": 195, "ttype": "CHECK_EXPENSE", "mail_dtime": "0001-01-01T00:00:00"}}'
        self.assertEqual(json_str, expected)
