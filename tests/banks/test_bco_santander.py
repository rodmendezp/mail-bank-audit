from tests.test_case import BankRegexTestCase


class TestBcoSantanderRegex(BankRegexTestCase):
    bank_name = 'bco_santander'
    mail_reg_results = {
        'check_transfer': {'nat': '123.456'}
    }


TestBcoSantanderRegex.add_tests()
