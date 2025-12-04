import httpx # Import httpx instead of requests

"""
This module serves the purpose of validating the passed in email by the prospect
"""

async def is_valid_email(email_payload) -> bool:
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
	print(response.json())

	# Example logic to return True/False based on the response
	if response.status_code == 200 and response.json().get("status") == "VALID":
		return True
	return False