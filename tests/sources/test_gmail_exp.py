from unittest import TestCase
from datetime import date, datetime
from mailbankdata.banks import bco_chile
from mailbankdata.sources import GMailExportBankApi


class TestGMailExportBankApi(TestCase):
    def test_generate_filters(self):
        st_date, end_date = date(1, 1, 1), date(1, 1, 2)
        filters = GMailExportBankApi.generate_filters(bco_chile.EMAIL, st_date, end_date)
        expected = {'from': bco_chile.EMAIL, 'after': st_date, 'before': end_date}
        self.assertEqual(filters, expected)

    def test_pass_filters(self):
        msg = {
            'from': 'enviodigital@bancochile.cl',
            'date': str(datetime(1, 1, 1, 2, 3, 4)),
        }
        st_date, end_date = date(1, 1, 1), date(1, 1, 2)
        filters = GMailExportBankApi.generate_filters(bco_chile.EMAIL, st_date, end_date)
        self.assertTrue(GMailExportBankApi.pass_filters(msg, filters))
