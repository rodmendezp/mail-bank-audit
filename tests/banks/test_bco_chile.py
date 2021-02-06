from tests.test_case import BankRegexTestCase


class TestBcoChileRegex(BankRegexTestCase):
    bank_name = 'bco_chile'
    mail_reg_results = {
        'check_expense': {'nat': '1.450'},
        'check_transfer': {'nat': '20.450'},
        'check_withdraw': {'nat': '30.000'},
        'int_cred_expense': {'int': '18,87'},
        'int_cred_pay': {
            'rate': '725,90',
            'int': '18,87',
            'nat': '13.698'
        },
        'nat_cred_expense': {'nat': '11.000'},
        'nat_cred_pay': {'nat': '66.784'}
    }


TestBcoChileRegex.add_tests()
