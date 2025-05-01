# server.py
import asyncio
import websockets
import aiohttp
from aiohttp import web

connected_clients = set()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    connected_clients.add(ws)
    print("Új kliens csatlakozott")

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            for client in connected_clients:
                if client != ws:
                    await client.send_str(msg.data)
        elif msg.type == web.WSMsgType.ERROR:
            print(f'Hiba a websocket kapcsolatban: {ws.exception()}')

    connected_clients.remove(ws)
    print("Kliens lecsatlakozott")
    return ws

async def index(request):
    return web.FileResponse('./static/client.html')

app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/ws', websocket_handler)
app.router.add_static('/static/', path='./static', name='static')

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
