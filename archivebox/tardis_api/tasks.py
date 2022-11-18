from core.celery import app
from tardis_api.services.archiver import Archiver


@app.task(name='create_archive_task', max_retries=None)
def create_archive_task(url: str) -> dict:
    snapshot = Archiver().archive(url=url)
    if not snapshot:
        data = None
    else:
        data = snapshot.archive_path
    return {'data': data}
