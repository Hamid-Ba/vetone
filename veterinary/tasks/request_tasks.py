from celery import shared_task

from monitoring.models.observability import CodeLog

from notifications import *


@shared_task
def inform_veterinarian_for_new_request(phone: str, tracking_code: str):
    try:
        kavenegar = KavenegarSMS()
        kavenegar.vet_new_req(phone, tracking_code)
        kavenegar.send()
        return True
    except Exception as e:
        CodeLog.log_critical(
            "request_tasks.py", "def inform_veterinarian_for_new_request", str(e)
        )

    return False


@shared_task
def inform_rancher_for_new_request(phone: str, tracking_code: str):
    try:
        kavenegar = KavenegarSMS()
        kavenegar.rancher_new_req(phone, tracking_code)
        kavenegar.send()
        return True
    except Exception as e:
        CodeLog.log_critical(
            "request_tasks.py", "def inform_veterinarian_for_new_request", str(e)
        )

    return False


@shared_task
def inform_rancher_for_confirm_or_reject_request(
    phone: str, tracking_code: str, status: bool
):
    try:
        kavenegar = KavenegarSMS()
        if status:
            kavenegar.confirm_rancher_req(phone, tracking_code)
        else:
            kavenegar.reject_rancher_req(phone, tracking_code)
        kavenegar.send()
        return True
    except Exception as e:
        CodeLog.log_critical(
            "request_tasks.py", "def inform_veterinarian_for_new_request", str(e)
        )

    return False
