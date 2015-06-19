import asyncio
from aiohttp import web
import time
import os

WS_FILE = os.path.join(os.path.dirname(__file__), 'websocket-error.html')

@asyncio.coroutine
def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
def wshandler(request):
    resp = web.WebSocketResponse()
    
    ok, protocol = resp.can_start(request)
    if not ok:
        with open(WS_FILE, 'rb') as fp:
            return web.Response(body=fp.read(), content_type='text/html')

    resp.start(request)

    request.app['sockets'].append(resp)

    while True:
        msg = yield from resp.receive()

        if msg.tp == web.MsgType.text:
            resp.send_str("Hello, {}".format(msg.data))
        elif msg.tp == web.MsgType.binary:
            resp.send_bytes(msg.data)
        elif msg.tp == web.MsgType.close:
            request.app['sockets'].remove(resp)
            break

    return resp


@asyncio.coroutine
def ws_ping(sockets, seconds):
    while True:
        a = yield from asyncio.sleep(seconds)
        for socket in sockets:
            socket.send_str('websocket server ping')


@asyncio.coroutine
def sleep_handler(request):
    is_sync = request.GET.get('is_sync') == "1"
    seconds = int(request.match_info.get('seconds', 1))
    if seconds not in range(1,10):
        seconds = 1
    if is_sync:
        time.sleep(seconds)
    else:
        yield from asyncio.sleep(seconds)
    text = "Wake up after {} seconds".format(seconds)
    return web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app['sockets'] = []
    app.router.add_route('GET', '/echo', wshandler)
    app.router.add_route('GET', '/sleep/{seconds}', sleep_handler)
    app.router.add_route('GET', '/{name}', handle)

    srv = yield from loop.create_server(app.make_handler(),
                                        '0.0.0.0', 8000)
    print("Server started at http://0.0.0.0:8000")

    yield from ws_ping(app['sockets'], 2)
    return srv, app


loop = asyncio.get_event_loop()
srv, app = loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()