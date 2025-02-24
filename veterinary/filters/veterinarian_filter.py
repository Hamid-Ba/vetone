from django_filters import rest_framework as filters
from ..models import Veterinarian


class VeterinarianFilter(filters.FilterSet):
    fullName = filters.CharFilter(field_name="user__fullName", lookup_expr="icontains")
    province = filters.NumberFilter(field_name="province__id")
    city = filters.NumberFilter(field_name="city__id")

    class Meta:
        model = Veterinarian
        fields = [
            "fullName",
            "province",
            "city",
        ]
