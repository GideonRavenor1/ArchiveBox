import json
from typing import Optional

from celery.result import AsyncResult
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from requests import codes

from core.celery import app
from tardis_api.tasks import create_archive_task
from util import URL_REGEX


@method_decorator(csrf_exempt, name='dispatch')
class CreateArchiveAPIView(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        url = json.loads(request.body).get('url')
        if not URL_REGEX.match(url):
            return JsonResponse(status=codes.bad_request, data={'result': 'Invalid url format'})

        task = create_archive_task.delay(url=url)
        return JsonResponse(status=codes.ok, data={'task_id': task.id})


@method_decorator(csrf_exempt, name='dispatch')
class GetArchiveAPIView(View):

    def get(self, request: HttpRequest, task_id: str) -> JsonResponse:
        response = AsyncResult(id=task_id, app=app)
        if response.status == 'SUCCESS':
            task_data = response.get()
            data = self._convert_data(request=request, data=task_data)
        else:
            data = None
        return JsonResponse(status=codes.ok, data={'result': data, 'status': response.status})

    @staticmethod
    def _convert_data(request: HttpRequest, data: dict) -> Optional[str]:
        link = data.get('data')
        if link is not None:
            scheme = request.scheme
            host = request.get_host()
            link = f'{scheme}://{host}/{link}'
        return link
