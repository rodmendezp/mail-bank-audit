import re
import html
import base64
import pickle
import importlib
from datetime import date
from dateutil import parser
from typing import List, Optional
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

    def get_messages(self, filters):
        result = self._api.users().messages().list(userId='me', q=filters).execute()
        if result['resultSizeEstimate'] == 0:
            return []
        return result['messages']

    def get_message_info(self, msg):
        msg_info = self._api.users().messages().get(userId='me', id=msg['id']).execute()
        result = {}
        for x in msg_info['payload']['headers']:
            if x['name'] == 'Subject' or x['name'] == 'Date':
                result[x['name']] = x['value']
        if msg_info['payload']['body']['size'] > 0:
            body = base64.urlsafe_b64decode(msg_info['payload']['body']['data']).decode()
        else:
            body = base64.urlsafe_b64decode(msg_info['payload']['parts'][0]['body']['data']).decode()
        result['Body'] = html.unescape(body)
        result['Date'] = parser.parse(result['Date']).replace(tzinfo=None)
        return result

    def subj_possible_types(self, subj: str, trans_types: List[TransType]) -> List[TransType]:
        possible_types = []
        for ttype in trans_types:
            if re.search(self._bc.MAIL_SUBJ.get(ttype, '(?!x)x'), subj):
                possible_types.append(ttype)
        return possible_types

    def msg_to_transaction(self, msg_info, possible_types: List[TransType]) -> Optional[Transaction]:
        for ttype in possible_types:
            mail_reg = self._bc.MAIL_REGEX[ttype]
            match = re.search(mail_reg, msg_info['Body'], re.DOTALL)
            if not match:
                continue
            return Transaction.from_match(match, msg_info['Date'], ttype)
        # It may happen when subjects are the same for different ttype
        return None

    def _get_transactions(self, filters, trans_types: List[TransType]) -> List[Transaction]:
        transactions = []
        for msg in self.get_messages(filters):
            msg_info = self.get_message_info(msg)
            possible_types = self.subj_possible_types(msg_info['Subject'], trans_types)
            if not possible_types:
                continue
            transaction = self.msg_to_transaction(msg_info, possible_types)
            if transaction:
                transactions.append(transaction)
        return transactions

    def all_transactions(self, st_date: date = None, end_date: date = None) -> List[Transaction]:
        trans_types = list(TransType)
        filters = self.generate_filters(self._bc.EMAIL, st_date, end_date)
        return self._get_transactions(filters, trans_types)

    def check_transactions(self, st_date: date = None, end_date: date = None) -> List[Transaction]:
        trans_types = [
            TransType.NAT_CRED_PAY,
            TransType.INT_CRED_PAY,
            TransType.CHECK_TRANSFER,
            TransType.CHECK_EXPENSE,
            TransType.CHECK_WITHDRAW,
        ]
        filters = self.generate_filters(self._bc.EMAIL, st_date, end_date)
        return self._get_transactions(filters, trans_types)

    def credit_transactions(self, st_date: date = None, end_date: date = None) -> List[Transaction]:
        trans_types = [
            TransType.NAT_CRED_PAY,
            TransType.NAT_CRED_EXPENSE,
            TransType.NAT_CRED_WITHDRAW
        ]
        filters = self.generate_filters(self._bc.EMAIL, st_date, end_date)
        return self._get_transactions(filters, trans_types)

    def int_credit_transactions(self, st_date: date = None, end_date: date = None) -> List[Transaction]:
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
