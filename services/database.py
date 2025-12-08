from schemas.waitlist import WaitList
from configs.database import get_async_db
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Save the email into the database
async def commit_email(db_session: AsyncSession, email_payload: Dict) -> bool:
	logger.info("[INFO]: Commit Email Async Function called.")
	try:
		payload = {}
		payload["email"] = email_payload.get("email")
		
		if payload.get("industry"):
			payload["industry"] = email_payload.get("industry")
		
		new_waitlist_user = WaitList(**payload)
		
		# Add the new user waitlist instance or object
		db_session.add(new_waitlist_user)
		await db_session.flush()

		await db_session.commit()
		logger.info("[INFO]: Transaction committed successfully.")
		return True
		logger.info("[INFO]: New User was added to the waitlist.")
	except Exception as e:
		logger.critical(f"[critical]: An Error occurd: {e}")
		raise
	