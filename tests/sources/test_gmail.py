import os
import base64
from datetime import date
from dateutil import parser
from unittest import TestCase
from mailbankdata.banks import Bank
from mailbankdata.banks import bco_chile
from unittest.mock import patch, MagicMock
from mailbankdata.sources import GMailBankApi
from mailbankdata import TransactionType as TransType


class TestGMailBankApi(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_api = None
        cls.str_filter = 'from:bancochile.cl after:0001-01-01 before:0001-01-02'

    def test_constructor(self):
        gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
        self.assertEqual(gmail_bank_api._api, self.mock_api)
        self.assertEqual(gmail_bank_api._bank, Bank.BCO_CHILE)
        self.assertEqual(gmail_bank_api._bc, bco_chile)

    def test_all_transactions(self):
        with patch.object(GMailBankApi, '_get_transactions') as mock:
            gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
            st_date, end_date = date(1, 1, 1), date(1, 1, 2)
            gmail_bank_api.all_transactions(st_date, end_date)
            mock.assert_called_with(self.str_filter, list(TransType))

    def test_check_transactions(self):
        check_trans_types = []
        for ttype in TransType:
            if ttype != TransType.INT_CRED_EXPENSE \
                    and ttype != TransType.NAT_CRED_EXPENSE \
                    and ttype != TransType.NAT_CRED_WITHDRAW:
                check_trans_types.append(ttype)
        with patch.object(GMailBankApi, '_get_transactions') as mock:
            gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
            st_date, end_date = date(1, 1, 1), date(1, 1, 2)
            gmail_bank_api.check_transactions(st_date, end_date)
            mock.assert_called_with(self.str_filter, check_trans_types)

    def test_credit_transactions(self):
        credit_transactions = [TransType.NAT_CRED_PAY, TransType.NAT_CRED_EXPENSE, TransType.NAT_CRED_WITHDRAW]
        with patch.object(GMailBankApi, '_get_transactions') as mock:
            gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
            st_date, end_date = date(1, 1, 1), date(1, 1, 2)
            gmail_bank_api.credit_transactions(st_date, end_date)
            mock.assert_called_with(self.str_filter, credit_transactions)

    def test_int_credit_transactions(self):
        int_cred_transactions = [TransType.INT_CRED_PAY, TransType.INT_CRED_EXPENSE]
        with patch.object(GMailBankApi, '_get_transactions') as mock:
            gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
            st_date, end_date = date(1, 1, 1), date(1, 1, 2)
            gmail_bank_api.int_credit_transactions(st_date, end_date)
            mock.assert_called_with(self.str_filter, int_cred_transactions)

    def test_generate_filters(self):
        st_date, end_date = date(1, 1, 1), date(1, 1, 2)
        filters = GMailBankApi.generate_filters(bco_chile.EMAIL, st_date, end_date)
        expected = self.str_filter
        self.assertEqual(filters, expected)

    def test_get_message_info(self):
        def mock_get(userId: str, id: int):
            return mock_api

        body = 'Hello World!'
        msg_date = 'Wed, 14 Mar 2018 15:06:46 -0300 (CLT)'
        msg_info = {
            'payload': {
                'headers': [
                    {
                        'name': 'Subject',
                        'value': 'Notificacion de Compra',
                    },
                    {
                        'name': 'Date',
                        'value': msg_date,
                    }
                ],
                'body': {'size': 0},
                'parts': [{
                    'partId': 0,
                    'mimeType': 'text/html',
                    'headers': {},
                    'body': {
                        'size': len(body),
                        'data': base64.urlsafe_b64encode(body.encode())
                    }
                }]
            }
        }
        msg = {'id': 12345}
        mock_api = MagicMock()
        mock_api.users = lambda: mock_api
        mock_api.messages = lambda: mock_api
        mock_api.get = mock_get
        mock_api.execute = lambda: msg_info
        gmail_bank_api = GMailBankApi(mock_api, Bank.BCO_CHILE)
        result = gmail_bank_api.get_message_info(msg)
        self.assertEqual(result['Subject'], 'Notificacion de Compra')
        self.assertEqual(result['Date'], parser.parse(msg_date).replace(tzinfo=None))
        self.assertEqual(result['Body'], body)

    def test_subj_possible_types(self):
        gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
        possible_types = gmail_bank_api.subj_possible_types('Notificación de Compra', list(TransType))
        expected = {TransType.INT_CRED_EXPENSE, TransType.NAT_CRED_EXPENSE, TransType.CHECK_EXPENSE}
        self.assertSetEqual(set(possible_types), expected)

    def test_msg_to_transaction(self):
        msg_body = """
        <tr>
          <td style="padding:30px 0 10px 0;">
            <font style="font-family:Arial,Tahoma,Verdana,sans-serif; font-size:15px; font-weight:normal; color:#7c7c7c;">
                Estimado Cliente: <br> <br>
                Compra por $3.400 con cargo a Cuenta ****3800 en DON HOMERO        el 14/03/2018 15:04. <br>
                Más información 600 637 37 37.
            </font>
          </td>
        </tr>
        """
        msg_date = 'Wed, 14 Mar 2018 15:06:46 -0300 (CLT)'
        msg_info = {'Body': msg_body, 'Date': parser.parse(msg_date).replace(tzinfo=None)}
        possible_types = [TransType.INT_CRED_EXPENSE, TransType.NAT_CRED_EXPENSE, TransType.CHECK_EXPENSE]
        gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
        transaction = gmail_bank_api.msg_to_transaction(msg_info, possible_types)
        self.assertEqual(transaction.amount, 3400)
        self.assertEqual(transaction.ttype, TransType.CHECK_EXPENSE)
        self.assertEqual(transaction.mail_dtime, parser.parse(msg_date).replace(tzinfo=None))

    def test_get_transactions(self):
        gmail_bank_api = GMailBankApi(self.mock_api, Bank.BCO_CHILE)
        trans_types = [
            TransType.INT_CRED_PAY,
            TransType.INT_CRED_EXPENSE
        ]

        def mock_get_messages(filters):
            return [{"id": "123456", "threadId": "234567"},
                    {"id": "234567", "threadId": "345678"},
                    {"id": "345678", "threadId": "456789"}]

        def mock_get_message_info(msg):
            cd = os.path.dirname(__file__)
            resources_path = os.path.abspath(os.path.join(cd, '..', '..', 'resources', 'bco_chile'))
            data = {}
            if msg['id'] == '123456':
                data['file_path'] = 'check_expense.html'
                data['subject'] = 'Notificación de Compra'
            elif msg['id'] == '234567':
                data['file_path'] = 'int_cred_expense.html'
                data['subject'] = 'Notificación de Compra'
            else:
                data['file_path'] = 'int_cred_pay.html'
                data['subject'] = 'Comprobante Pago Tarjeta Internacional'
            data['file_path'] = os.path.join(resources_path, data['file_path'])
            with open(data['file_path'], encoding='utf-8') as f:
                body = f.read()
            msg_info = {
                'Subject': data['subject'],
                'Date': parser.parse('Wed, 14 Mar 2018 15:06:46 -0300 (CLT)').replace(tzinfo=None),
                'Body': body,
            }
            return msg_info

        with patch.object(GMailBankApi, 'get_messages', side_effect=mock_get_messages), \
                patch.object(GMailBankApi, 'get_message_info', side_effect=mock_get_message_info):
            transactions = gmail_bank_api._get_transactions({}, trans_types)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].ttype, TransType.INT_CRED_EXPENSE)
        self.assertEqual(transactions[0].int_amount, 18.87)
        self.assertEqual(transactions[1].ttype, TransType.INT_CRED_PAY)
        self.assertEqual(transactions[1].int_amount, 18.87)
