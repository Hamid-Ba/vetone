from ..models import Request


def rate_request(id: int, rate: int):
    """Rate Request"""
    request = Request.objects.filter(id=id).first()

    if request:
        request.rate = rate
        request.save()
        return True
    return False
