import datetime
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import MetaData, DateTime, String, Column, Integer, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from database import engine
Base = declarative_base()
Base.metadata = MetaData()


class Holiday(Base):
    __tablename__ = "Holiday"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    type = Column(String, nullable=True)
    info = Column(String, nullable=True)


class HolidayBase(BaseModel):
    year: Optional[int] = None
    month: Optional[str] = None
    number: Optional[int] = None
    type: Optional[str] = None
    info: Optional[str] = None


class HolidayError(HolidayBase):
    status: Optional[int] = None
    msg: Optional[str] = None


class HolidayPost(BaseModel):
    year: int
    month: str
    number: int
    type: Optional[str] = None
    info: Optional[str] = None

