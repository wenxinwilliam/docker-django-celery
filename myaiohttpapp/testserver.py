import asyncio
from aiohttp import web
import asynqp
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
def setup_connection(loop):
    print('s')
    # connect to the RabbitMQ broker
    connection = yield from asynqp.connect(
        os.environ.get('RABBIT_PORT_5672_TCP_ADDR', '127.0.0.1'),
        int(os.environ.get('RABBIT_PORT_5672_TCP_PORT', 5672)),
        username=os.environ.get('RABBIT_ENV_USER', 'admin'),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'password'),
    )
    return connection


@asyncio.coroutine
def on_receive_wrapper(ws_sockets):
    def on_receive(msg):
        for socket in ws_sockets:
            socket.send_str('amqp: {}'.format(msg))
    return on_receive


@asyncio.coroutine
def setup_consumer(connection, channels, ws_sockets):
    print('s')
    # callback will be called each time a message is received from the queue

    _, queue = yield from setup_exchange_and_queue(connection, channels)

    # connect the callback to the queue
    consumer = yield from queue.consume(on_receive_wrapper(ws_sockets))
    return consumer


@asyncio.coroutine
def setup_exchange_and_queue(connection, channels):
    print('s')
    # Open a communications channel
    channel = yield from connection.open_channel()

    # Create a queue and an exchange on the broker
    # exchange = yield from channel.declare_exchange('ws_msg.exchange', 'direct')
    queue = yield from channel.declare_queue('ws_msg')

    # Save a reference to each channel so we can close it later
    channels.append(channel)

    # Bind the queue to the exchange, so the queue will get messages published to the exchange
    yield from queue.bind(exchange, 'ws_msg')

    return exchange, queue


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

    loop.create_task(ws_ping(app['sockets'], 2))

    connection = yield from setup_connection(loop)
    channels = []
    consumer = yield from setup_consumer(connection, channels, app['sockets'])

    return srv, app


loop = asyncio.get_event_loop()
srv, app = loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()