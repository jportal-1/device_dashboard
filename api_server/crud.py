# This file contains the Create, Read, Update and Delete operations on DB.

from . import models, schemas
from datetime import datetime
from sqlalchemy.orm import Session


def get_device_list(db: Session):
    query = db.query(models.TimeSeriesEntryDB.device_name).distinct().all()
    device_list = []
    for row in query:
        device_list.append(row[0])
    device_list.sort()
    return device_list

def get_latest_device_entry(db: Session, device_name: str):
    return db.query(models.TimeSeriesEntryDB) \
             .filter(models.TimeSeriesEntryDB.device_name == device_name) \
             .order_by(models.TimeSeriesEntryDB.timestamp.desc()) \
             .first()

def create_timeseries_entry(db: Session, entry: schemas.TimeSeriesEntry):
    db_entry = models.TimeSeriesEntryDB(timestamp=entry.timestamp, device_name=entry.device_name, vibration_velocity=entry.vibration_velocity)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_device_entries(db: Session, device_name: str, since: datetime):
    query = db.query(models.TimeSeriesEntryDB) \
              .filter(models.TimeSeriesEntryDB.device_name == device_name, models.TimeSeriesEntryDB.timestamp >= since) \
              .order_by(models.TimeSeriesEntryDB.timestamp.asc()) \
              .all()
    return query

def add_user_entry(db: Session, username: str, hashed_password: str):
    db_entry = get_user_entry(db=db, username=username)
    if db_entry is None:
        db_entry = models.UserEntryDB(username=username, hashed_password=hashed_password)
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
    else:
        db_entry.hashed_password = hashed_password
        db.commit()
        db.refresh(db_entry)
    return db_entry

def get_user_entry(db: Session, username: str):
    return db.query(models.UserEntryDB) \
             .filter(models.UserEntryDB.username == username) \
             .first()
