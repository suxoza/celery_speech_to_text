
from typing import Dict
import time
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

JWT_SECRET = '0c504602e917945b83d12e78076f41a2692d28c16fcd66ae' # some random string
JWT_ALGORITHM = 'HS256'


users = [
    {'id': 1, 'user': 'paliko', 'password': 'some_simple_password'},
    {'id': 2, 'user': 'shaliko', 'password': 'some_simple_password'},
    {'id': 3, 'user': 'john', 'password': 'some_simple_password'},
]

class auth:
    @staticmethod
    def signJWT(user_id: str) -> Dict[str, str]:
        payload = {
            "user_id": user_id,
            "expires": time.time() + 600
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {"access_token": token}

    @staticmethod
    def decodeJWT(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except BaseException as e:
            return {"error": str(e)}

    @staticmethod
    def check_user(data):
        return len([user for user in users if user['user'] == data.user and user['password'] == data.password]) == 1
    


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = auth.decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid