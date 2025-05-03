# serializers.py

from rest_framework import serializers
from ..models import Medicine


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["id", "user", "name", "image", "analysis_result"]
        read_only_fields = ["id", "user", "analysis_result"]
