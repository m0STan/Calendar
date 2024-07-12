import datetime
from calendar import monthrange
from typing import List, Type, Optional, Annotated
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session, Query
from database import get_db
from models.models import Holiday, HolidayBase
from config import TOKEN
from script import day_parser
from const import Naming

app = FastAPI(
    title="Производственный календарь"
)


@app.get("/get_days", response_model=List[HolidayBase])
def get_all_days(db: Session = Depends(get_db)):
    holidays = db.query(Holiday).all()
    results = []
    return holidays


@app.get("/get_day_info/{month}/{number}")
def get_day(month: str, number: int, db: Session = Depends(get_db)):
    db_day = db.query(Holiday).filter_by(month=month, number=number).one_or_none()
    if not db_day and month in Naming.items() and number <= monthrange(datetime.date.today().year, Naming.keys()[list(Naming.values().index(month))])[1]:
        return {
            "year": datetime.date.today().year,
            "number": number,
            "type": "Рабочий день",
            "month": month
        }
    elif db_day:
        return db_day
    else:
        return {"status": 400, "Error": "Неккоректные данные"}


@app.post("/update_day_info/{month}/{number}", response_model=HolidayBase)
def update_day(month: str, number: int, info: str = None, db: Session = Depends(get_db)):
    db_day = db.query(Holiday).filter_by(month=month, number=number).one_or_none()
    if db_day:
        db_day.info = info
        db.commit()
        db.refresh(db_day)
        return db_day


@app.post("/add_day/{year}/{month}/{number}")
def add_day(year: int, month: str, number: int, type: str, info: str, db: Session = Depends(get_db)):
    db_day = Holiday(year=year, month=month, number=number, type=type, info=info)
    db.add(db_day)
    db.commit()
    db.refresh(db_day)
    return {"Code": "Successfully added", "Day": db_day}


@app.delete("/delete_day/{month}/{number}/")
def delete_day(month: str, number: int, db: Session = Depends(get_db)):
    db_day = db.query(Holiday).filter(Holiday.month == month and Holiday.number == number).first()
    db.delete(db_day)
    db.commit()
    return {"Code": "Successfully deleted", "Day": db_day}


@app.get("/update_database/{token}")
def update_database(token, db: Session = Depends(get_db)):
    if token == TOKEN:
        db.query(Holiday).delete()
        db.commit()
        day_parser(db)
        return {"Status": "200"}
    else:
        return {"Status": "400", "Error": "Token is not acceptable"}


@app.get("/drop_database/{token}")
def drop_database(token, db: Session = Depends(get_db)):
    if token == TOKEN:
        db.query(Holiday).delete()
        db.commit()
        days = db.query(Holiday).all()
        return {"days": days}
    else:
        return {"Status": "400", "Error": "Token is not acceptable"}


if __name__ == "__main__":
    uvicorn.run(app)
