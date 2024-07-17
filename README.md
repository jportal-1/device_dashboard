# Device Dashboard

## What it is

This application is a dashboard that monitors the vibration velocity of devices. It is a fully containerized solution composed by 4 parts, each one running inside a container:

- PostgreSQL database, where all data is stored.
- The API server, based on FastAPI, where the the device data requests are handled. It is the only entity that connects to the database.
- The data generator, that generates random device data and sends to the API server. It only communicates with the API server.
- The frontend, that is an instance of Grafana, that shows the device data. It only communicates with the API server.

## How to use

Clone this repository and run `docker compose up` inside the repository folder. When all containers are running, open a browser and access http://localhost:3000 , where is the login screen of Grafana. Click in the "Sign in with GitHub" button to log in using your GitHub account. On the left menu, click in "Dashboards" and after in "Device Acceleration Velocity Dashboard". The dashboard shown in the image below will appear. If there is no data, wait 1 minute and it should be updated.

![dashboard](https://github.com/user-attachments/assets/c2169a16-c084-42a8-9dfe-aff4f63e1983)

To allow further interaction with the system, the ports of the API server (number 8000) and the database (number 5432) are exposed outside the docker network. The API server documentation can be accessed at http://localhost:8000/docs .

## Folder structure

An explanation about the files of the repository is shown below.

```
.
├── api_server
│   ├── crud.py                # Contains helper methods to operate on the DB.
│   ├── database.py            # Contains the database connection data.
│   ├── Dockerfile
│   ├── __init__.py
│   ├── main.py                # Contains the FastAPI app.
│   ├── models.py              # Contains the SQLAlchemy database models.
│   ├── requirements.txt
│   ├── routers
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── devices.py     # Contains the devices API endpoints implementation.
│   │       └── __init__.py
│   └── schemas.py             # Contains the Pydantic models/schemas.
├── data_generator
│   ├── config.yaml            # Contains the list of devices to generate data.
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── start.sh               # Start script of data generator container.
│   └── tasks.py               # Contains the implementation of the periodic generation of random device data.
├── docker-compose.yaml
├── frontend
│   ├── Dockerfile
│   └── grafana_cfg
│       ├── grafana.db
│       └── grafana.ini
└── README.md
```

## Description of the API

An explanation about the API is shown below.

```
1) GET /v1/devices
   Gets the list of all devices with at least one data entry on the DB.
   Returns: the device list (list of strings).

2) GET /v1/devices/{device_name}
   Get the latest data of a specific device
   Parameters:
     - device_name: the device name (string).
   Returns: the device name (string), the vibration velocity (integer) and
            the timestamp of this data (time formatted string).

3) POST /v1/devices/{device_name}/velocity_data
   Add device velocity data to the DB.
   Parameters:
     - device_name: the device name (string).
     - vibration_velocity: the vibration velocity (integer).
   Returns: the same device name (string) and vibration velocity (integer),
            and also the timestamp of this data (time formatted string).

4) GET /v1/devices/{device_name}/timeseries
   Get a summed timeseries with the specified resolution.
   Parameters:
     - device_name: the device name (string).
     - hours_since: the number of hours before now to fetch device data (integer).
       Example: 2 means "fetch data from 2 hours ago to now".
       Note: restricted to values from 1 to 12.
     - resolution: the resolution in minutes (integer).
       Note: restricted to values from 1 to 60.
   Returns: a list of data points of UNIX timestamp (float) and velocity data (integer).
```

## License

MIT License

Copyright (c) 2024 João Victor Portal.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
