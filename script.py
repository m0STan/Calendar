import datetime
import json
import requests
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from models.models import Holiday
from database import get_db
from const import Naming
from calendar import monthrange


# Function for calendar db filling
def day_parser(year_calendar, db: Session = Depends(get_db)):
    json_url = f"https://xmlcalendar.ru/data/ru/{year_calendar}/calendar.json"

    # Getting json of holidays
    response = requests.get(json_url)
    days_dict = json.loads(response.content)

    # Restart "id" sequence and delete all rows
    db.execute(text("ALTER SEQUENCE \"Holiday_id_seq\" RESTART WITH 1"))
    db.commit()

    # Parser
    for month in days_dict["months"]:
        d = month["days"].replace("+", "").split(",")
        d = list(map(lambda x: int(x) if x == x.replace("*", "") else "!", d))
        while "!" in d:
            d.remove("!")
        for day in d:
            db_day = Holiday(year=days_dict["year"], month=Naming[month["month"]], number=int(day),
                             type="Выходной день")
            try:
                db.add(db_day)
                db.commit()
                db.refresh(db_day)
                print(db_day)
            except Exception as e:
                print(e)

    for month in Naming.values():
        month_number = list(Naming.values()).index(month) + 1
        for number in range(1, monthrange(days_dict["year"], month_number)[1]+1):
            db_day = db.query(Holiday).filter_by(month=month, number=number).one_or_none()
            if not db_day:
                db_day = Holiday(year=days_dict["year"], month=month, number=number, type="Рабочий день")
                try:
                    db.add(db_day)
                    db.commit()
                    db.refresh(db_day)
                    print(db_day)
                except Exception as e:
                    print(e)
