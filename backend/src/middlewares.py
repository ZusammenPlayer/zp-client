from aiohttp.web import middleware
from socketio_manager import SocketIOManager


def socketio_middleware(sio_mngr: SocketIOManager):
    @middleware
    async def inner(request, handler):
        request["sio_mngr"] = sio_mngr
        return await handler(request)

    return inner
