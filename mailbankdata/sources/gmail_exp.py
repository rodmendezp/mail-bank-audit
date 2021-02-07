import re
import email
import zipfile
import mailbox
import importlib
from datetime import date
from dateutil import parser
from typing import List, Dict, Any
from mailbankdata.banks import Bank
from mailbankdata.core import Transaction
from mailbankdata.core.constants import TransactionType as TransType


class GMailExportBankApi:
    def __init__(self, zip_file: str, bank: Bank) -> None:
        self._bank = bank
        self._zip_file = zip_file
        self._bc = importlib.import_module(f'mailbankdata.banks.{bank.name.lower()}')
        self._extract_mbox()

    def _extract_mbox(self):
        zip_obj = zipfile.ZipFile(self._zip_file, 'r')
        mbox_zip_file_path = next(x for x in zip_obj.namelist() if x.endswith('.mbox'))
        self.mbox_file = zip_obj.extract(mbox_zip_file_path)

    def _get_transactions(self, filters, trans_types: List[TransType]) -> List[Transaction]:
        transactions = []
        for msg in mailbox.mbox(self.mbox_file):
            if not self.pass_filters(msg, filters):
                continue
            msg_subj = email.header.decode_header(msg['subject'])[0][0]
            if isinstance(msg_subj, bytes):
                msg_subj = msg_subj.decode()
            trans_type = next((t for t in trans_types if re.search(self._bc.MAIL_SUBJ[t], msg_subj)), None)
            if not trans_type:
                # Subject does not match to any of transactions subjects
                continue
            mail_reg = self._bc.MAIL_REGEX[trans_type]
            if msg.is_multipart():
                text = ''.join(part.get_payload(decode=True).decode() for part in msg.get_payload())
            else:
                text = msg.get_payload(decode=True).decode()
            match = re.search(mail_reg, text, re.DOTALL)
            if not match:
                # Mail's body does not contain regex
                continue
            mail_dtime = next(x[1] for x in msg._headers if x[0] == 'Date')
            mail_dtime = parser.parse(mail_dtime).replace(tzinfo=None)
            t = Transaction.from_match(match, mail_dtime, trans_type)
            transactions.append(t)
        return transactions

    @staticmethod
    def generate_filters(from_: str, st_date: date, end_date: date) -> Dict[str, Any]:
        filters = {
            'from': from_,
        }
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
