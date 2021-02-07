from datetime import date
from unittest import TestCase
from mailbankdata.banks import bco_chile, Bank
from mailbankdata.sources import GMailAttachmentBankApi


class TestGMailAttachmentBankApi(TestCase):
    def test_constructor(self):
        GMailAttachmentBankApi(None, Bank.BCO_CHILE, 123456)

    def test_constructor_exc(self):
        with self.assertRaises(Exception):
            GMailAttachmentBankApi(None, Bank.BCO_CHILE)

    def test_generate_filters(self):
        st_date, end_date = date(1, 1, 1), date(1, 1, 2)
        filters = GMailAttachmentBankApi.generate_filters(bco_chile.EMAIL, st_date, end_date)
        expected = {'from': bco_chile.EMAIL, 'after': st_date, 'before': end_date}
        self.assertEqual(filters, expected)

