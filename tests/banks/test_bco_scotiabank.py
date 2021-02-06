from tests.test_case import BankRegexTestCase


class TestBcoScotiabank(BankRegexTestCase):
    bank_name = 'bco_scotiabank'
    mail_reg_results = {
        'check_expense': {'nat': '2.400'}
    }


TestBcoScotiabank.add_tests()
