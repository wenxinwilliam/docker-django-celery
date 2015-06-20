import asyncio
from aiohttp import web
import aioamqp
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
    # print(request.app['sockets'])

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


def callback_wrapper(ws_sockets):
    @asyncio.coroutine
    def callback(body, envelope, properties):
        for socket in ws_sockets:
            socket.send_str('amqp: {}'.format(body))
    return callback


@asyncio.coroutine
def receive(ws_sockets):
    try:
        transport, protocol = yield from aioamqp.connect(
            host=os.environ.get('RABBIT_PORT_5672_TCP_ADDR', '192.168.59.103'),
            port=int(os.environ.get('RABBIT_PORT_5672_TCP_PORT', 5672)),
            login=os.environ.get('RABBIT_ENV_USER', 'admin'),
            password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'password'),
        )
    except Exception as e:
        print("closed connections")
        return

    channel = yield from protocol.channel()
    exchange = yield from channel.exchange_declare(exchange_name='ws_msg.exchange', type_name='direct')
    queue_name = 'ws_msg'

    yield from channel.queue_declare(queue_name)
    yield from channel.queue_bind(queue_name, 'ws_msg.exchange', 'ws_msg')

    # yield from asyncio.wait_for(channel.queue(queue_name, durable=False, auto_delete=False), timeout=10)
    yield from asyncio.wait_for(channel.basic_consume(queue_name, callback=callback_wrapper(ws_sockets)), timeout=10)



@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app['sockets'] = []
    app.router.add_route('GET', '/echo', wshandler)
    app.router.add_route('GET', '/sleep/{seconds}', sleep_handler)
    app.router.add_route('GET', '/{name}', handle)

    srv = yield from loop.create_server(
        app.make_handler(),
        '0.0.0.0', 8000
    )
    print("async server started at http://0.0.0.0:8000")

    loop.create_task(ws_ping(app['sockets'], 2))

    return srv, app


loop = asyncio.get_event_loop()
srv, app = loop.run_until_complete(init(loop))
loop.run_until_complete(receive(app['sockets']))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()