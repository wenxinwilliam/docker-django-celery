import asyncio
from aiohttp import web
import time


@asyncio.coroutine
def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
def wshandler(request):
    ws = web.WebSocketResponse()
    ws.start(request)

    while True:
        msg = yield from ws.receive()

        if msg.tp == web.MsgType.text:
            ws.send_str("Hello, {}".format(msg.data))
        elif msg.tp == web.MsgType.binary:
            ws.send_bytes(msg.data)
        elif msg.tp == web.MsgType.close:
            break

    return ws

@asyncio.coroutine
def sleep_handler(request):
    seconds = int(request.match_info.get('seconds', 1))
    if seconds not in range(1,10):
        seconds = 1

    yield from asyncio.sleep(seconds)
    text = "Wake up after {} seconds".format(seconds)
    return web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/echo', wshandler)
    app.router.add_route('GET', '/sleep/{seconds}', sleep_handler)
    app.router.add_route('GET', '/{name}', handle)

    srv = yield from loop.create_server(app.make_handler(),
                                        '0.0.0.0', 8000)
    print("Server started at http://0.0.0.0:8000")
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()