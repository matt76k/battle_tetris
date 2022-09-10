import asyncio
import websockets
import json
import time
from Bot.Player import Player

player = Player('bot')

async def main():
    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send(json.dumps({'event': 'join', 'name': player.name}))
        async for message in ws:
            message = json.loads(message)

            e = message['event']
            if e == 'act':
                await ws.send(json.dumps({'event': 'act', 'act': player.act(json.loads(message['info']))}))
            elif e == 'gameover':
                print(f"score = {json.loads(message['info'])[0]['score']}")
                break

asyncio.run(main())
