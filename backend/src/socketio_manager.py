from aiohttp import web
import socketio
import logging


class SocketIOManager:

    def __init__(self, app: web.Application):
        sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
        sio.attach(app)
        self.sio = sio

        @sio.on("connect")
        async def connect(sid, data):
            logging.info('frontend connected: ' + sid)

        @sio.on("disconnect")
        async def disconnect(sid):
            logging.info(sid + " disconnected")
