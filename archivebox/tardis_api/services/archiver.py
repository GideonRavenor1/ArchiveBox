import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from index import Link
from main import oneshot

logger = logging.getLogger(__name__)


class Archiver:
    _input_kwargs = {
        'url': '',
        'extractors': 'title,singlefile,pdf',
        'return_link_obj': True,
        'timestamp_dir_name': True,
    }

    def archive(self, url: str) -> Optional[Link]:
        data = self._prepare_data(url=url)
        try:
            result = oneshot(**data)
        except Exception as error:
            logger.error(f'[tardis_api] Ошибка при архивации: {str(error)}')
            result = None
        return result

    def _prepare_data(self, url: str) -> dict:
        timestamp = datetime.now(timezone.utc).isoformat('T', 'seconds')
        self._input_kwargs['url'] = f'{url}#{timestamp}_{str(uuid.uuid4())}'
        return self._input_kwargs
