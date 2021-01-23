from typing import Match
from mailbankdata.core.constants import TransactionType


class Transaction:
    def __init__(self, ttype: TransactionType, amount=None, int_amount=None, rate=None) -> None:
        self.amount = amount
        self.int_amount = int_amount
        self.rate = rate
        self.ttype = ttype

    def __repr__(self) -> str:
        if self.rate:
            return '(%s, %s, USD %s (%s))' % (self.ttype, self.amount, self.int_amount, self.rate)
        if self.int_amount:
            return '(%s, USD %s)' % (self.ttype.name, self.int_amount)
        return '(%s, %s)' % (self.ttype.name, self.amount)

    @classmethod
    def from_match(cls, match: Match, ttype: TransactionType) -> 'Transaction':
        groups_dict = match.groupdict()
        transaction = cls.__new__(cls)
        kwargs = {'ttype': ttype}
        if 'nat' in groups_dict:
            kwargs['amount'] = float(groups_dict['nat'].replace('.', '').replace(',', '.'))
        if 'int' in groups_dict:
            kwargs['int_amount'] = float(groups_dict['int'].replace(',', '.'))
        if 'rate' in groups_dict:
            kwargs['rate'] = float(groups_dict.get('rate', None).replace('.', '').replace(',', '.'))
        transaction.__init__(**kwargs)
        return transaction
