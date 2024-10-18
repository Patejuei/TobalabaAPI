from fastapi import FastAPI
from routes.items import items

app = FastAPI()

app.include_router(items)


@app.get("/")
async def root():
    return {"message": "Hello World"}
