import json

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from requests import codes

from tardis_api.services.archiver import Archiver
from util import URL_REGEX


@method_decorator(csrf_exempt, name='dispatch')
class CreateArchiveAPIView(View):

    archiver = Archiver()

    def post(self, request: HttpRequest) -> JsonResponse:
        url = json.loads(request.body).get('url')
        if not URL_REGEX.match(url):
            return JsonResponse(status=codes.bad_request, data={'result': 'Invalid url format'})

        snapshot = self.archiver.archive(url=url)
        if not snapshot:
            data = None
            status_code = codes.internal_server_error
        else:
            scheme = request.scheme
            host = request.get_host()
            data = f'{scheme}://{host}/{snapshot.archive_path}'
            status_code = codes.ok
        return JsonResponse(status=status_code, data={'result': data})
