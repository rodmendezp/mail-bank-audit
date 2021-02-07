from datetime import date
from unittest import TestCase
from unittest.mock import patch
from mailbankdata.banks import Bank
from mailbankdata.banks import bco_chile
from mailbankdata.sources import GMailBankApi
from mailbankdata import TransactionType as TransType

CLS_PATH = 'mailbankdata.sources.gmail.GMailBankApi'


class TestGMailBankApi(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_api = None
        cls.str_filter = 'from:bancochile.cl after:0001-01-01 before:0001-01-02'

    def test_constructor(self):
        gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
        self.assertEqual(gmail_bank_api._api, self.mock_api)
        self.assertEqual(gmail_bank_api._bank, Bank.BCO_CHILE)
        self.assertEqual(gmail_bank_api._bc, bco_chile)

    def test_all_transactions(self):
        with patch.object(GMailBankApi, '_get_transactions') as mock:
            gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
            st_date, end_date = date(1, 1, 1), date(1, 1, 2)
            gmail_bank_api.all_transactions(st_date, end_date)
            mock.assert_called_with(self.str_filter, list(TransType))

    def test_check_transactions(self):
        check_trans_types = []
        for ttype in TransType:
            if ttype != TransType.INT_CRED_EXPENSE \
               and ttype != TransType.NAT_CRED_EXPENSE \
               and ttype != TransType.NAT_CRED_WITHDRAW:
                check_trans_types.append(ttype)
        with patch.object(GMailBankApi, '_get_transactions') as mock:
            gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
            st_date, end_date = date(1, 1, 1), date(1, 1, 2)
            gmail_bank_api.check_transactions(st_date, end_date)
            mock.assert_called_with(self.str_filter, check_trans_types)

    def test_credit_transactions(self):
        credit_transactions = [TransType.NAT_CRED_PAY, TransType.NAT_CRED_EXPENSE, TransType.NAT_CRED_WITHDRAW]
        with patch.object(GMailBankApi, '_get_transactions') as mock:
            gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
            st_date, end_date = date(1, 1, 1), date(1, 1, 2)
            gmail_bank_api.credit_transactions(st_date, end_date)
            mock.assert_called_with(self.str_filter, credit_transactions)

    def test_int_credit_transactions(self):
        int_cred_transactions = [TransType.INT_CRED_PAY, TransType.INT_CRED_EXPENSE]
        with patch.object(GMailBankApi, '_get_transactions') as mock:
            gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
            st_date, end_date = date(1, 1, 1), date(1, 1, 2)
            gmail_bank_api.int_credit_transactions(st_date, end_date)
            mock.assert_called_with(self.str_filter, int_cred_transactions)

    def test_generate_filters(self):
        st_date, end_date = date(1, 1, 1), date(1, 1, 2)
        filters = GMailBankApi.generate_filters(bco_chile.EMAIL, st_date, end_date)
        expected = self.str_filter
        self.assertEqual(filters, expected)
