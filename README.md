# Device Dashboard

## What it is

This application is a full stack solution to showcase the following technologies: Docker, PostgreSQL, Python, FastAPI (Python framework for API server), SQLAlchemy (SQL toolkit and ORM in Python), Pydantic (data parsing and validation in Python), Pandas (data manipulation and analysis in Python), Celery (task queue in Python), TypeScript (superset of JavaScript language), Angular (TypeScript-based web framework), Nginx (HTTP server) and OAuth 2.0 (authorization protocol).

The application is a dashboard that monitors the vibration velocity of devices. It is composed of 4 parts, each running inside a container, described below.

- PostgreSQL database, where all data is stored.
- The API server, implemented using FastAPI, SQLAlquemy, Pydantic, Pandas and OAuth 2.0 in Python. It is the only entity that connects to the database.
- The data generator, implemented using Celery in Python, that generates random device data and sends to the API server, simulating the behavior of devices. It only communicates with the API server.
- The web page frontend, implemented using Angular and hosted in a Nginx instance, that shows the device data. This web page only communicates with the API server.

Every 5 seconds, the data generator will create a random number, between 1 and 5 (this is the velocity data of the device), for each of devices "Device_01", "Device_02" and "Device_03" (or any name listed in the file "data_generator/config.yaml"), and send a POST request to the API server at path "/v1/devices/{device_name}/velocity_data" to add this velocity data in the DB.

The web page frontend has two pages: login and dashboard, shown in the images below. The dashboard page has two elements: a table of all devices with data present in the DB and a graph of the summed times of the data of these devices.

- Login page:

![login](https://github.com/user-attachments/assets/d3b41577-c35a-4ea6-b730-3552957894f8)

- Dashboard page:

![dashboard](https://github.com/user-attachments/assets/3481c3ce-ea27-4a16-8111-4c53db1202c6)

The dashboard table is updated every 5 seconds: each time, it is requested the list of devices with data present in the DB with a GET request to the API server at path "/v1/devices" and, for each device in the list, it is requested the latest data of the device with a GET request to the API server at "/v1/devices/{device_name}".

The dashboard graph is updated every 60 seconds: each time, it is requested the list of devices with data present in the DB with a GET request to the API server at path "/v1/devices" and, for each device in the list, it is requested the summed timeseries of the device with 1 minute resolution (the data entries are grouped in sets of 1 minute interval and then summed) with a GET request to the API server at "/v1/devices/{device_name}/timeseries" using the parameters "hours_since=1" (to get data since 1 hour ago) and "resolution=1". This summed timeseries is calculated using Pandas in the API server.

The API server access is protected by authentication: both the web page frontend and the data generator need to send an authentication token in each request. The OAuth 2.0 flow implemented in this application is the "password" flow: the client sends the username and password in a POST request to the API server at "/v1/auth/token" to get a token, to be used later in any request. To get more information about the user authenticated, a GET request with the token can be made to API server at path "/v1/auth/userinfo".

The documentation of this API can be found at http://localhost:8000/docs .

## How to use

Clone this repository and run `docker compose up` inside the repository folder (tested on Ubuntu 22.04.4 LTS with Docker Desktop 4.32.0 and Chrome 127.0.6533.88). When all containers are running, open a browser and access http://localhost:4200 . You will be redirected to the login screen. There are two users registered in the DB: you can either use user "user01" and password "password" or user "admin" and password "admin". Click in the "Login" button and the dashboard page should appear.

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
│   │       ├── auth.py        # Contains the authentication API endpoints implementation.
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
│   ├── deviceapp
│   │   ├── (...)              # The Angular project files.
│   ├── Dockerfile
│   └── nginx.conf             # The Nginx configuration file.
├── LICENSE
└── README.md
```
