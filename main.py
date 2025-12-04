from fastapi import FastAPI
from models.waitlist import WaitList
from configs.rabbit_mq import lifespan
from utils.is_valid_email import is_valid_email

app = FastAPI(title="Waitlist", lifespan=lifespan)


"""
This endpoint serves the purpose
of return the current system or server health of the backend
"""
@app.get("/health")
async def health_check():
    return {"health": "OK"}


"""
This endpoint serves the purpose of collecting the email
entered by a user.
"""
@app.post("/api/v1/waitlist")
async def join_waitlist(email_request_payload: WaitList):
    status = await is_valid_email(email_request_payload)
    return { "status": status }