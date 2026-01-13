from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from lifespan import lifespan

from src.models.wait_list import WaitList
from src.services.superbase_manager import save_to_db

from dotenv import load_dotenv
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

SUPERBASE_TABLE_NAME = os.getenv("SUPERBASE_TABLE_NAME")
if SUPERBASE_TABLE_NAME is None:
    SUPERBASE_TABLE_NAME = "waitlist"



origins = ["*"]


app = FastAPI(title="Email Waitlist", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def wait_list_health():
    return {"status": "OK"}



@app.post("/api/v1/waitlist")
async def add_to_wait_list(request: Request, payload: WaitList):
    pydantic_dump = payload.model_dump()
    superbase = request.app.state.superbase
    try:
        response = await save_to_db(superbase, SUPERBASE_TABLE_NAME, pydantic_dump)
        print(response)
        if response is True:
            return {"message": "Email was added to waitlist."}
    except Exception as e:
        return {"message": "Unable to save email, either exists or not valid email."}