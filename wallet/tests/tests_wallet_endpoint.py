from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from model_bakery import baker

from ..serializers import TransactionSerializer
from ..models import Transaction

TRANSACTION_LIST_URL = reverse("wallet:transactions")


def transaction_detail_url(id):
    return reverse("wallet:transaction", kwargs={"id": id})


class PrivateTest(TestCase):
    """Test Those Endpoints Which Need User To Be Authorized"""

    def setUp(self):
        self.client = APIClient()
        self.user = baker.make("account.User", phone="09151498722")
        self.client.force_authenticate(self.user)

        self.wallet = self.user.wallet

    def test_get_transaction_should_work_properly(self):
        """Test Get Transaction"""

        transaction = baker.make(Transaction, wallet=self.user.wallet)
        transaction_2 = baker.make(Transaction, wallet=self.user.wallet)

        url = transaction_detail_url(transaction.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        self.assertEqual(TransactionSerializer(transaction).data, res.json())
        self.assertNotEqual(TransactionSerializer(transaction_2).data, res.json())

    def test_list_transaction_should_work_properly(self):
        """Test List Of Transaction API"""
        transaction_1 = baker.make(Transaction, wallet=self.wallet)
        transaction_2 = baker.make(Transaction, wallet=self.wallet)
        transaction_3 = baker.make(Transaction, wallet=self.wallet)

        user_2 = baker.make("account.User", phone="09151498721")
        transaction_4 = baker.make(Transaction, wallet=user_2.wallet)

        res = self.client.get(TRANSACTION_LIST_URL)
        self.assertEqual(res.status_code, 200)

        res_json_res = res.json()["results"]

        self.assertIn(TransactionSerializer(transaction_1).data, res_json_res)
        self.assertIn(TransactionSerializer(transaction_2).data, res_json_res)
        self.assertIn(TransactionSerializer(transaction_3).data, res_json_res)
        self.assertNotIn(TransactionSerializer(transaction_4).data, res_json_res)

    def test_search_transaction_by_type_should_work_properly(self):
        """Test List Of Transaction API"""
        transaction_1 = baker.make(Transaction, type="C", wallet=self.wallet)
        transaction_2 = baker.make(Transaction, type="C", wallet=self.wallet)
        transaction_3 = baker.make(Transaction, type="D", wallet=self.wallet)

        user_2 = baker.make("account.User", phone="09151498721")
        transaction_4 = baker.make(Transaction, wallet=user_2.wallet)

        res = self.client.get(TRANSACTION_LIST_URL, {"search": "C"})
        self.assertEqual(res.status_code, 200)

        res_json_res = res.json()["results"]

        self.assertIn(TransactionSerializer(transaction_1).data, res_json_res)
        self.assertIn(TransactionSerializer(transaction_2).data, res_json_res)
        self.assertNotIn(TransactionSerializer(transaction_3).data, res_json_res)
        self.assertNotIn(TransactionSerializer(transaction_4).data, res_json_res)
