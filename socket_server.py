from aiohttp import web
import asyncio
import socketio
import random
import time
import subprocess
from signal import SIGTERM, SIGINT

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)


@sio.on('connect')
def connect(sid, environ):
    print("connected: ", sid)


SEND_DATA = False


@sio.on('data_request')
async def send_data(sid):
    print("Sending data")
    global SEND_DATA
    SEND_DATA = True
    while(SEND_DATA):
        sensor_data = 100
        if (random.uniform(0, 1) > 0.5):
            sensor_data += random.uniform(0, 1) * 200
        else:
            sensor_data -= random.uniform(0, 1) * 200
        data = {
            'x': int(time.time() * 1000),
            'y': sensor_data
        }
        await sio.emit('data', data)
        await asyncio.sleep(5/1000)


@sio.on('data_request_stop')
async def stop_sending_data(sid):
    global SEND_DATA
    SEND_DATA = False
    print('stop sending data')


@sio.on('launch_script')
async def launch_script(sid):
    print("Launching script")
    global process
    process = subprocess.Popen(
        ["python", "cont_scan_csv.py"],
        shell=False)


@sio.on('kill_script')
async def kill_script(sid):
    print("Killing script")
    global process
    process.send_signal(SIGINT)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    web.run_app(app, host="0.0.0.0", port=8765)
