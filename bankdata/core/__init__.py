from bankdata.core.constants import TransactionType


class Transaction:
    def __init__(self, amount: float, trans_type: TransactionType) -> None:
        self.amount = amount
        self.trans_type = trans_type

    def __repr__(self) -> str:
        return '%s %s' % (self.trans_type.name, self.amount)

