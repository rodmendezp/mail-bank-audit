import bankdata.core.constants as consts

TransType = consts.TransactionType

EMAIL = 'bancochile.cl'

MAIL_SUBJ = {
    TransType.NAT_CRED_PAY: 'Comprobante Pago Tarjeta',
    TransType.INT_CRED_PAY: 'Comprobante Pago Tarjeta Internacional',
    TransType.CHECK_TRANSFER: 'Transferencias de Fondos',
    TransType.NAT_CRED_EXPENSE: 'Notificación de Compra',
    TransType.INT_CRED_EXPENSE: 'Notificación de Compra',
    TransType.CHECK_EXPENSE: 'Notificación de Compra',
    TransType.CHECK_WITHDRAW: 'Notificación de Giro'
}

MAIL_REGEX = {
    TransType.NAT_CRED_PAY: 'monto Nacional de \$(\S+) con cargo a su Cuenta Corriente',
    TransType.INT_CRED_PAY: 'Monto Pagado\<\/td\>.+USD (\S+)\<\/td\>',
    TransType.CHECK_TRANSFER: 'Monto\<\/td\>.+\$(\S+)\<\/td\>',
    TransType.NAT_CRED_EXPENSE: 'Compra por \$(\S+) con T\.Crédito',
    TransType.INT_CRED_EXPENSE: 'Compra por US\$(\S+) con T\.Crédito',
    TransType.CHECK_EXPENSE: 'Compra por \$(\S+) con cargo a Cuenta',
    TransType.CHECK_WITHDRAW: 'Giro en Cajero por \$(\S+) con cargo a Cuenta'
}


