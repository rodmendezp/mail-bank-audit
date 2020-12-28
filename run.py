from datetime import date
from bankdata.banks import Bank
from bankdata.sources import GMailBankApi, GMailExportBankApi, GMailAttachmentBankApi


if __name__ == '__main__':
    mail_bank_api = GMailBankApi.from_token_pickle('token.pickle', Bank.BCO_CHILE)
    st_date, end_date = date(2018, 3, 10), date(2018, 3, 15)
    transactions = mail_bank_api.check_transactions(st_date, end_date)
    print(transactions)

    msg_sub = 'Prueba Emails Attachment'
    gmail_api = GMailAttachmentBankApi.api_from_token_pickle('token.pickle')
    mail_att_bank_api = GMailAttachmentBankApi(gmail_api, Bank.BCO_CHILE, msg_subj=msg_sub)
    print(mail_att_bank_api.int_credit_transactions())

    mail_export_bank_api = GMailExportBankApi('takeout.zip', Bank.BCO_CHILE)
    transactions = mail_export_bank_api.check_transactions(st_date, end_date)
    print(transactions)
