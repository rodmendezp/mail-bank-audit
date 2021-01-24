import re
import base64
import pickle
import importlib
from typing import List
from datetime import date
from mailbankdata.banks import Bank
from mailbankdata.core import Transaction
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from mailbankdata.core.constants import TransactionType as TransType

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GMailApi:
    def __init__(self, api) -> None:
        self._api = api

    @classmethod
    def api_from_creds_json(cls, creds_path: str):
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
        creds = flow.run_local_server(port=0)
        return build('gmail', 'v1', credentials=creds)

    @classmethod
    def api_from_token_pickle(cls, token_path: str):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return build('gmail', 'v1', credentials=creds)


class GMailBankApi(GMailApi):
    def __init__(self, api, bank: Bank) -> None:
        super().__init__(api)
        self._bank = bank
        self._bc = importlib.import_module(f'mailbankdata.banks.{bank.name.lower()}')

    @classmethod
    def from_creds_json(cls, creds_path: str, bank: Bank) -> 'GMailBankApi':
        gmail_api = super().api_from_creds_json(creds_path)
        gmail_bank_api = cls.__new__(cls)
        gmail_bank_api.__init__(gmail_api, bank)
        return gmail_bank_api

    @classmethod
    def from_token_pickle(cls, token_path: str, bank: Bank) -> 'GMailBankApi':
        gmail_api = super().api_from_token_pickle(token_path)
        gmail_bank_api = cls.__new__(cls)
        gmail_bank_api.__init__(gmail_api, bank)
        return gmail_bank_api

    def _get_transactions(self, gmail_filter: str, trans_types: List[TransType]) -> List[Transaction]:
        transactions = []
        result = self._api.users().messages().list(userId='me', q=gmail_filter).execute()
        if result['resultSizeEstimate'] == 0:
            return transactions
        messages = result['messages']
        for msg in messages:
            msg_info = self._api.users().messages().get(userId='me', id=msg['id']).execute()
            msg_subj = next(x['value'] for x in msg_info['payload']['headers'] if x['name'] == 'Subject')
            possible_types = []
            for trans_type in trans_types:
                if re.search(self._bc.MAIL_SUBJ.get(trans_type, '(?!x)x'), msg_subj):
                    # Some subjects are very similar
                    possible_types.append(trans_type)
            if not possible_types:
                # Subject does not match to any of transactions subjects
                continue
            if msg_info['payload']['body']['size'] > 0:
                text = base64.urlsafe_b64decode(msg_info['payload']['body']['data']).decode()
            else:
                text = msg_info['snippet']
            for trans_type in possible_types:
                mail_reg = self._bc.MAIL_REGEX[trans_type]
                match = re.search(mail_reg, text, re.DOTALL)
                if match:
                    t = Transaction.from_match(match, trans_type)
                    transactions.append(t)
                    break
        return transactions

    def check_transactions(self, st_date: date=None, end_date: date=None) -> List[Transaction]:
        trans_types = [
            TransType.NAT_CRED_PAY,
            TransType.INT_CRED_PAY,
            TransType.CHECK_TRANSFER,
            TransType.CHECK_EXPENSE,
            TransType.CHECK_WITHDRAW,
        ]
        filters = self.generate_filters(self._bc.EMAIL, st_date, end_date)
        return self._get_transactions(filters, trans_types)

    def credit_transactions(self, st_date: date=None, end_date: date=None) -> List[Transaction]:
        trans_types = [
            TransType.NAT_CRED_PAY,
            TransType.NAT_CRED_EXPENSE
        ]
        filters = self.generate_filters(self._bc.EMAIL, st_date, end_date)
        return self._get_transactions(filters, trans_types)

    def int_credit_transactions(self, st_date: date=None, end_date: date=None) -> List[Transaction]:
        trans_types = [
            TransType.INT_CRED_PAY,
            TransType.INT_CRED_EXPENSE
        ]
        filters = self.generate_filters(self._bc.EMAIL, st_date, end_date)
        return self._get_transactions(filters, trans_types)

    @staticmethod
    def generate_filters(from_: str, st_date: date, end_date: date) -> str:
        filters = {
            'from': from_,
        }
        if st_date:
            filters['after'] = str(st_date)
        if end_date:
            filters['before'] = str(end_date)
        filters = ' '.join(map(lambda x: f'{x[0]}:{x[1]}', filters.items()))
        return filters
