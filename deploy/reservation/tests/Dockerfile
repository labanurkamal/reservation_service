FROM python:3.10-slim

WORKDIR /opt/app

ENV PYTHONPATH="/opt/app/tests"

COPY reservation/tests/requirements.txt requirements.txt

RUN pip install --upgrade pip --no-cache-dir \
    && pip install --no-cache-dir -r requirements.txt

COPY reservation/tests/ tests

CMD ["pytest", "-v", "tests"]