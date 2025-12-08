import httpx
from typing import Dict
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from services.database import commit_email
"""
This module serves the purpose of validating the passed in email by the prospect
"""

async def is_valid_email(db_session:AsyncSession, email_payload: Dict) -> bool:
	# 1. Extract the dictionary and the email value
	email_payload_dict = email_payload.model_dump()
	email = email_payload_dict.get("email")

	# 2. Use httpx for asynchronous requests
	async with httpx.AsyncClient() as client:
		# 3. Use the 'params' argument for GET query parameters
		response = await client.get(
			"https://rapid-email-verifier.fly.dev/api/validate",
			params={"email": email} # CRITICAL FIX: Use 'params'
		)

	# Check the status and content
	print(type(response.json()))
	email_payload = response.json()

	# Example logic to return True/False based on the response
	if response.status_code == 200 and response.json().get("status") == "VALID":
		await commit_email(db_session, email_payload)
		return True
	return False

