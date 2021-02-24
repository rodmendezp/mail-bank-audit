import re
import html
import base64
from datetime import date
from dateutil import parser
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

    def get_messages(self, filters):
        msg_attachment = self._api.users().messages().get(userId='me', id=self._msg_id).execute()
        for part in msg_attachment['payload']['parts']:
            if not part.get('filename'):
                continue
            if 'data' in part['body']:
                data = part['body']['data']
            else:
                attachment_id = part['body']['attachmentId']
                attachment = self._api.users().messages().attachments().get(userId='me', messageId=self._msg_id, id=attachment_id).execute()
                data = attachment['data']
            file_data = base64.urlsafe_b64decode(data)
            text = html.unescape(file_data.decode())
            mail_dtime = re.search(r'Date\: ([^\n]*)', text).group(1)
            mail_dtime = parser.parse(mail_dtime).replace(tzinfo=None)
            after, before = filters.get('after', date.min), filters.get('before', date.max)
            if not after <= mail_dtime.date() < before:
                continue
            yield {'Subject': part['filename'], 'Date': mail_dtime, 'Body': text}
        return

    def get_message_info(self, msg):
        return msg

    @staticmethod
    def generate_filters(from_: str, st_date: date, end_date: date) -> Dict[str, Any]:
        filters = {'from': from_}
        if st_date:
            filters['after'] = st_date
        if end_date:
            filters['before'] = end_date
        return filters
