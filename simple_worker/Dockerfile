FROM python:3.10-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt
ADD . /simple_worker
WORKDIR /simple_worker

ENTRYPOINT celery -A tasks worker --loglevel=info