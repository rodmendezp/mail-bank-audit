import re
import email
import zipfile
import mailbox
import importlib
from datetime import date
from dateutil import parser
from typing import List, Dict, Any
from mailbankdata.banks import Bank
from mailbankdata.sources import GMailBankApi


class GMailExportBankApi(GMailBankApi):
    def __init__(self, zip_file: str, bank: Bank) -> None:
        self._bank = bank
        self._zip_file = zip_file
        self._bc = importlib.import_module(f'mailbankdata.banks.{bank.name.lower()}')
        self._extract_mbox()

    def _extract_mbox(self):
        zip_obj = zipfile.ZipFile(self._zip_file, 'r')
        mbox_zip_file_path = next(x for x in zip_obj.namelist() if x.endswith('.mbox'))
        self.mbox_file = zip_obj.extract(mbox_zip_file_path)

    def get_messages(self, filters):
        return filter(lambda x: self.pass_filters(x, filters), mailbox.mbox(self.mbox_file))

    def get_message_info(self, msg):
        mail_dtime = next(parser.parse(x[1]).replace(tzinfo=None) for x in msg._headers if x[0] == 'Date')
        subject = email.header.decode_header(msg['subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        if msg.is_multipart():
            body = ''.join(part.get_payload(decode=True).decode() for part in msg.get_payload())
        else:
            body = msg.get_payload(decode=True).decode()
        return {'Date': mail_dtime, 'Subject': subject, 'Body': body}

    @staticmethod
    def generate_filters(from_: str, st_date: date, end_date: date) -> Dict[str, Any]:
        filters = {'from': from_}
        if st_date:
            filters['after'] = st_date
        if end_date:
            filters['before'] = end_date
        return filters

    @staticmethod
    def pass_filters(msg, filters: Dict) -> bool:
        msg_from = re.search(r'.+@(\S+)', msg['from']).group(1)
        msg_from = msg_from.replace('>', '')
        if msg_from != filters['from']:
            return False
        msg_date = re.search(r'(.+)\d{2}:\d{2}:\d{2}', msg['date']).group(1)
        msg_date = parser.parse(msg_date).date()
        after, before = filters.get('after', date.min), filters.get('before', date.max)
        if not after <= msg_date < before:
            return False
        return True
