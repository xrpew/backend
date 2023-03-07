from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password:str

users_db = {
    "sergiope":{
        'username':'sergiope',
        'full_name':'xerpew',
        'email':'sergio@mail.com',
        'disabled':False,
        'password':'$2a$12$1oKHIakUk.aU75281lnNjeep7zrXEEkmhfwdSlSbf7GUWP7x0hCc.'
    },
    "sergiope2":{
        'username':'sergiope2',
        'full_name':'xerpew2',
        'email':'sergio2@mail.com',
        'disabled':True,
        'password':'$2a$12$Bk1YQQEwHcQNARNxaFPvz.9MEFjeeJoAlzORtK1r5jxlefpvwRiSq'
    }
}

@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    user_db = users_db.get(form.username)
    if not user_db:
       raise HTTPException(
        status_code=404, detail=ERROR_ID)

    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=404, detail=ERROR_PW)
    return {"access_token": user.username, "token_type":"bearer"}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    #print('logro entrar')
    if username in users_db:
        #print("autenticar")
        return User(**users_db[username])
