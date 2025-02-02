from django.db.models.signals import post_delete
from django.dispatch import receiver

from gallery.models import Gallery, Media


@receiver(post_delete, sender=Gallery)
def post_delete_gallery_image(sender, instance, *args, **kwargs):
    """Clean Old Image file"""
    try:
        instance.image.delete(save=False)
    except:
        pass


@receiver(post_delete, sender=Media)
def post_delete_media_image(sender, instance, *args, **kwargs):
    """Clean Old Image file"""
    try:
        instance.file.delete(save=False)
        instance.thumbnail.delete(save=False)
    except:
        pass
