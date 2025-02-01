from decimal import Decimal
from drf_spectacular.utils import extend_schema
from django.shortcuts import redirect, get_object_or_404, resolve_url
from rest_framework_simplejwt import authentication
from django.conf import settings
from datetime import datetime
from rest_framework import (
    mixins,
    viewsets,
    views,
    response,
    permissions,
    status,
    serializers,
    authentication,
)

from config.pagination import StandardPagination

from monitoring.models.observability import CodeLog
from zarinpal.serializers import PaymentSerializer, PaymentInputSerializer

from .models import Payment
from .zp import Zarinpal, ZarinpalError


# zarin_pal = Zarinpal(settings.MERCHANT_ID, settings.VERIFY_URL, sandbox=True)
FRONT_VERIFY = settings.FRONT_VERIFY


class TransactionRequest(views.APIView):
    """Making Payment View."""

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    class TransactionOutputSerializer(serializers.Serializer):
        detail = serializers.CharField(required=True)

    @extend_schema(
        request=PaymentInputSerializer, responses=TransactionOutputSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            user = self.request.user
        except:
            return response.Response(
                {"detial": "شما قادر به شارژ کیف پول نمی باشید"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PaymentInputSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data.get("pay_amount", 0)
            zarin_pal = Zarinpal(
                settings.MERCHANT_ID,
                settings.VERIFY_URL,
                sandbox=False,
            )
            desc = f"شارژ کیف پول  {user.phone} به میزان {amount} تومان"
            try:
                # try to create payment if success get url to redirect it
                redirect_url = zarin_pal.payment_request(
                    int(amount),
                    desc,
                    mobile=self.request.user.phone,
                    email=self.request.user.email,
                )

                payment = Payment.objects.create(
                    user=user,
                    pay_amount=Decimal(amount),
                    desc=desc,
                    authority=zarin_pal.authority,
                )
                payment.save()

                # redirect user to zarinpal payment gate to paid
                return response.Response(
                    self.TransactionOutputSerializer({"detail": redirect_url}).data,
                    status=status.HTTP_201_CREATED,
                )
                # return redirect(redirect_url)

            # if got error from zarinpal
            except ZarinpalError as e:
                CodeLog.log_critical(
                    "zarinpal-views.py",
                    "TransactionRequest-def post",
                    str(e),
                    {"user": user},
                )
                return response.Response(
                    self.TransactionOutputSerializer({"detail": str(e)}).data,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


class TransactionVerify(views.APIView):
    """TransactionVerify View"""

    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            res_data = request.query_params
            authority = res_data["Authority"]
        except ZarinpalError:
            return redirect(FRONT_VERIFY + "?status=NOK")

        payment = get_object_or_404(Payment, authority=authority)

        if res_data["Status"] != "OK":
            payment.status = 3
            payment.save()
            return redirect(FRONT_VERIFY + "?status=CANCELLED")
        try:
            zarin_pal = Zarinpal(
                settings.MERCHANT_ID,
                settings.VERIFY_URL,
                sandbox=False,
            )
            code, message, ref_id = zarin_pal.payment_verification(
                int(payment.pay_amount), authority
            )

            # everything is ok
            if code == 100:
                payment.ref_id = ref_id
                payment.is_payed = True
                payment.payed_date = datetime.now()
                payment.status = 2
                payment.save()

                return redirect(FRONT_VERIFY + "?status=OK&RefID=" + str(ref_id))
            # operation was successful but PaymentVerification operation on this transaction have already been done
            elif code == 101:
                return redirect(FRONT_VERIFY + "?status=PAYED")

        # if got an error from zarinpal
        except ZarinpalError:
            return redirect(FRONT_VERIFY + "?status=NOK")


class PaymentsView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Payments View"""

    serializer_class = PaymentSerializer
    pagination_class = StandardPagination
    queryset = Payment.objects.order_by("-created_at")
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_serializer_context(self):
        context = {"request": self.request}
        return context

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
