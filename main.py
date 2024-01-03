from fastapi import FastAPI

app = FastAPI()


@app.get("/index")
def index():
    return {"Hello": "World"}

@app.get('/about')
def about():
    return "Ai Vision Project"


@app.get('/blog/{id}')
def getId(id : int):
    return {"data": id}