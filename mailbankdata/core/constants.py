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

