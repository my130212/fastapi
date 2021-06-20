from typing import Optional
import uvicorn
from fastapi import FastAPI
from tutorial import app03,app04

app = FastAPI()

app.include_router(app03, prefix='/chapter03', tags=['第三章，请求参数与验证'])
app.include_router(app04, prefix='/chapter04', tags=['第三章，请求参数与验证'])

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
if __name__ == '__main__':
    uvicorn.run('main:app', host = '127.0.0.1',port = 8000, reload = True, debug = True, workers = 1)
