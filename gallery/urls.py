from django.urls import path

from gallery import views

app_name = "gallery"

urlpatterns = [
    path("galleries/", views.GalleryList.as_view(), name="gallery_list"),
    path("medias/", views.MediaList.as_view(), name="media_list"),
]
