from decimal import Decimal

from model_bakery import baker
from rest_framework.test import APITestCase

from ..models import *


class WalletTestCase(APITestCase):
    def setUp(self):
        """Set up Wallet for tests."""
        self.user = baker.make("account.User", phone="09151498721")

        self.user.wallet.balance = Decimal("1000.00")

        self.wallet = self.user.wallet

    def test_wallet_charge(self):
        """Test charging the wallet."""
        initial_balance = self.wallet.balance
        charge_amount = Decimal("500.00")
        self.wallet.charge(charge_amount)
        self.wallet.refresh_from_db()

        # Assert that the balance has been correctly updated
        self.assertEqual(self.wallet.balance, initial_balance + charge_amount)

    def test_wallet_deduct_sufficient_balance(self):
        """Test deducting from the wallet with sufficient balance."""
        deduct_amount = Decimal("100.00")

        self.wallet.deduct(deduct_amount)  # Deduction should succeed
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("900.00"))

    def test_wallet_deduct_insufficient_balance(self):
        """Test deducting from the wallet with insufficient balance."""
        deduct_amount = Decimal("1500.00")
        self.wallet.deduct(deduct_amount)
        self.wallet.refresh_from_db()
        self.assertTrue(self.wallet.balance < 0)  # User Must Be Desabled

    def test_transaction_creation_on_charge(self):
        """Test that a transaction is logged when the wallet is charged."""
        charge_amount = Decimal("200.00")
        initial_transaction_count = Transaction.objects.count()
        self.wallet.charge(charge_amount)
        self.assertEqual(Transaction.objects.count(), initial_transaction_count + 1)
        transaction = Transaction.objects.last()
        self.assertEqual(transaction.amount, charge_amount)

    def test_transaction_creation_on_deduct(self):
        """Test that a transaction is logged when the wallet is deducted."""
        deduct_amount = Decimal("100.00")
        self.wallet.deduct(deduct_amount)
        transaction = Transaction.objects.last()
        self.assertEqual(
            transaction.amount, -deduct_amount
        )  # Deduction should create a negative transaction
