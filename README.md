# SocketIOServer

## Table Of Contents

- [About the Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Socket Usage](#socket-usage)
- [TODO](#todo)

## About The Project

Socket Server to keep running to respond to clients (intended to be running on Raspberry Pi)

## Built With

SocketIO, aiohttp

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

- python 3.4+ (for asyncio)

### Installation

1. Download the script

2. Install dependencies

```sh
pip install python-socketio aiohttp
```

## Usage

Run app

```sh
python ./socket_server.py
```

### Socket Usage

Socket init

```py
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)
```

Events based socket server eg:

```py
@sio.on('data_request')
async def send_data(sid):
    # data = ...............
    await sio.emit('data', data)
```

Socket available at http://localhost:PORT

## TODO

Implement real Data and real events

For now random numbers are sent over to the client

```py
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

```

The data acquisition script is launched in a subprocess and when it's stopped the subprocess received a SIGTERM

```py
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
```
