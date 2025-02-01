from config.celery import app

from notifications import KavenegarSMS
from .models import Wallet


@app.task
def wallet_balance_check():
    wallets = Wallet.objects.filter(balance__gte=100_000, balance__lte=300_000)
    sms = KavenegarSMS()
    for wallet in wallets:
        sms.check_wallet(receptor=wallet.store.user.phone, code=wallet.store.user.phone)
        sms.send()
