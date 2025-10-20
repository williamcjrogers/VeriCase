from celery import Celery
from .config import settings

celery_app = Celery("vericase-docs", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
# The actual task is defined in the worker container under worker_app.worker.ocr_and_index
# We will call it by name from the API.
