import re
import html
import base64
from datetime import date
from mailbankdata.banks import Bank
from typing import List, Dict, Any
from mailbankdata.core import Transaction
from mailbankdata.sources.gmail import GMailBankApi
from mailbankdata.core.constants import TransactionType as TransType


class GMailAttachmentBankApi(GMailBankApi):
    def __init__(self, api, bank: Bank, msg_id=None, msg_subj=None) -> None:
        if not msg_id and not msg_subj:
            raise Exception('msg_id or msg_subj must be filled')
        super().__init__(api, bank)
        self._msg_id = msg_id or self._get_message_id(msg_subj)

    def _get_message_id(self, msg_subj: str) -> str:
        gmail_filter = f'subject: {msg_subj}'
        result = self._api.users().messages().list(userId='me', q=gmail_filter).execute()
        if result['resultSizeEstimate'] == 0:
            raise Exception(f'Did not find message with subject {msg_subj}')
        if result['resultSizeEstimate'] > 1:
            msg_count = result['resultSizeEstimate']
            raise Exception(f'Subject {msg_subj} needs to be unique, {msg_count} mails match this subject')
        return result['messages'][0]['id']

    @classmethod
    def from_creds_json(cls, creds_path: str, bank: Bank) -> 'GMailAttachmentBankApi':
        gmail_api = super().api_from_creds_json(creds_path)
        gmail_bank_api = cls.__new__(cls)
        gmail_bank_api.__init__(gmail_api, bank)
        return gmail_bank_api

    @classmethod
    def from_token_pickle(cls, token_path: str, bank: Bank) -> 'GMailAttachmentBankApi':
        gmail_api = super().api_from_token_pickle(token_path)
        gmail_bank_api = cls.__new__(cls)
        gmail_bank_api.__init__(gmail_api, bank)
        return gmail_bank_api

    def _get_transactions(self, filters, trans_types: List[TransType]) -> List[Transaction]:
        transactions = []
        msg_info = self._api.users().messages().get(userId='me', id=self._msg_id).execute()
        for part in msg_info['payload']['parts']:
            if not part.get('filename', None):
                continue
            msg_subj, possible_types = part['filename'], []
            for trans_type in trans_types:
                if re.search(self._bc.MAIL_SUBJ.get(trans_type, '(?!x)x'), msg_subj):
                    # Some subjects are very similar
                    possible_types.append(trans_type)
            if not possible_types:
                # Subject does not match to any of transactions subjects
                continue
            if 'data' in part['body']:
                data = part['body']['data']
            else:
                attachment_id = part['body']['attachmentId']
                attachment = self._api.users().messages().attachments().get(userId='me', messageId=self._msg_id, id=attachment_id).execute()
                data = attachment['data']
            file_data = base64.urlsafe_b64decode(data)
            # TODO: Get message body
            text = html.unescape(file_data.decode())
            for trans_type in possible_types:
                mail_reg = self._bc.MAIL_REGEX[trans_type]
                match = re.search(mail_reg, text, re.DOTALL)
                if not match:
                    continue
                t = Transaction.from_match(match, trans_type)
                transactions.append(t)
                break
        return transactions

    @staticmethod
    def generate_filters(from_: str, st_date: date, end_date: date) -> Dict[str, Any]:
        filters = {'from': from_}
        if st_date:
            filters['after'] = st_date
        if end_date:
            filters['before'] = end_date
        return filters
