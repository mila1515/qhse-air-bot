from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
