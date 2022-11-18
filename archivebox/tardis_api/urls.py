from django.urls import path

from tardis_api.view import CreateArchiveAPIView, GetArchiveAPIView

urlpatterns = [
    path('archive/', CreateArchiveAPIView.as_view(), name='api-archive-post'),
    path('result/<str:task_id>/', GetArchiveAPIView.as_view(), name='api-archive-get')
]
