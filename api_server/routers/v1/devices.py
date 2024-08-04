from . import auth
from api_server import crud, database, schemas
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from pandas import DataFrame, Grouper
from sqlalchemy.orm import Session
from typing import Annotated


router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)

@router.get("", response_model=schemas.DeviceList,
            responses={401: {"description": "Unauthorized"}})
async def get_device_list(db: Annotated[Session, Depends(database.get_db)],
                          username: Annotated[str, Depends(auth.get_valid_user_from_token)]):
    device_list = crud.get_device_list(db=db)
    return schemas.DeviceList(device_list=device_list)

@router.get("/{device_name}", response_model=schemas.TimeSeriesEntry,
            responses={404: {"description": "Entry not found"},
                       401: {"description": "Unauthorized"}})
async def get_latest_device_data(device_name: str, db: Annotated[Session, Depends(database.get_db)],
                                 username: Annotated[str, Depends(auth.get_valid_user_from_token)]):
    entry = crud.get_latest_device_entry(db=db, device_name=device_name)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return schemas.TimeSeriesEntry(timestamp=entry.timestamp,
                                   device_name=entry.device_name,
                                   vibration_velocity=entry.vibration_velocity)

@router.post("/{device_name}/velocity_data", response_model=schemas.TimeSeriesEntry,
             responses={401: {"description": "Unauthorized"}})
async def add_device_velocity_data(device_name: str, vibration_velocity: int,
                                   db: Annotated[Session, Depends(database.get_db)],
                                   username: Annotated[str, Depends(auth.get_valid_user_from_token)]):
    new_entry = schemas.TimeSeriesEntry(timestamp=datetime.now(timezone.utc),
                                        device_name=device_name,
                                        vibration_velocity=vibration_velocity)
    created_entry = crud.create_timeseries_entry(db=db, entry=new_entry)
    return schemas.TimeSeriesEntry(timestamp=created_entry.timestamp,
                                   device_name=created_entry.device_name,
                                   vibration_velocity=created_entry.vibration_velocity)

@router.get("/{device_name}/timeseries", response_model=schemas.DataPointList,
            responses={400: {"description": "Bad Request"},
                       401: {"description": "Unauthorized"}})
async def get_summed_timeseries(device_name: str, hours_since: int,
                                resolution: int, db: Annotated[Session, Depends(database.get_db)],
                                username: Annotated[str, Depends(auth.get_valid_user_from_token)]):
    
    # Restricting values for hours_since and resolution.
    if not (0 < hours_since <= 12):
        raise HTTPException(status_code=400,
                            detail="The parameter hours_since is out of the valid range '0 < hours_since <= 12'.")
    if not (0 < resolution <= 60):
        raise HTTPException(status_code=400,
                            detail="The parameter resolution is out of the valid range '0 < resolution <= 60'.")
    
    entries = crud.get_device_entries(db=db, device_name=device_name,
                                      since=datetime.now(timezone.utc)-timedelta(hours=hours_since))

    data_points = schemas.DataPointList(data_point_list=[])
    if len(entries) > 0:

        # Sum timeseries using the informed resolution (in minutes).
        data = {"timestamp": [], "vibration_velocity": []}
        for entry in entries:
            data["timestamp"].append(entry.timestamp)
            data["vibration_velocity"].append(entry.vibration_velocity)
        dataframe = DataFrame(data)
        summed_dataframe = dataframe.groupby(Grouper(key="timestamp",
                                                     freq=f"{resolution}min",
                                                     origin=dataframe["timestamp"][0])).sum()

        # Transform the data in a format the frontend understands.
        for timestamp, series in summed_dataframe.iterrows():
            data_points.data_point_list.append({"x": timestamp.timestamp()*1000,
                                                "y": int(series["vibration_velocity"])})
        
        # Don't sent the last data point, as this data is still being summed.
        if len(data_points.data_point_list) > 0:
            data_points.data_point_list.pop()

        # Debug.
        #print(f"DEBUG:")
        #print(f"Inside method get_summed_timeseries:")
        #print(f"dataframe:")
        #print(f"{dataframe}")
        #print(f"summed_dataframe:")
        #print(f"{summed_dataframe}")
        #print(f"data_points:")
        #print(f"{data_points}")

    return data_points
