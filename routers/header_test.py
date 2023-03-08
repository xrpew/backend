from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

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

def verificar_user(user:str):
    return user

@app.get("/users/me")
def read_user_me(authorization: str = Header(None)):
    resultado_autorizacion = verificar_autorizacion(authorization)
    return resultado_autorizacion