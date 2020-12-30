import os
import re
from unittest import TestCase
from bankdata.banks.bco_chile import MAIL_REGEX
from bankdata.core.constants import TransactionType as TransType


class TestRegex(TestCase):
    resource_folder = '../../resources/bco_chile/'

    def test_check_expense_regex(self):
        file_path = os.path.join(self.resource_folder, 'check_expense.html')
        with open(file_path, encoding='utf-8') as f:
            text = f.read()
        reg = MAIL_REGEX[TransType.CHECK_EXPENSE]
        result = re.search(reg, text, re.DOTALL)
        self.assertEqual(result.group('nat'), '1.450')

    def test_check_transfer(self):
        file_path = os.path.join(self.resource_folder, 'check_transfer.html')
        with open(file_path, encoding='utf-8') as f:
            text = f.read()
        reg = MAIL_REGEX[TransType.CHECK_TRANSFER]
        result = re.search(reg, text, re.DOTALL)
        self.assertEqual(result.group('nat'), '20.450')

    def test_check_withdraw(self):
        file_path = os.path.join(self.resource_folder, 'check_withdraw.html')
        with open(file_path, encoding='utf-8') as f:
            text = f.read()
        reg = MAIL_REGEX[TransType.CHECK_WITHDRAW]
        result = re.search(reg, text, re.DOTALL)
        self.assertEqual(result.group('nat'), '30.000')

    def test_int_cred_exp(self):
        file_path = os.path.join(self.resource_folder, 'int_cred_exp.html')
        with open(file_path, encoding='utf-8') as f:
            text = f.read()
        reg = MAIL_REGEX[TransType.INT_CRED_EXPENSE]
        result = re.search(reg, text, re.DOTALL)
        self.assertEqual(result.group('int'), '18,87')

    def test_int_cred_pay(self):
        file_path = os.path.join(self.resource_folder, 'int_cred_pay.html')
        with open(file_path, encoding='utf-8') as f:
            text = f.read()
        reg = MAIL_REGEX[TransType.INT_CRED_PAY]
        result = re.search(reg, text, re.DOTALL)
        self.assertEqual(result.group('rate'), '725,90')
        self.assertEqual(result.group('int'), '18,87')
        self.assertEqual(result.group('nat'), '13.698')

    def test_nat_cred_exp(self):
        file_path = os.path.join(self.resource_folder, 'nat_cred_exp.html')
        with open(file_path, encoding='utf-8') as f:
            text = f.read()
        reg = MAIL_REGEX[TransType.NAT_CRED_EXPENSE]
        result = re.search(reg, text, re.DOTALL)
        self.assertEqual(result.group('nat'), '11.000')

    def test_nat_cred_pay(self):
        file_path = os.path.join(self.resource_folder, 'nat_cred_pay.html')
        with open(file_path, encoding='utf-8') as f:
            text = f.read()
        reg = MAIL_REGEX[TransType.NAT_CRED_PAY]
        result = re.search(reg, text, re.DOTALL)
        self.assertEqual(result.group('nat'), '66.784')
