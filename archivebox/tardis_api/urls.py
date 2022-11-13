from django.urls import path

from tardis_api.view import CreateArchiveAPIView

urlpatterns = [
    path('archive/', CreateArchiveAPIView.as_view(), name='api-archive')
]
