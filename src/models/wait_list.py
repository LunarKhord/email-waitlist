from pydantic import BaseModel, EmailStr, Field



class WaitList(BaseModel):
    email:EmailStr = Field(..., description="Email of interested user", examples=["somethingraw@gmail.com"])