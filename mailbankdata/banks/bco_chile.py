import mailbankdata.core.constants as consts

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
    TransType.NAT_CRED_PAY:
        r'monto Nacional de \$(?P<nat>\S+) con cargo a su Cuenta Corriente',
    TransType.INT_CRED_PAY:
        r'Tipo de Cambio[^$]*\$ (?P<rate>\S+)\<\/td\>.+'
        r'Monto Pagado\<\/td\>.+?(?=USD)USD (?P<int>\S+)\<\/td\>.+'
        r'Monto Pagado Pesos\<\/td\>[^$]*\$ (?P<nat>\S+)\<\/td\>',
    TransType.CHECK_TRANSFER:
        r'Monto\<\/td\>[^$]*\$(?P<nat>\S+)\<\/td\>',
    TransType.NAT_CRED_EXPENSE:
        r'Compra por \$(?P<nat>\S+) con T\.Crédito',
    TransType.INT_CRED_EXPENSE:
        r'Compra por US\$(?P<int>\S+) con T\.Crédito',
    TransType.CHECK_EXPENSE:
        r'Compra por \$(?P<nat>\S+) con cargo a Cuenta',
    TransType.CHECK_WITHDRAW:
        r'Giro en Cajero por \$(?P<nat>\S+) con cargo a Cuenta'
}
