import mailbankdata.core.constants as consts

TransType = consts.TransactionType

EMAIL = 'bancoestado.cl'

MAIL_SUBJ = {
    TransType.CHECK_TRANSFER: 'Aviso de Transferencia de Fondos',
    TransType.CHECK_EXPENSE: 'Notificación de compra',
    TransType.CHECK_WITHDRAW: 'Notificación de giro',
}

MAIL_REGEX = {
    TransType.CHECK_TRANSFER: r'una Transferencia.+Monto transferido\:.+\<strong\>\$(?P<nat>\S+)\<\/strong\>',
    TransType.CHECK_EXPENSE: r'compra\s+por\s+\$(?P<nat>\S+)\s+en\s.+asociado a su tarjeta',
    TransType.CHECK_WITHDRAW: r'giro\s+en.+por\s+\$(?P<nat>\S+)\s+asociado\s+a\s+su\s+tarjeta',
}
