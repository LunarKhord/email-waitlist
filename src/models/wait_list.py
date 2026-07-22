from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class WaitList(BaseModel):
    name: str = Field(..., description="Name of the business", examples=["My Business"])
    email:EmailStr = Field(..., description="Email of interested user", examples=["somethingraw@gmail.com"])
    company_size: str = Field(..., description="Size of the company", examples=["1-10", "11-50", "51-200", "201-500", "501-1000", "1001+"])
    current_tool: Optional[str] = Field(None, description="Current invoice tool used by the business", examples=["QuickBooks", "FreshBooks", "Xero"])
