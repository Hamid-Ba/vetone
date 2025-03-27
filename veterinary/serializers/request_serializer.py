from rest_framework import serializers
from ..models import Request, AnimalRequest
from .veterinarian_serializer import VeterinarianSerializer
from .rancher_serializer import RancherVeterinarianSerializer


class AnimalRequestSerializer(serializers.ModelSerializer):
    animal = serializers.CharField(source="animal.name", read_only=True)

    class Meta:
        model = AnimalRequest
        fields = ["id", "count", "weight", "sign", "animal", "request"]
        read_only_fields = ["is_active", "created_at"]
        extra_kwargs = {"request": {"read_only": True}}  # Prevent manual assignment


class CreateRequestSerializer(serializers.ModelSerializer):
    # animals = AnimalRequestSerializer(many=True, write_only=True)
    animals = serializers.JSONField(write_only=True)

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
            "rancher",
            "veterinarian",
            "animals",
            "image",
        ]
        read_only_fields = ["is_active", "created_at", "rancher"]

    def validate_animals(self, value):
        # Check if each item in the animals array has the required fields
        for animal in value:
            if not all(
                key in animal for key in ["count", "weight", "sign", "animal_id"]
            ):
                raise serializers.ValidationError(
                    "Each animal must have 'count', 'weight', 'sign', and 'animal' fields."
                )

            # Additional validation for types, if necessary
            if not isinstance(animal["count"], int) or not isinstance(
                animal["weight"], int
            ):
                raise serializers.ValidationError(
                    "'count' must be an integer and 'weight' must be a float."
                )

        return value

    def create(self, validated_data):
        animals_data = validated_data.pop("animals", [])
        # Create Request
        request_instance = Request.objects.create(**validated_data)

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
