# Mail Bank Audit

**Mail Bank Audit** is a python package that can go through
your emails and check your bank transactions.  
Sometimes your bank transaction information is incomplete
(specially with credit cards or due to websites maintenance) 
and you can use this package go through your emails and list 
the transactions you have done.  


It currently supports using gmail api or reading extracted 
data from gmail.


## How to use


## Supported Banks

| Name | Country | 
| ---  | ------- |
| Banco de Chile | Chile | 
| Banco Estado   | Chile |

To include a new bank add it to `Bank(Enum)` in `mailbankdata\banks\__init__.py`
and its name must match a new file in `mailbankdata\banks\bank_name.py` (lower case).  
Inside `mailbankdata\banks\bank_name.py` define `MAIL_SUBJ` and `MAIL_REGEX`, with the 
last being a regex where the first group correspond where the amount should be.

## What's Next
* Add support for more banks
* Plotting expenses by category
