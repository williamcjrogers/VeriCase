FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

# Install system dependencies including PST library
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    autoconf \
    automake \
    libtool \
    pkg-config \
    libssl-dev \
    gettext \
    autopoint \
    python3-dev \
    pst-utils \
    && rm -rf /var/lib/apt/lists/*

# Build and install libpff from source (required for pypff)
RUN git clone https://github.com/libyal/libpff.git /tmp/libpff && \
    cd /tmp/libpff && \
    ./synclibs.sh && \
    ./autogen.sh && \
    ./configure --enable-python PYTHON_VERSION=3.11 PYTHON=/usr/local/bin/python3 && \
    make && \
    make install && \
    ldconfig && \
    cd /tmp && rm -rf /tmp/libpff

# Copy requirements and install Python dependencies
COPY api/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy application code
COPY api/app /code/app
COPY api/alembic.ini /code/alembic.ini
COPY api/migrations /code/migrations

# Copy UI files for serving
COPY ui /code/ui

# Copy startup scripts
COPY start.sh /code/start.sh
COPY start.py /code/start.py
RUN chmod +x /code/start.sh /code/start.py

EXPOSE 8000
CMD ["python3", "/code/start.py"]
