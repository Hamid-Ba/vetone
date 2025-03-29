from rest_framework import serializers

from monitoring.models.observability import CodeLog

from ..models.veterinarian_models import Veterinarian
from ..models import Request, AnimalRequest
from .veterinarian_serializer import VeterinarianSerializer
from .rancher_serializer import RancherVeterinarianSerializer


class AnimalRequestSerializer(serializers.ModelSerializer):
    animal = serializers.CharField(source="animal.name", read_only=True)
    image = serializers.ImageField(source="animal.image.image", read_only=True)

    def get_image(self, obj):
        return obj.animal.image.image

    class Meta:
        model = AnimalRequest
        fields = ["id", "count", "animal", "request", "image"]
        read_only_fields = ["is_active", "created_at"]
        extra_kwargs = {"request": {"read_only": True}}  # Prevent manual assignment


class CreateRequestSerializer(serializers.ModelSerializer):
    # animals = AnimalRequestSerializer(many=True, write_only=True)
    animals = serializers.JSONField(write_only=True)
    veterinarian = serializers.CharField(required=True)

    class Meta:
        model = Request
        fields = [
            "id",
            "description",
            "voice",
            "video",
            "type",
            "date",
            "time",
            "tracking_code",
            "latitude",
            "longitude",
            "rancher",
            "veterinarian",
            "animals",
            "image",
        ]
        read_only_fields = ["is_active", "created_at", "rancher", "tracking_code"]

    def validate_animals(self, value):
        # Check if each item in the animals array has the required fields
        for animal in value:
            if not all(key in animal for key in ["count", "animal_id"]):
                raise serializers.ValidationError(
                    "Each animal must have 'count', 'animal_id' fields."
                )

            # Additional validation for types, if necessary
            if not isinstance(animal["count"], int):
                raise serializers.ValidationError("'count' must be an integer")

        return value

    def validate_veterinarian(self, value):
        # Check if each item in the veterinarian array has the required fields

        try:
            veterinarian_id = int(value)
            veterinarian = Veterinarian.objects.get(id=veterinarian_id)
            return veterinarian
        except Exception as e:
            CodeLog.log_critical(
                "request_serializer.py - class CreateRequestSerializer",
                "def validate_veterinarian",
                str(e),
            )
            raise serializers.ValidationError("Veterinarian id is wrong")

        return value

    def create(self, validated_data):
        animals_data = validated_data.pop("animals", [])
        # Create Request
        tracking_code = 1000000000000000 + Request.objects.count()
        request_instance = Request.objects.create(
            tracking_code=tracking_code, **validated_data
        )

        # Create related AnimalRequests
        for animal_data in animals_data:
            AnimalRequest.objects.create(request=request_instance, **animal_data)

        return request_instance


class RequestSerializer(CreateRequestSerializer):

    # Returning full object in response
    animals = AnimalRequestSerializer(many=True, read_only=True)
    rancher = RancherVeterinarianSerializer(read_only=True)
    veterinarian = VeterinarianSerializer(read_only=True)

    class Meta(CreateRequestSerializer.Meta):
        pass
