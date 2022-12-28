import os
import logging
from threading import Thread

from fastapi import FastAPI, Body, Depends, UploadFile, HTTPException
from src.celery_instance import simple_app
from src.auth import auth, JWTBearer
from src.schemas import UserLoginSchema
import base64

log = logging.getLogger(__name__)

app = FastAPI()


@app.post("/user/login")
async def user_login(user: UserLoginSchema = Body(...)):
    if auth.check_user(user):
        return auth.signJWT(user.user)
    return {"error": "Wrong login details!"}

@app.post("/upload_file/", dependencies=[Depends(JWTBearer())])
async def upload_file(file: UploadFile):
    if file.content_type not in ['audio/wav']:
        raise HTTPException(400, detail="Invalid File Format")

    byte = base64.b64encode(file.file.read())
    task = simple_app.send_task('tasks.speech_to_text', kwargs={'file_name': byte.decode('utf-8')})
    
    return task.id

@app.get('/get_status/{task_id}', dependencies=[Depends(JWTBearer())])
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    return {"message": "Status of the Task " + str(status.state)}


@app.get('/get_result/{task_id}', dependencies=[Depends(JWTBearer())])
def task_result(task_id):
    result = simple_app.AsyncResult(task_id)
    return {"message": "Result of the Task " + str(result.result)}
