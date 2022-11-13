import uuid
from datetime import datetime, timezone

from main import oneshot


class Archiver:
    _input_kwargs = {
        'url': '',
        'extractors': 'title,singlefile,pdf,screenshot',
        'return_link_obj': True,
        'timestamp_dir_name': True,
    }

    def archive(self, url: str):
        data = self._prepare_data(url=url)
        return oneshot(**data)

    def _prepare_data(self, url: str) -> dict:
        timestamp = datetime.now(timezone.utc).isoformat('T', 'seconds')
        self._input_kwargs['url'] = f'{url}#{timestamp}_{str(uuid.uuid4())}'
        return self._input_kwargs
