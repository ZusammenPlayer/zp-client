from aiohttp import web

def setup(app: web.Application, conf):
    app.router.add_get("/", index_handler)
    app.router.add_static("/", conf["zp-client"]["web-path"], show_index=True, follow_symlinks=True)
    app.router.add_get('/{tail:(?!api).*}', index_handler)


async def index_handler(request):
    conf = request["conf"]
    with open(conf["zp-client"]["web-path"] + "/index.html") as f:
        html = f.read()
        return web.Response(text=html, content_type="text/html")
