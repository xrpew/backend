from fastapi import FastAPI
#from pydantic import BasModel

app = FastAPI()

#class User(BasModel)

@app.get('/users')
def users():
    return [{'name':'Sergio', 'surname':'xerpew', 'url':'xerpew.com'},
            {'name':'Alejandro', 'surname':'dev', 'url':'alejandro.com'},
            {'name':'Sergio', 'surname':'xerpew', 'url':'xerpew.com'}]

