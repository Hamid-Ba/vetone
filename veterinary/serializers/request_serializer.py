from rest_framework import serializers
from ..models import Request, AnimalRequest
from .veterinarian_serializer import VeterinarianSerializer
from .rancher_serializer import RancherVeterinarianSerializer


class AnimalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalRequest
        fields = ["id", "count", "weight", "sign", "animal", "request"]
        read_only_fields = ["is_active", "created_at"]
        extra_kwargs = {"request": {"read_only": True}}  # Prevent manual assignment


class CreateRequestSerializer(serializers.ModelSerializer):
    animals = AnimalRequestSerializer(many=True, write_only=True)

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
        read_only_fields = ["is_active", "created_at"]

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
    rancher = RancherVeterinarianSerializer(read_only=True)
    veterinarian = VeterinarianSerializer(read_only=True)

    class Meta(CreateRequestSerializer.Meta):
        pass
