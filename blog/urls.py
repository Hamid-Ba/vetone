from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
)

from blog import views


router = DefaultRouter()

app_name = "blog"

urlpatterns = [
    path("", include(router.urls)),
    path("<str:slug>/", views.BlogDetailView.as_view(), name="blog_detail"),
    path("blogs", views.BlogsView.as_view(), name="blogs-list"),
    path("search_blogs", views.SearchBlogsAPI.as_view(), name="search_blogs"),
    path(
        "latest-blogs-list", views.LatestBlogsView.as_view(), name="latest-blogs-list"
    ),
]
