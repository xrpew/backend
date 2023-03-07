from fastapi import FastAPI, Header, Depends

app = FastAPI()


def basic_auth(value:str):
    return value


@app.get("/items/")
async def read_items(www_authenticate: str | None = Header(default=None)):
    if www_authenticate == 'Basic':
        return basic_auth('valor')

    if www_authenticate == 'Bearer':

        return {'WWW-Authenticate':www_authenticate}
