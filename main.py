from fastapi import FastAPI, Request
from src.models.wait_list import WaitList



app = FastAPI()


@app.get("/health")
async def wait_list_health():
    return {"status": "OK"}



@app.post("/api/v1/waitlist")
async def add_to_wait_list(payload: WaitList):
    pydantic_dump = payload.model_dump()
    print(pydantic_dump)