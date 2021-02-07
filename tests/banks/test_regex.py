import importlib
from unittest import TestCase
from mailbankdata.banks import Bank
import mailbankdata.core.constants as consts

TransType = consts.TransactionType


class TestRegex(TestCase):
    banks_modules = []
    trans_groups = {
        TransType.NAT_CRED_PAY: ['?P<nat>'],
        TransType.INT_CRED_PAY: ['?P<nat>', '?P<int>', '?P<rate>'],
        TransType.CHECK_TRANSFER: ['?P<nat>'],
        TransType.NAT_CRED_EXPENSE: ['?P<nat>'],
        TransType.INT_CRED_EXPENSE: ['?P<int>'],
        TransType.CHECK_EXPENSE: ['?P<nat>'],
        TransType.CHECK_WITHDRAW: ['?P<nat>'],
    }

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        pkg_base = 'mailbankdata.banks'
        for bank in Bank:
            bank_module = importlib.import_module(f'{pkg_base}.{bank.name.lower()}')
            cls.banks_modules.append(bank_module)

    def test_regex_groups(self):
        for bank_module in self.banks_modules:
            mail_regex = bank_module.MAIL_REGEX
            for trans_type in mail_regex:
                for group in self.trans_groups[trans_type]:
                    msg = f'{group} not in MAIL_REGEX[{trans_type}] in {bank_module}'
                    self.assertTrue(group in mail_regex[trans_type], msg)
        return


