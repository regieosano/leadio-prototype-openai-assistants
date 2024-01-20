from fastapi import FastAPI
from routers import useraichat

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Leadio AI Assistant Prototype!!!"}


@app.get("/favicon.ico")
def favicon():
    return {"message": "Regie's Favicon!"}


app.include_router(useraichat.post_router)
