from django.urls import path

from .views import *

app_name = "siteinfo"


urlpatterns = [
    path(
        "stats/",
        AboutUsStatsAPI.as_view(),
        name="stats",
    )
]
