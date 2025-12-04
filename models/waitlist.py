from pydantic import BaseModel, EmailStr, Field


"""
This module serves the purpose of validating the incoming email payload from the user
"""

class WaitList(BaseModel):
	email: EmailStr = Field(..., description="The email of the potential client or user.")
	industry: str = Field("null", description="The field of specialization")