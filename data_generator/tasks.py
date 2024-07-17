from celery import Celery
import random
import requests
import yaml


REQUEST_HEADERS = {'accept': 'application/json', 'Content-Type': 'application/json'}

app = Celery('tasks', broker='amqp://localhost')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, generate_data.s(), name='generate data every 30s')

@app.task
def generate_data():
    with open('config.yaml', 'r') as file:
        file_data = yaml.load(file, Loader=yaml.SafeLoader)
    device_list = file_data["device_list"]
    for device_name in device_list:
        url = f"http://api-server:8000/v1/devices/{device_name}/velocity_data" \
              f"?vibration_velocity={random.randrange(1, 6, 1)}"
        try:
            requests.post(url, headers=REQUEST_HEADERS, json={})
        except Exception as e:
            print(f"Exception {e=}")
    return
