from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone


from configs.database import Base


"""This module, defines the Schema and or fields that the table will contain as colums with restrictions"""


class WaitList(Base):
	__tablename__ = "waitlist"
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	email = Column(String(512), index=True, unique=True, nullable=False)
	industry = Column(String(512), index=True, unique=False, nullable=True)
	createdAt = Column(DateTime(timezone=True), default=func.now())
