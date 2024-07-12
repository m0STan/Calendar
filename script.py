import json
import requests
from fastapi import Depends
from sqlalchemy.orm import Session
from models.models import Holiday
from database import get_db
from const import Naming

json_url = "https://xmlcalendar.ru/data/ru/2024/calendar.json"
response = requests.get(json_url)
days_dict = json.loads(response.content)


def day_parser(db: Session = Depends(get_db)):
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
