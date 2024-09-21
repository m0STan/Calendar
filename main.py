import datetime
from typing import List, Type, Optional, Annotated
import uvicorn
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models.models import Holiday, HolidayBase, HolidayError, HolidayPost
from config import TOKEN
from script import day_parser


app = FastAPI(
    title="Производственный календарь"
)


@app.get("/get_days", response_model=List[HolidayBase])
def get_all_days(db: Session = Depends(get_db)):
    holidays = db.query(Holiday).all()
    results = []
    return holidays


@app.get("/get_day_info/{month}/{number}", response_model=HolidayError, response_model_exclude_none=True)
def get_day(month: str, number: int, db: Session = Depends(get_db)):
    db_day = db.query(Holiday).filter_by(month=month, number=number).one_or_none()
    if db_day:
        return db_day
    else:
        return {"status": 400, "msg": "Day not exist"}


@app.post("/update_day_info/", response_model=HolidayError, response_model_exclude_none=True)
def update_day(day: HolidayPost, db: Session = Depends(get_db)):
    db_day = db.query(Holiday).filter_by(month=day.month, number=day.number).one_or_none()
    if db_day:
        db_day.info = day.info
        db.commit()
        db.refresh(db_day)
        return db_day
    else:
        return {"status": 400, "msg": "Day not exist"}


@app.post("/add_day/", response_model=HolidayBase)
def add_day(day: HolidayPost, db: Session = Depends(get_db)):
    db_day = Holiday(year=day.year, month=day.month, number=day.number, type=day.type, info=day.info)
    db.add(db_day)
    db.commit()
    db.refresh(db_day)
    return db_day


@app.delete("/delete_day/{month}/{number}/", response_model=HolidayError, response_model_exclude_none=True)
def delete_day(month: str, number: int, db: Session = Depends(get_db)):
    db_day = db.query(Holiday).filter(Holiday.month == month and Holiday.number == number).first()
    db.delete(db_day)
    db.commit()
    return {"status": 200, "msg": "Successfully deleted"}


@app.get("/update_database/{token}/", )
def update_database(token: str, year: int = datetime.datetime.today().year, db: Session = Depends(get_db)):
    if token == TOKEN:
        db.query(Holiday).delete()
        db.commit()
        day_parser(year, db)
        return {"Status": "200"}
    else:
        return {"Status": "400", "msg": "Token is not acceptable"}


@app.get("/drop_database/{token}")
def drop_database(token, db: Session = Depends(get_db)):
    if token == TOKEN:
        db.query(Holiday).delete()
        db.commit()
        days = db.query(Holiday).all()
        return {"days": days}
    else:
        return {"Status": "400", "msg": "Token is not acceptable"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
