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
    SUPABASE_URL = "https://vblydvoaercptwoudryp.supabase.co"
if not SUPABASE_KEY:
    SUPABASE_KEY = "sb_publishable_6MRue7UftVnBfafQAlzBVA_i1zmYKJM"

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.superbase =  supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client created successfully")

    except Exception as e:
        logger.error(f"Error during lifespan startup: {e}")
        raise e 
    yield