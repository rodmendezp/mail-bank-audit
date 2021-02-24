from enum import Enum


class TransactionType(Enum):
    NAT_CRED_PAY = 1
    INT_CRED_PAY = 2
    CHECK_TRANSFER = 3
    NAT_CRED_EXPENSE = 4
    INT_CRED_EXPENSE = 5
    CHECK_EXPENSE = 6
    NAT_CRED_WITHDRAW = 7
    CHECK_WITHDRAW = 8


CHECK_TTYPES = {
    TransactionType.CHECK_EXPENSE: -1,
    TransactionType.CHECK_TRANSFER: -1,
    TransactionType.CHECK_WITHDRAW: -1,
    TransactionType.NAT_CRED_PAY: -1,
    TransactionType.INT_CRED_PAY: -1
}

NAT_CRED_TTYPES = {
    TransactionType.NAT_CRED_PAY: 1,
    TransactionType.NAT_CRED_EXPENSE: -1,
    TransactionType.NAT_CRED_WITHDRAW: -1
}

INT_CRED_TTYPES = {
    TransactionType.INT_CRED_PAY: 1,
    TransactionType.INT_CRED_EXPENSE: -1
}
