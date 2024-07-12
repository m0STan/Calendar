import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import MetaData, DateTime, String, Column, Integer, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from database import engine
Base = declarative_base()
Base.metadata = MetaData()

# Days = Table(
#     "Days",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("year", Integer, nullable=False),
#     Column("month", String, nullable=False),
#     Column("number", Integer, nullable=False),
#     Column("type", String, nullable=False),
#     Column("info", String, nullable=True),
# )


class Holiday(Base):
    __tablename__ = "Holiday"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    type = Column(String, nullable=True)
    info = Column(String, nullable=True)


class HolidayBase(BaseModel):
    year: int
    month: str
    number: int
    type: str
    info: Optional[str] = None





# def create_tables():
#     engine.echo = False
#     metadata.drop_all(engine)
#     metadata.create_all(engine)
#     engine.echo = True

