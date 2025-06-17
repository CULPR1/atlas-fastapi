from utils.user_functions import *
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class ProfileLogin(BaseModel):
    user_id : str
    password : str
    name : str | None = None


class ProfileRegister(BaseModel):
    user_id : str
    password : str
    role : str
    name : str | None = None

class response(BaseModel):
    message : str
    role :str | None = None

class result(BaseModel):
    message : str


@app.post("/register", response_model = response,description = "registers a new user with user_id, password, role and name, no default values, role can be buyer or seller")
def register(details : ProfileRegister):
    message = register_user(details.user_id, details.password, details.role, details.name)
    return result(message=message)

@app.post("/login", response_model = response,description = "logs in a user with user_id and password, no default values, returns message and role if successful")
def login(details : ProfileLogin):
    message, role = login_user(details.user_id,details.password)
    return response(message=message, role=role)