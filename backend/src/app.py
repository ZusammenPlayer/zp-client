import aiohttp
from aiohttp import web
from middlewares import socketio_middleware, config_middleware
from socketio_manager import SocketIOManager
import socketio
import logging
import logging.handlers
import sys
import toml
import web_handler
import socket
import time


def read_conf():
    file_path = "/opt/zp-client/settings.toml"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    with open(file_path, "r") as f:
        return toml.load(f)


def setup_logging(conf):
    log_file_name = conf["zp-client"]["log-dir-path"] + "/zp-client.log"
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
        logging.info("not implemented yet")
        # simulate some delay until load data is implemented
        time.sleep(5)


async def setup_socketio_client(sio_mngr: SocketIOManager, conf):
    sio = socketio.AsyncClient()

    @sio.event
    async def connect():
        logging.info("connected to hub")
        register_data = {
            "type": "player",
            "uid": "p1",  # socket.gethostname(),
            "status": "ready",
        }
        await sio.emit("register", register_data)

    @sio.event
    def connect_error(data):
        logging.error("connecting to hub failed: " + str(data))

    @sio.event
    def disconnect():
        logging.info("disconnected from hub")

    @sio.event
    async def updated(data):
        # this event is triggered by the hub in order to inform the client that we have new data
        print("message received with ", data)
        await sio.emit(
            "player_status", {"response": "progress or status or download finished"}
        )

    @sio.event
    async def file_sync(data):
        logging.info("file sync event for project: " + data["project"]["name"])
        await sio.emit("device_status", {"status": "syncing"})
        await load_data(data["media"])
        await sio.emit("device_status", {"status": "ready"})

    @sio.event
    async def trigger(data):
        logging.info("dispatch hub event to client")
        await sio_mngr.sio.emit("trigger", data)

    @sio.event
    async def pause(data):
        logging.info("dispatch hub event to client")
        await sio_mngr.sio.emit("pause", data)

    await sio.connect(conf["zp-client"]["zp-hub-url"])


async def init_app():
    conf = read_conf()

    setup_logging(conf)

    # create web application
    app = web.Application()

    # init socketio - server component for communication with local frontend
    sio_mngr = SocketIOManager(app)

    app.middlewares.append(socketio_middleware(sio_mngr))
    app.middlewares.append(config_middleware(conf))

    # init socketio client for communication with zp-hub
    await setup_socketio_client(sio_mngr, conf)

    web_handler.setup(app, conf)

    # setup api handler
    return app


if __name__ == "__main__":
    web.run_app(init_app(), port=8090, access_log=None)
