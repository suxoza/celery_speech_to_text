import os
from celery import Celery

simple_app = Celery('simple_worker',
                    broker=f"amqp://{os.environ.get('RABBITMQ_DEFAULT_USER')}:{os.environ.get('RABBITMQ_DEFAULT_PASS')}@rabbitmq:5672",
                    backend='mongodb://mongo_server:27017/test_db')