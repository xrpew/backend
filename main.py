from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/')
def root():
    return {'ok':'Home FastAPI'}
