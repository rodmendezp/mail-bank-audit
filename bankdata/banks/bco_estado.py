import bankdata.core.constants as consts

TransType = consts.TransactionType

EMAIL = 'bancoestado.cl'

MAIL_SUBJ = {
    TransType.CHECK_TRANSFER: 'Aviso de Transferencia de Fondos',
    TransType.CHECK_EXPENSE: 'Notificacion de compra',
    TransType.CHECK_WITHDRAW: 'Notificacion de giro',
}

MAIL_REGEX = {
    TransType.CHECK_TRANSFER: 'Acabas de realizar una Transferencia.+Monto transferido\:.+\<strong\>\$(\S+)\<\/strong\>',
    TransType.CHECK_EXPENSE: 'compra .*por \$(\S+) en (.+) asociado a su tarjeta',
    TransType.CHECK_WITHDRAW: 'giro en .+ por \$(\S+) asociado a su tarjeta',
}
