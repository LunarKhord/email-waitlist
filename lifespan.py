from fastapi import FastAPI
from contextlib import asynccontextmanager
from supabase import create_client


from dotenv import load_dotenv
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL environment variable is not set.")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY environment variable is not set.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.superbase  = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client created successfully")

    except Exception as e:
        logger.error(f"Error during lifespan startup: {e}")
        raise e 
    yield