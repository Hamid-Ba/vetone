from ..models import Rancher


def get_count_of_ranchers():
    """get count of ranchers"""
    return Rancher.objects.filter(is_active=True).count()
