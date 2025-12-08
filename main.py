from fastapi import FastAPI, Depends, Request, HTTPException, status
from models.waitlist import WaitList
from configs.rabbit_mq import lifespan
from utils.is_valid_email import is_valid_email
from contextlib import asynccontextmanager
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict


from configs.database import get_async_db, async_engine, Base

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("[INFO]: Attempting connect Postgres database")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("[INFO]: Table and columns were created.")
        yield

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
async def join_waitlist(email_request_payload: WaitList, db_session:AsyncSession = Depends(get_async_db)) -> Dict:
    status = await is_valid_email(db_session, email_request_payload)
    return { "status": status }