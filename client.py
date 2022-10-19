import asyncio
import websockets
import json
import argparse
import socket
import importlib
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default=socket.gethostname())
parser.add_argument('--port', type=int, default=8765)
parser.add_argument('--timeout', type=int, default=60*2)
parser.add_argument('--player', type=str, default="Bot")
parser.add_argument('--devnull', action='store_true')

args = parser.parse_args()
player = getattr(importlib.import_module(f"{args.player}.Player"), "Player")(args.player)

score = 0

async def play():
    global score, executor

    async with websockets.connect(f"ws://{args.host}:{args.port}") as ws:
        await ws.send(json.dumps({'event': 'join', 'name': player.name}))
        async for message in ws:
            message = json.loads(message)
            e = message['event']
            info = json.loads(message['info'])
            score = info[0]['score']

            if e == 'act':
                result = player.act(info)
                await ws.send(json.dumps({'event': 'act', 'act': result}))
            elif e == 'gameover':
                break

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        with open(os.devnull, 'w') as t:
            if args.devnull:
                sys.stdout = t
            loop.run_until_complete(asyncio.wait_for(play(), args.timeout))
    except:
        pass
    finally:
        sys.stdout = sys.__stdout__
        print(f"score = {score}", flush=True)
        loop.close()