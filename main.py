from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import jwt
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import uvicorn

app = FastAPI()

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myClient["python_dev"]
users = db['users']

user = {"_id": 1,"email": "thang.pc@beetechsoft.com", "password": "123456"}
users.insert_one(user)

class User(BaseModel):
    email: str
    password: str


@app.post('/login')
def login(item: User, response: Response):
    user = users.find_one({"email": item.email})
    if user != None:
        data = jsonable_encoder(user)
        if user['password'] == item.password:
            encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            response.status_code = status.HTTP_200_OK
            return {'token': encoded_jwt}
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {'message': 'Login failed'}
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'status': 500,'message': 'Login failed'}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')