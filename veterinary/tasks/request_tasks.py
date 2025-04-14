import requests
from celery import shared_task
from django.conf import settings

from notifications import *
from monitoring.models.observability import CodeLog

from ..models import Request


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


@shared_task
def inform_rancher_for_end_of_request(phone: str, tracking_code: str):
    try:
        kavenegar = KavenegarSMS()
        kavenegar.visit_done(phone, tracking_code)
        kavenegar.send()
        return True
    except Exception as e:
        CodeLog.log_critical(
            "request_tasks.py", "def inform_rancher_for_end_of_request", str(e)
        )

    return False


def get_weather(lat, lon):
    try:
        response = requests.get(
            settings.OPENWEATHER_URL,
            params={
                "lat": lat,
                "lon": lon,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "fa",
            },
        )
        data = response.json()
        return {
            "description": data["weather"][0]["description"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
        }
    except Exception as e:
        CodeLog.log_error("request_tasks.py", "def get_weather", str(e))
        return {
            "description": "اطلاعاتی در دسترس نیست",
            "temp": "نامشخص",
            "humidity": "نامشخص",
        }


def build_persian_prompt(request_instance):
    rancher_location = {
        "lat": request_instance.latitude,
        "lon": request_instance.longitude,
    }
    weather = get_weather(rancher_location["lat"], rancher_location["lon"])

    animal_requests = request_instance.animals.all()
    animal_lines = []
    for ar in animal_requests:
        animal_lines.append(f"- نوع حیوان: {ar.animal.name}، تعداد: {ar.count}")

    prompt = f"""
شما یک دستیار دامپزشک هستید که به یک دامدار برای تشخیص و مدیریت مشکل حیواناتش کمک می‌کنید.

موقعیت جغرافیایی دامدار:
- عرض جغرافیایی: {rancher_location['lat']}، طول جغرافیایی: {rancher_location['lon']}
- وضعیت آب‌وهوا: {weather['description']}، دما: {weather['temp']}°C، رطوبت: {weather['humidity']}٪

مشخصات حیوان:
{chr(10).join(animal_lines)}

شرح مشکل ارائه‌شده توسط دامدار:
{request_instance.description}

تاریخ درخواست: {request_instance.date} ساعت {request_instance.time}

لطفاً با توجه به اطلاعات بالا موارد زیر را بررسی و به زبان فارسی پاسخ دهید:
1. علت یا علل احتمالی مشکل حیوان چیست؟
2. سطح اورژانسی بودن موضوع (پایین، متوسط، بالا) چگونه است؟
3. دامدار تا زمان رسیدن دامپزشک چه اقدامات فوری می‌تواند انجام دهد؟
4. در صورت نیاز، چه اطلاعات اضافی باید جمع‌آوری شود؟
"""
    return prompt.strip()


def ask_gemini(prompt: str):
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{settings.GEMINI_API_URL}?key={settings.GEMINI_API_KEY}",
        headers=headers,
        json={
            "contents": [{"parts": [{"text": prompt}]}],
        },
    )
    result = response.json()
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        CodeLog.log_error("request_tasks.py", "def ask_gemini", str(result))
        return "پاسخی از هوش مصنوعی دریافت نشد."


@shared_task
def analyze_request_with_ai(request_id):
    try:
        req = Request.objects.get(id=request_id)
        prompt = build_persian_prompt(req)
        result = ask_gemini(prompt)

        # Save the result to the request instance
        req.analysis_result = result
        req.save()

        CodeLog.log_info(
            "request_tasks.py",
            "def analyze_request_with_ai",
            f"Request ID: {request_id} - Result: {result}",
        )
        return f"✅ تحلیل با موفقیت انجام شد برای درخواست {req.id}"
    except Request.DoesNotExist:
        CodeLog.log_error(
            "request_tasks.py",
            "def analyze_request_with_ai",
            f"Request ID: {request_id} not found.",
        )
        return f"❌ درخواست با شناسه {request_id} یافت نشد."
    except Exception as e:
        CodeLog.log_error("request_tasks.py", "def analyze_request_with_ai", str(e))
        return f"❌ خطا در تحلیل: {str(e)}"
