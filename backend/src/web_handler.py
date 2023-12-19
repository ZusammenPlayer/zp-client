from aiohttp import web
import json

def setup(app: web.Application, conf):
    app.router.add_get("/", index_handler)
    app.router.add_get('/media/{t}/{d}', get_media_file)
    app.router.add_static("/", conf["zp-client"]["web-path"], show_index=True, follow_symlinks=True)
    app.router.add_get('/{tail:(?!api).*}', index_handler)


async def index_handler(request):
    conf = request["conf"]
    with open(conf["zp-client"]["web-path"] + "/index.html") as f:
        html = f.read()
        return web.Response(text=html, content_type="text/html")

async def get_media_file(request):
    conf = request["conf"]

    with open(conf["zp-client"]["data-path"] + "/db.json", "r") as db_file:
        database = json.load(db_file)
        mime_type = None
        filename = None
        if request.match_info["t"] == "md5":
            for m in database["media"]:
                if m["md5"] == request.match_info["d"]:
                    mime_type = m["mime_type"]
                    filename = m["filename"]
        if request.match_info["t"] == "file":
            for m in database["media"]:
                if m["filename"] == request.match_info["d"]:
                    mime_type = m["mime_type"]
                    filename = m["filename"]

        if filename is not None and mime_type is not None:
            with open(conf["zp-client"]["data-path"] + "/" + filename, "rb") as media_file:
                return web.Response(body=media_file.read(), content_type=mime_type)
        else:
            return web.HTTPNotFound()
