import asyncio
import websockets
import json
import time
from Bot.Player import Player
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor
import os

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default=socket.gethostname())
parser.add_argument('--port', type=int, default=8765)
parser.add_argument('--timeout', type=int, default=60*10)

args = parser.parse_args()
player = Player('bot')
executor = ThreadPoolExecutor(max_workers=1)

score = 0

async def play():
    global score, executor

    loop = asyncio.get_event_loop()

    async with websockets.connect(f"ws://{args.host}:{args.port}") as ws:
        await ws.send(json.dumps({'event': 'join', 'name': player.name}))
        async for message in ws:
            message = json.loads(message)
            e = message['event']
            info = json.loads(message['info'])
            score = info[0]['score']

            try:
                result = await asyncio.wait_for(loop.run_in_executor(executor, player.act, info), timeout=args.timeout)
            except:
                e = 'gameover'

            if e == 'act':
                await ws.send(json.dumps({'event': 'act', 'act': result}))
            elif e == 'gameover':
                print(f"score = {score}", flush=True)
                break

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(play())
    finally:
        loop.close()
        os._exit(0)