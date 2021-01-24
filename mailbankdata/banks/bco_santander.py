import mailbankdata.core.constants as consts

TransType = consts.TransactionType

EMAIL = 'santander.cl'

MAIL_SUBJ = {
  TransType.CHECK_TRANSFER: 'Transferencia de fondos'
}

MAIL_REGEX = {
  TransType.CHECK_TRANSFER:
    r'Monto de Transferencia\:[^$]*\$ (?P<nat>\S+)\.\-',
}
