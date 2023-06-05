from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_():
    return "API alpha version"

@app.get("/saludo")
def get_saludo():
    return {"mensaje": "¡Hola, mundo!"}
