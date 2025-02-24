from ..models import Veterinarian


def get_count_of_veterinarians():
    """get count of veterinarians"""
    return Veterinarian.objects.filter(is_active=True).count()
