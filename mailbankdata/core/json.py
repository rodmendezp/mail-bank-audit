from typing import Any
from json import JSONEncoder
from datetime import datetime
from mailbankdata.core import Transaction
from mailbankdata.core.constants import TransactionType


class TransactionEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Transaction):
            return {k: v for k, v in o.__dict__.items() if v is not None}
        elif isinstance(o, TransactionType):
            return o.name
        elif isinstance(o, datetime):
            return o.isoformat()
        return JSONEncoder.default(self, o)
