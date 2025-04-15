FROM python:3.10-slim

USER root

WORKDIR /opt/app

ENV PYTHONDONTWRITECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PYTHONPATH="/opt/app/src"

COPY reservation/requirements.txt requirements.txt

RUN pip install --upgrade pip --no-cache-dir \
    && pip install --no-cache-dir -r requirements.txt

COPY deploy/reservation/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY reservation/ .

ENTRYPOINT ["/entrypoint.sh"]

