"""
Account Module Serializers
"""
from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from random import randint

from monitoring.models.observability import CodeLog
from notifications import KavenegarSMS
import os


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""

    class Meta:
        """Meta Class"""

        model = get_user_model()
        fields = [
            "id",
            "fullName",
            "phone",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "password",
            "groups",
            "user_permissions",
        ]
        read_only_fields = [
            "id",
            "phone",
            "is_active",
            "is_staff",
            "groups",
            "user_permissions",
            "is_superuser",
            "last_login",
            "password",
        ]


class AuthenticationSerializer(serializers.Serializer):
    """Authentication Serializer For Login And Register"""

    phone = serializers.CharField(
        max_length=11,
        required=True,
        error_messages={
            "blank": "موبایل خود را وارد نمایید",
            "required": "موبایل خود را وارد نمایید",
        },
    )

    def validate(self, attrs):
        phone = attrs.get("phone")
        if not phone.isdigit():
            return super().validate(attrs)
        return attrs

    def create(self, validated_data):
        """Login Or Register User"""
        phone = validated_data.get("phone")
        otp = str(randint(100000, 999999))

        user, created = get_user_model().objects.get_or_create(phone=phone)
        user.set_password(otp)
        # For Test
        user.fullName = otp
        user.save()

        # Send Otp Code
        IS_TEST = os.getenv("IS_TEST", default=False)
        if not IS_TEST:
            try:
                kavenegar = KavenegarSMS()
                kavenegar.otp(user.phone, otp)
                kavenegar.send()
            except Exception as e:
                CodeLog.log_error("account - serializers.py", "def create", str(e))
                raise serializers.ValidationError("kavenegar error")

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Auth Token Serializer For Create Token"""

    phone = serializers.CharField(
        max_length=11,
        required=True,
        error_messages={"blank": "موبایل خود را وارد نمایید"},
    )
    password = serializers.CharField(
        max_length=11,
        required=True,
        error_messages={"blank": "رمز یک بار مصرف خود را وارد نمایید"},
    )

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=phone, password=password
        )

        if not user:
            msg = "کد وارد شده نامعتبر است"
            raise serializers.ValidationError(msg, code="authorization")

        user.last_login = datetime.now()
        user.save()

        attrs["user"] = user
        return attrs
