FROM python:3.10-alpine

RUN apk add --update \
    --virtual build-dependencies \
    bash \
    postgresql-dev \
    musl-dev \
    python3-dev \
    git \
    curl-dev \
    jpeg-dev \
    libressl-dev \
    libffi-dev \
    gcc \
    g++ \
    libxslt-dev

WORKDIR /app
COPY . /app/

# Set environment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/app"

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
