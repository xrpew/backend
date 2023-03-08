import secrets
from fastapi import FastAPI, Depends, status, HTTPException, Header
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
import base64

app = FastAPI()

# OAuth
oauth2 = OAuth2PasswordBearer(tokenUrl='login')

# Basic
security = HTTPBasic()

# Mensajes ERROR constantes
ERROR_ID = {'error':'no existe usuario con ese id'}
ERROR_ID_EXIST = {'error':'ya existe usuario con ese id'}
ERROR_PW = {'error':'contraseña incorrecta'}

# Mensajes OK constantes
ADD_USER_OK = {'ok':'se agregó correctamente el usuario'}
UPDATE_USER_OK = {'ok':'se actualizó correctamente el usuario'}
DELETE_OK = {'ok':'se eliminó correctamente el usuario'}


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
        'password':'123456'
    },
    "sergiope2":{
        'username':'sergiope2',
        'full_name':'xerpew2',
        'email':'sergio2@mail.com',
        'disabled':True,
        'password':'1234562'
    }
}

@app.get('/user')
async def users():
    return users_db

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    #print('logro entrar')
    if username in users_db:
        print("autenticar")
        return User(**users_db[username]) 

@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    user_db = users_db.get(form.username)
    if not user_db:
       raise HTTPException(
        status_code=404, detail=ERROR_ID)
    user = search_user_db(form.username)
    
    if not form.password == user.password:
        raise HTTPException(
            status_code=404, detail=ERROR_PW)
    
    return {"access_token": user.username, "token_type":"bearer"}

def basic_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username
    current_password_bytes = credentials.password

    user = search_user_db(current_username_bytes)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    is_correct_username = secrets.compare_digest(
        current_username_bytes, user.username
    )
    is_correct_password = secrets.compare_digest(
        current_password_bytes, user.password
    )

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="USUARIO INACTIVO",
            headers={"WWW-Authenticate":"Basic"})

    return search_user(current_username_bytes)
    
def read_current_user(username: str = Depends(basic_current_username)):
    return username

def verificar_autorizacion(authorization: str):
    if authorization is None:
        raise HTTPException(status_code=401, detail="No se encontró el encabezado de autorización")

    elif authorization.startswith("Bearer"):
        token = authorization.split(" ")[1]
        user = search_user(token)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
            headers={"WWW-Authenticate": "Basic"},
        )
        if user.disabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="USUARIO INACTIVO",
                headers={"WWW-Authenticate":"Bearer"})

        return {"Authorization Type": "Bearer", 'user':user}

    elif authorization.startswith("Basic"):

        username = authorization
        user = read_current_user(username).split(' ')[1]
        userdec = base64.b64decode(user).decode('utf8').split(':')[0]
        pwdec = base64.b64decode(user).decode('utf8').split(':')[1]
        final_user = search_user_db(userdec)

        if not final_user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

        if final_user.password != pwdec:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        if final_user.disabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="USUARIO INACTIVO",
                headers={"WWW-Authenticate":"Basic"})

        return {"Authorization Type": "Basic", 'user':final_user}

    else:
       raise HTTPException(status_code=401, detail="Tipo de autorización no válido")

@app.get("/user/me")
def read_user_me(authorization: str = Header(None)):
    resultado_autorizacion = verificar_autorizacion(authorization)
    return resultado_autorizacion