from aiohttp import web
import socketio
import json
import logging


class SocketIOManager:

    def __init__(self, app: web.Application):
        sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
        sio.attach(app)
        self.sio = sio

        @sio.on("disconnect")
        async def disconnect(sid):
            logging.info(sid + " disconnected")
