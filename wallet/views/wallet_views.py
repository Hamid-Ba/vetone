from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import views, generics, response, status, permissions, authentication
from rest_framework.filters import SearchFilter

from monitoring.models.observability import CodeLog

from ..models import Transaction
from ..serializers import TransactionSerializer

from config.pagination import StandardPagination


class TransactionListAPI(generics.ListAPIView):
    """Transaction List API"""

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.order_by("-created_at")
    pagination_class = StandardPagination
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    filter_backends = [SearchFilter]
    search_fields = ["type"]

    def get_queryset(self):
        queryset = self.queryset.filter(wallet=self.request.user.wallet)

        # Get query parameters
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        # Filter by date range if provided
        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset.order_by("-created_at")


class TransactionDetailAPI(views.APIView):
    """Transaction Detail API"""

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    @extend_schema(responses=TransactionSerializer)
    def get(self, request, id, *args, **kwargs):
        transaction = get_object_or_404(Transaction, pk=id)

        if transaction.wallet.user != self.request.user:
            CodeLog.log_warning(
                "wallet_views.py",
                "TransactionDetailAPI",
                "Someone wants to do dirty things!",
                {"user_id": self.request.user},
            )
            return response.Response(
                {"message": "you are now allowed to get transaction of this wallet"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transaction = TransactionSerializer(transaction, many=False).data

        return response.Response(transaction, status=status.HTTP_200_OK)
