from fastapi import FastAPI
from pydantic import BasModel

app = FastAPI()

class User(BasModel)

@app.get('/users')
def users():
    return {'msg':'hola users'}

