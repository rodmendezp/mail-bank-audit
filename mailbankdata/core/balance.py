from typing import List
from mailbankdata import Transaction
from mailbankdata.core.constants import CHECK_TTYPES, NAT_CRED_TTYPES, INT_CRED_TTYPES


class Balance:
    def __init__(self, check: float = 0, nat_cred: float = 0, int_cred: float = 0):
        self.check = check
        self.nat_cred = nat_cred
        self.int_cred = int_cred

    def update(self, transactions: List[Transaction]):
        for t in transactions:
            if t.ttype in CHECK_TTYPES:
                self.check += CHECK_TTYPES[t.ttype] * t.amount
            if t.ttype in NAT_CRED_TTYPES:
                self.nat_cred += NAT_CRED_TTYPES[t.ttype] * t.amount
            if t.ttype in INT_CRED_TTYPES:
                self.int_cred += INT_CRED_TTYPES[t.ttype] * t.int_amount
        return

    def __str__(self):
        return f'(check: {self.check}, nat_cred: {self.nat_cred}, int_cred: {self.int_cred})'
