from db.user_db import UserInDB
from db.user_db import get_user, update_user
from models.user_model import UserIn, UserOut
import datetime
from fastapi import FastAPI
from fastapi import HTTPException

api = FastAPI()

##################Añadiendo politica de cors###########################
from fastapi.middleware.cors import CORSMiddleware
origins = ["http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
            "http://localhost", "http://localhost:8080",]
api.add_middleware(CORSMiddleware, allow_origins=origins,
        allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)
######################################################################

@api.post("/user/auth/")
async def user_auth(user_in: UserIn):
    user_in_db = get_user(user_in.userid)
    if user_in_db == None:
        raise HTTPException(status_code=404, 
                            detail = 'El Usuario No Existe')
    if user_in_db.password != user_in.password:
        return {'Autenticado': False}
    return {'Autenticado': True}
        
@api.get("/user/config/{userid}")
async def get_historial(userid: int):
    user_in_db = get_user(userid)
    if user_in_db == None:
        raise HTTPException(status_code=404, detail = 'El Usuario No Existe')
    user_out = UserOut(**(user_in_db.dict()))
    return user_out
    
@api.put("/user/config/update")
async def update_usuario(user_out: UserOut):
    user_in_db = get_user(user_out.userid)
    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    update_user(UserInDB(**(user_out.dict())))   
    return user_out