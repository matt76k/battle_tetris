import curses
from board import ACTIONS, Board
from renderer import RenderBoard, init_colors
import asyncio
import websockets
import json
import time

players = {}
num_players = 0
start = asyncio.Condition()
lock = asyncio.Lock()

async def join(ws, name):
    global num_players, lock, start
    async with lock:
        num_players += 1
    board = Board(seed=42)
    viewer = RenderBoard(board, player2=True if num_players == 2 else False)
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
    

async def handler(ws):
    global players

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
                player['viewer'].draw_game_window()
                await ws.send(json.dumps({'event': 'gameover', 'info': json.dumps(await make_info(ws))}))
                return 

            player['viewer'].draw_game_window()

            if player['score'] != player['board'].score:
                player['viewer'].draw_status_window()
                player['score'] = player['board'].score
            
            penalty = [0, 0, 0, 1, 3][player['board'].num_burn]

            if penalty != 0:
                opponent_ws = list((o for o in players.keys() if o != ws))[0]
                opponent = players[opponent_ws]
                opponent['board'].add_penalty_minos(penalty)
                if opponent['board'].is_game_over():
                    opponent['score'] = player['board'].score
                    opponent['viewer'].draw_game_window()
                    opponent_ws.send(json.dumps({'event': 'gameover', 'info': json.dumps(await make_info(opponent_ws))}))

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
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore')
    init_render()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        curses.endwin()
