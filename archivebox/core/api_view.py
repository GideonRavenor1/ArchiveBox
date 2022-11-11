import json
import uuid
import os
from datetime import datetime, timezone
from pathlib import PosixPath
from typing import Optional

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from requests import codes

from index import Link
from main import add
from util import URL_REGEX


@method_decorator(csrf_exempt, name='dispatch')
class CreateArchiveAPIView(View):

    DIR = PosixPath(os.environ.get('OUTPUT_DIR'))
    input_kwargs = {
        'urls': '',
        'tag': '',
        'depth': 0,
        'parser': 'auto',
        'out_dir': DIR,
        'extractors': 'title,singlefile,pdf,screenshot',
        'return_only_new': True,
    }

    def post(self, request: HttpRequest) -> JsonResponse:
        url = json.loads(request.body).get('url')
        if not URL_REGEX.match(url):
            return JsonResponse(status=codes.bad_request, data={'result': 'Invalid url format'})

        snapshot = self.add_snapshot(url=url)
        if not snapshot:
            data = None
            status_code = codes.internal_server_error
        else:
            scheme = request.scheme
            host = request.get_host()
            data = f'{scheme}://{host}/{snapshot.archive_path}'
            status_code = codes.ok
        return JsonResponse(status=status_code, data={'result': data})

    def add_snapshot(self, url: str) -> Optional[Link]:
        timestamp = datetime.now(timezone.utc).isoformat('T', 'seconds')
        new_url = f'{url}#{timestamp}_{str(uuid.uuid4())}'
        return self._archive_snapshot(url=new_url)

    def _archive_snapshot(self, url: str) -> Optional[Link]:
        self.input_kwargs['urls'] = url
        result = add(**self.input_kwargs)
        current_snapshot = self._get_current_snapshot(result, url)
        return current_snapshot

    @staticmethod
    def _get_current_snapshot(result: list[Link], url: str) -> Optional[Link]:
        for model in result:
            if model.url == url:
                return model
        return None
