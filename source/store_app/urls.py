from django.urls import path
from store_app.views.base import index_view


urlpatterns = [
    path("", index_view)
]