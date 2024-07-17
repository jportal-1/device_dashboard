FROM python:3.10.14-slim-bookworm

RUN apt-get -y update && apt-get install -y build-essential curl libpq-dev
COPY . /api_server
WORKDIR /api_server
RUN pip install -r requirements.txt

CMD ["fastapi", "run", "./main.py"]