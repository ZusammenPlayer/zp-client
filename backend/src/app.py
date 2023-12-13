import aiohttp
from aiohttp import web
from middlewares import socketio_middleware
from socketio_manager import SocketIOManager
import socketio
import config
import logging
import logging.handlers
import json


def setup_logging():
    log_file_name = config.log_dir_path + "/zp-client.log"
    formatter = logging.Formatter(
        "[%(levelname)s]%(asctime)s|%(filename)s - %(message)s"
    )
    handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when="midnight")
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


async def load_data(files_data):
    async with aiohttp.ClientSession() as session:
        # load current list of files
        # check with files_data and determine which files to download
        print("not implemented yet")


async def setup_socketio_client(sio_mngr: SocketIOManager):
    sio = socketio.AsyncClient()
    
    @sio.event
    async def updated(data):
        # this event is triggered by the hub in order to inform the client that we have new data
        print('message received with ', data)
        await sio.emit('player_status', {'response': 'progress or status or download finished'})
    
    @sio.event
    async def trigger(data):
        logging.info("dispatch hub event to client")
        await sio_mngr.sio.emit('trigger', data)
    
    @sio.event
    async def pause(data):
        logging.info("dispatch hub event to client")
        await sio_mngr.sio.emit('pause', data)
    
    await sio.connect('http://localhost:8080')
    logging.info('connected to zp-hub via socketio')

    register_data = {
        "type": "player",
        "uid": "p1",
        "name": "raspi 18 - Bühne vorne links",
    }
    await sio.emit('register', register_data)


async def init_app():
    setup_logging()

    # create web application
    app = web.Application()

    # init socketio - server component for communication with local frontend
    sio_mngr = SocketIOManager(app)

    app.middlewares.append(socketio_middleware(sio_mngr))

    # init socketio client for communication with zp-hub
    await setup_socketio_client(sio_mngr)

    # setup api handler
    return app


if __name__ == "__main__":
    web.run_app(init_app(), port=8090, access_log=None)
