import os
import re
import importlib
from unittest import TestCase
from typing import List, Tuple, Callable
from mailbankdata import TransactionType as TransType

BANK_BASE = 'mailbankdata.banks'


class BankRegexTestCase(TestCase):
    bank_name = None
    mail_reg_results = {}
    _resource_folder = None
    _trans_files = None
    _mail_regex = None

    @staticmethod
    def make_test_function(ttype: TransType, ttype_file: str) -> Callable:
        ttype_name = ttype.name.lower()

        def test(self):
            print(f'[{self.bank_name}] test_{ttype_name}_regex')
            with open(ttype_file, encoding='utf-8') as f:
                text = f.read()
            reg = self._mail_regex[ttype]
            result = re.search(reg, text, re.DOTALL)
            for k, v in self.mail_reg_results[ttype_name].items():
                self.assertEqual(result.group(k), v)

        return test

    @classmethod
    def add_tests(cls) -> None:
        if cls.bank_name is None:
            raise Exception('You need to set bank_name')

        cd = os.path.dirname(__file__)
        bank_module = importlib.import_module(f'{BANK_BASE}.{cls.bank_name}')
        cls._resource_folder = os.path.abspath(os.path.join(cd, '..', 'resources'))
        cls._trans_files = cls._get_transactions_files()
        cls._mail_regex = getattr(bank_module, 'MAIL_REGEX')
        for ttype, ttype_file in cls._trans_files:
            test_func = cls.make_test_function(ttype, ttype_file)
            ttype_name = ttype.name.lower()
            test_name = f'test_{ttype_name}_regex'

            setattr(cls, test_name, test_func)
        return

    @classmethod
    def _get_transactions_files(cls) -> List[Tuple[TransType, str]]:
        result = []
        for ttype in TransType:
            ttype_name = str(ttype.name).lower()
            file_name = f'{ttype_name}.html'
            html_path = os.path.join(cls._resource_folder, cls.bank_name, file_name)
            if os.path.exists(html_path):
                result.append((ttype, html_path))
        return result
