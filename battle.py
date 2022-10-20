import curses
from board import ACTIONS, Board
from renderer import RenderBoard, init_colors
import asyncio
import websockets
import json
import random
import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default=socket.gethostname())
parser.add_argument('--port', type=int, default=8765)
parser.add_argument('--timeout', type=int, default=10000)
parser.add_argument('--nodisplay', action='store_false')
args = parser.parse_args()

players = {}
num_players = 0
start = asyncio.Condition()
lock = asyncio.Lock()
seed = random.randint(0, 1000)

async def join(ws, name):
    global num_players, lock, start
    async with lock:
        num_players += 1
    board = Board(seed=seed)
    if args.nodisplay:
        viewer = RenderBoard(board, player2=True if num_players == 2 else False)
    else:
        viewer = None
    players[ws] = {'name': name, 'board': board, 'viewer': viewer, 'score': 0}
    async with start:
        if num_players == 2:
            start.notify_all()
        else:
            await start.wait()

async def make_info(ws):
    global players

    board1 = None
    board2 = None

    for k, v in players.items():
        if k == ws:
            board1 = v['board'].__dict__
        else:
            board2 = v['board'].__dict__

    return [board1, board2]
    

async def handler(ws, port):
    global players, num_players

    async for message in ws:
        message = json.loads(message)
        e = message['event']
        player = players.get(ws, None)

        if e == 'join':
            await join(ws, message['name'])
            player = players[ws]
            info = json.dumps(await make_info(ws))
            await ws.send(json.dumps({'event': 'act', 'info': info}))

        elif e == 'act':
            player['board'].act(ACTIONS.index(message['act']))

            info = json.dumps(await make_info(ws))

            if player['board'].is_game_over():
                player['score'] = player['board'].score
                if args.nodisplay:
                    player['viewer'].draw_game_window()
                await ws.send(json.dumps({'event': 'gameover', 'info': json.dumps(await make_info(ws))}))
                num_players -= 1
                return 

            if args.nodisplay:
                player['viewer'].draw_game_window()

            if player['score'] != player['board'].score:
                if args.nodisplay:
                    player['viewer'].draw_status_window()
                player['score'] = player['board'].score
            
            penalty = [0, 0, 0, 1, 3][player['board'].num_burn]

            if (num_players == 2) and (penalty != 0):
                opponent_ws = list((o for o in players.keys() if o != ws))[0]
                opponent = players[opponent_ws]
                opponent['board'].add_penalty_minos(penalty)
                if opponent['board'].is_game_over():
                    opponent['score'] = player['board'].score
                    if args.nodisplay:
                        opponent['viewer'].draw_game_window()
                    await opponent_ws.send(json.dumps({'event': 'gameover', 'info': json.dumps(await make_info(opponent_ws))}))
                    num_players -= 1

            player['board'].num_burn = 0

            await ws.send(json.dumps({'event': 'act', 'info': info}))

def init_render():
    curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.curs_set(0)

    init_colors()

async def main():
    async with websockets.serve(handler, args.host, args.port):
        await asyncio.Future()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if args.nodisplay:
        init_render()

    try:
        loop.run_until_complete(asyncio.wait_for(main(), args.timeout))
    except:
        if args.nodisplay:
            curses.endwin()
    finally:

        p1 = list(players.values())[0]
        p2 = list(players.values())[1]
        loop.close()
        print(f"{p1['name']}:{p2['name']} = {p1['score']}:{p2['score']}", flush=True)
