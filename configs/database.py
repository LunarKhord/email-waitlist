import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from typing import AsyncGenerator
import logging
from sqlalchemy import exc

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("POSTGRES_URL")

if not DATABASE_URL:
	logger.critical("[FATAL] POSTGRES_URL environment variable is not set. Database connection cannot be established.")

try:
	# 1. Create Async Engine
	async_engine = create_async_engine(
		DATABASE_URL, 
		echo=True, 
		pool_size=100, 
		max_overflow=200, 
		isolation_level="REPEATABLE READ"
		)
	logger.info("[INFO]: Async database engine was created.")

	# 2. Create Async Session FACTORY (using async_sessionmaker is the preferred way)
	AsyncSessionLocal = async_sessionmaker(
		bind=async_engine, 
		class_=AsyncSession,
		# Keep autocommit/autoflush off to enforce explicit commit/rollback for safety
		autocommit=False, 
		autoflush=False,
		expire_on_commit=False,
		)
	# 3. Declare a Base
	Base = declarative_base()

	# 4. Dependency injection: Get a new session instance for each request
	async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
		# Get a new session from the factory
		db = AsyncSessionLocal() 
		logger.info("[INFO]: Injection DB Session called")
		try:
			# Yield the session to the dependent function (e.g., a FastAPI route)
			yield db
		except exc.SQLAlchemyError as e:
			# Rollback if an error occurs within the dependency or before the commit is called
			await db.rollback()
			raise e
		finally:
			# Ensure the session is always closed after use
			await db.close()

except Exception as e:
	logger.error(f"An error occurred during database setup: {e}")
	# Re-raise or handle appropriately
	raise e