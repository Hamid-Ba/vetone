# tasks.py

from celery import shared_task
from django.conf import settings
import base64
import requests

from notifications import *
from monitoring.models.observability import CodeLog

from ..models import Medicine


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def ask_gemini_about_medicine(medicine_name: str, image_base64: str):
    headers = {"Content-Type": "application/json"}
    prompt = f"""
    یک کاربر تصویر دارویی ارسال کرده و همچنین نام آن را نوشته است.
    نام دارو: {medicine_name}
    لطفاً بر اساس نام و تصویر، کاربردها، موارد مصرف و دسته دارویی این دارو را به زبان فارسی توضیح دهید.
    """

    response = requests.post(
        f"{settings.GEMINI_API_URL}?key={settings.GEMINI_API_KEY}",
        headers=headers,
        json={
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64,
                            }
                        },
                    ]
                }
            ]
        },
    )
    result = response.json()
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "پاسخی از هوش مصنوعی دریافت نشد."


@shared_task
def analyze_medicine(medicine_id):
    try:
        med = Medicine.objects.get(id=medicine_id)
        image_base64 = encode_image_to_base64(med.image.path)
        result = ask_gemini_about_medicine(med.name, image_base64)
        med.analysis_result = result
        med.save()

        CodeLog.log_info(
            "medicine_tasks.py",
            "def analyze_medicine",
            f"Medicine ID: {medicine_id} - Result: {result}",
        )
        return f"✅ تحلیل با موفقیت انجام شد برای دارو {medicine_id}"
    except Medicine.DoesNotExist:
        CodeLog.log_error(
            "medicine_tasks.py",
            "def analyze_request_with_ai",
            f"Request ID: {medicine_id} not found.",
        )
        return f"❌ دارو با شناسه {medicine_id} یافت نشد."
    except Exception as e:
        CodeLog.log_error("medicine_tasks.py", "def analyze_medicine", str(e))
        return f"❌ خطا در تحلیل: {str(e)}"
