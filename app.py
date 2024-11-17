from fastapi import FastAPI
from routes.items import items
from routes.personal import personal

app = FastAPI()

app.include_router(items)
app.include_router(personal)


@app.get("/")
async def root():
    return {"message": "Hello World"}
