import mailbankdata.core.constants as consts

TransType = consts.TransactionType

EMAIL = 'scotiabank.cl'

MAIL_SUBJ = {
    TransType.CHECK_EXPENSE: 'Comprobante de Pagos'
}

MAIL_REGEX = {
    TransType.CHECK_EXPENSE:
        r'Monto pagado\<\/span\>[^$]*\$ (?P<nat>\S+)\<\/span\>',

}