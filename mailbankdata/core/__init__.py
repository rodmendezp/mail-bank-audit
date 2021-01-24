from typing import Match
from datetime import datetime
from mailbankdata.core.constants import TransactionType as TransType


class Transaction:
    def __init__(self, ttype: TransType, mail_dtime: datetime, amount=None, int_amount=None, rate=None) -> None:
        self.amount = amount
        self.int_amount = int_amount
        self.rate = rate
        self.ttype = ttype
        self.dtime = None
        self.mail_dtime = mail_dtime

    def __repr__(self) -> str:
        if self.rate:
            return '(%s, %s, %s, USD %s (%s))' % (self.mail_dtime, self.ttype.name, self.amount, self.int_amount, self.rate)
        if self.int_amount:
            return '(%s, %s, USD %s)' % (self.mail_dtime, self.ttype.name, self.int_amount)
        return '(%s, %s, %s)' % (self.mail_dtime, self.ttype.name, self.amount)

    @classmethod
    def from_match(cls, match: Match, mail_dtime: datetime, ttype: TransType) -> 'Transaction':
        groups_dict = match.groupdict()
        transaction = cls.__new__(cls)
        kwargs = {
            'ttype': ttype,
            'mail_dtime': mail_dtime,
        }
        if 'nat' in groups_dict:
            kwargs['amount'] = float(groups_dict['nat'].replace('.', '').replace(',', '.'))
        if 'int' in groups_dict:
            kwargs['int_amount'] = float(groups_dict['int'].replace(',', '.'))
        if 'rate' in groups_dict:
            kwargs['rate'] = float(groups_dict.get('rate', None).replace('.', '').replace(',', '.'))
        transaction.__init__(**kwargs)
        return transaction
