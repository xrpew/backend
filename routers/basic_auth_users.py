import secrets
from fastapi import FastAPI, Depends, status, HTTPException, Header
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm


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
        #print("autenticar")
        return User(**users_db[username]) 



async def current_user(token:str = Depends(oauth2)):
    user = search_user(token)
    print(token)
    #if not user:
    #    print('not')
    #    raise HTTPException(
    #       status_code=status.HTTP_401_UNAUTHORIZED, 
     #       detail="Credenciales de autenticación inválidas",
     #       headers={"WWW-Authenticate":"Bearer"})

    #if user.disabled:
    #    raise HTTPException(
     #       status_code=status.HTTP_400_BAD_REQUEST, 
     #       detail="USUARIO INACTIVO",
     #       headers={"WWW-Authenticate":"Bearer"})

    #return user 



#@app.get('/user/bearer')


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
        pass
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Incorrect email or password",
        #     headers={"WWW-Authenticate": "Basic"},
        # )

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





def read_current_username(username:str = Depends(basic_current_username)):
    return username

def basic_user():
    return 'Usuario básico desde la función externa'

def bearer_user():
    return 'Usuario Bearer desde la función externa'

@app.get("/user/me")
def read_items(www_authenticate: str | None = Header(default=None)):
    if www_authenticate == 'Basic':
        #username = read_current_username()
        username = basic_user()
        return username
        #return 'basic_test'

    # if www_authenticate == 'Bearer':
    #     username = bearer_user()
    #     return username


@app.get("/user/mee")
def read_current_user(username: str = Depends(basic_current_username)):
    return username