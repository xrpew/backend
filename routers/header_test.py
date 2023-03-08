import secrets
from fastapi import FastAPI, Depends, status, HTTPException, Header
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

security = HTTPBasic()

def verificar_autorizacion(authorization: str):
    if authorization is None:
        raise HTTPException(status_code=401, detail="No se encontró el encabezado de autorización")
    
    elif authorization.startswith("Bearer"):
        # Extraemos el valor del token de la cadena de encabezado de autorización
        token = authorization.split(" ")[1]
        # Aquí llamamos a la función para verificar el token de autenticación Bearer
        user = verificar_token(token)
        return {"Authorization Type": "Bearer", 'user':user}

    elif authorization.startswith("Basic"):
        username = authorization
        user = verificar_user(username)
        return {"Authorization Type": "Basic", 'user':user}
    
    else:
       raise HTTPException(status_code=401, detail="Tipo de autorización no válido")


def verificar_token(token:str):
    return token



def basic_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username
    current_password_bytes = credentials.password
    return current_username_bytes
    


def verificar_user(username: str = Depends(basic_current_username)):
    return username

@app.get("/user/me")
def read_user_me(authorization: str = Header(None)):
    resultado_autorizacion = verificar_autorizacion(authorization)
    return resultado_autorizacion