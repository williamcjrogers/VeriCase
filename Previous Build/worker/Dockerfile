FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# System deps for OCR
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    tesseract-ocr tesseract-ocr-eng     ghostscript qpdf poppler-utils     libsm6 libxext6 libxrender1     build-essential curl && rm -rf /var/lib/apt/lists/*

COPY worker/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY worker /code

CMD ["celery", "-A", "worker_app.worker", "worker", "--loglevel=INFO", "--concurrency=2"]
