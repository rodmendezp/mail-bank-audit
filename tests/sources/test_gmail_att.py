from datetime import date
from typing import Dict, Any
from unittest import TestCase
from unittest.mock import MagicMock
from mailbankdata.banks import bco_chile, Bank
from mailbankdata.sources import GMailAttachmentBankApi


class TestGMailAttachmentBankApi(TestCase):
    mock_api = None

    @staticmethod
    def get_mock_api(result: Dict):
        mock_api = MagicMock()

        def mock_list(userId: str, q: str):
            return mock_api

        def mock_get(userId: str, id: int):
            return mock_api

        mock_api.users = lambda: mock_api
        mock_api.messages = lambda: mock_api
        mock_api.list = mock_list
        mock_api.get = mock_get
        mock_api.execute = lambda: result
        return mock_api

    def setUp(self) -> None:
        super().setUp()

    def test_constructor(self):
        GMailAttachmentBankApi(None, Bank.BCO_CHILE, 123456)

    def test_constructor_exc(self):
        with self.assertRaises(Exception):
            GMailAttachmentBankApi(None, Bank.BCO_CHILE)

    def test_generate_filters(self):
        st_date, end_date = date(1, 1, 1), date(1, 1, 2)
        filters = GMailAttachmentBankApi.generate_filters(bco_chile.EMAIL, st_date, end_date)
        expected = {'from': bco_chile.EMAIL, 'after': st_date, 'before': end_date}
        self.assertEqual(filters, expected)

    def test_get_message_id_exc(self):
        subj = 'somesubject'
        with self.assertRaises(Exception) as e:
            mock_api = self.get_mock_api({'resultSizeEstimate': 0})
            gmail_api = GMailAttachmentBankApi(mock_api, Bank.BCO_CHILE, 123456)
            gmail_api._get_message_id(subj)
        self.assertEqual(e.exception.args[0], f'Did not find message with subject {subj}')

        with self.assertRaises(Exception) as e:
            mock_api = self.get_mock_api({'resultSizeEstimate': 2})
            gmail_api = GMailAttachmentBankApi(mock_api, Bank.BCO_CHILE, 123456)
            gmail_api._get_message_id(subj)
        self.assertEqual(e.exception.args[0], f'Subject {subj} needs to be unique, 2 mails match this subject')

    def test_get_message_id(self):
        msg_id = 1234
        mock_api = self.get_mock_api({'resultSizeEstimate': 1, 'messages': [{'id': msg_id}]})
        gmail_api = GMailAttachmentBankApi(mock_api, Bank.BCO_CHILE, 123456)
        self.assertEqual(gmail_api._get_message_id('somesubj'), msg_id)

