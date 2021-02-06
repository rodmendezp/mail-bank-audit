from tests.test_case import BankRegexTestCase


class TestBcoEstadoRegex(BankRegexTestCase):
    bank_name = 'bco_estado'
    mail_reg_results = {
        'check_expense': {'nat': '58.950'},
        'check_transfer': {'nat': '160.000'},
        'check_withdraw': {'nat': '10.000'}
    }


TestBcoEstadoRegex.add_tests()
