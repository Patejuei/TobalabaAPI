from fastapi import FastAPI
from routes.items import items
from routes.personal import personal
from routes.tesoreria import cash

app = FastAPI()

app.include_router(items)
app.include_router(personal)
app.include_router(cash)


@app.get("/")
async def root():
    return {"message": "Hello World"}
