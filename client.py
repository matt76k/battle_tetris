import asyncio
import websockets
import json
import argparse
import socket
import importlib

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default=socket.gethostname())
parser.add_argument('--port', type=int, default=8765)
parser.add_argument('--timeout', type=int, default=60*10)
parser.add_argument('--player', type=str, default="Bot")

args = parser.parse_args()
player = getattr(importlib.import_module(f"{args.player}.Player"), "Player")(args.player)

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

            if e == 'act':
                result = player.act(info)
                await ws.send(json.dumps({'event': 'act', 'act': result}))
            elif e == 'gameover':
                break

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(asyncio.wait_for(play(), args.timeout))
    except:
        pass
    finally:
        print(f"score = {score}", flush=True)
        loop.close()