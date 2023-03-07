from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Iniciar el server: uvicorn users:router --reload
router = APIRouter(tags=['users'], prefix='/user')

# Entidad user con BaseModel
class User(BaseModel):
    id:int
    name: str
    surname: str
    url: str
    age: int

# Mensajes ERROR constantes
ERROR_ID = {'error':'no existe usuario con ese id'}
ERROR_ID_EXIST = {'error':'ya existe usuario con ese id'}

# Mensajes OK constantes
ADD_USER_OK = {'ok':'se agregó correctamente el usuario'}
UPDATE_USER_OK = {'ok':'se actualizó correctamente el usuario'}
DELETE_OK = {'ok':'se eliminó correctamente el usuario'}

#users = [User('Sergio','xerpew','xerpew.com', 35)]
users_list = [User(id=1,name='Sergio', surname='xerpew', url='xerpew.com', age=34),
            User(id=2,name='Alejandro', surname='dev', url='alejandro.com', age=34),
            User(id=3,name='Sergio', surname='xerpew', url='xerpew.com', age=34)]


@router.get('/all')
async def user():
    return users_list

# Path
@router.get('/{id}')
async def user(id: int):
    try:
        return search_user(id)
    except:
        raise HTTPException(status_code=404, detail=ERROR_ID)

# Query
@router.get('/')
async def user_query(id: int):
    return search_user(id)

# Agregando usuarios
@router.post('/', status_code=201)
async def add_user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail=ERROR_ID_EXIST)
       # return ERROR_ID_EXIST
    else:
        users_list.append(user)
        return user, ADD_USER_OK

# Actualización de usuarios
@router.put('/')
async def update_user(user:User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index]= user
            found = True
            return user, UPDATE_USER_OK

    if not found:
        raise HTTPException(status_code=404, detail=ERROR_ID)
       # return ERROR_ID

# Eliminación de usuarios
@router.delete('/{id}')
async def delete_user(id:int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return DELETE_OK

    if not found:
        raise HTTPException(status_code=404, detail=ERROR_ID)
        #return ERROR_ID

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return ERROR_ID
