from celery import Celery
import random
import requests
import yaml


app = Celery('tasks', broker='amqp://localhost')
token = ''

def get_token(username, password):
    url = f"http://api-server:8000/v1/auth/token"
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = f'grant_type=password&username={username}&password={password}&scope=&client_id=&client_secret='
    try:
        response = requests.post(url=url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            return None
    except Exception as e:
        print(f"Exception {e=}")
        return None

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, generate_data.s(), name='generate data every 5s')

@app.task
def generate_data():
    global token
    if token == '':
        token = get_token(username='admin', password='admin')
    with open('config.yaml', 'r') as file:
        file_data = yaml.load(file, Loader=yaml.SafeLoader)
    device_list = file_data["device_list"]
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {token}'}
    for device_name in device_list:
        url = f"http://api-server:8000/v1/devices/{device_name}/velocity_data" \
              f"?vibration_velocity={random.randrange(1, 6, 1)}"
        try:
            requests.post(url, headers=headers, json={})
        except Exception as e:
            print(f"Exception {e=}")
    return
