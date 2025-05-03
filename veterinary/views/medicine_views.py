# views.py

from rest_framework import generics, permissions, authentication

from ..serializers import MedicineSerializer
from ..tasks import analyze_medicine  # Celery task
from ..models import Medicine


class MedicineCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = MedicineSerializer

    def perform_create(self, serializer):
        medicine = serializer.save(user=self.request.user)
        analyze_medicine.delay(medicine.id)


class MedicineListView(generics.ListAPIView):
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        return Medicine.objects.filter(user=self.request.user).order_by("-created_at")


class MedicineDetailView(generics.RetrieveAPIView):
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        return Medicine.objects.filter(user=self.request.user)
