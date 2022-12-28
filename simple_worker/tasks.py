import time, os, base64
from celery import Celery
from celery.utils.log import get_task_logger
import speech_recognition as sr
from io import StringIO, BytesIO
logger = get_task_logger(__name__) 

app = Celery('tasks',
             broker=f"amqp://{os.environ.get('RABBITMQ_DEFAULT_USER')}:{os.environ.get('RABBITMQ_DEFAULT_PASS')}@rabbitmq:5672",
             backend='mongodb://mongo_server:27017/test_db')

@app.task()
def speech_to_text(file_name):
    _file = BytesIO(base64.b64decode(file_name.encode(encoding = 'utf-8')))
    r = sr.Recognizer()
    with sr.AudioFile(_file) as source:
        audio = r.record(source)
        try:
            return r.recognize_google(audio)
        except Exception as e:
            print("Exception: "+str(e))

