import curses
from board import ACTIONS, Board
from renderer import RenderBoard, init_colors
import asyncio
import websockets
import json
import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default=socket.gethostname())
parser.add_argument('--port', type=int, default=8765)
parser.add_argument('--nodisplay', action='store_false')
args = parser.parse_args()

players = {}
board = None
viewer = None
old_score = 0

async def join(ws, name):
    players[name] = ws

async def handler(ws, port):
    global old_score

    async for message in ws:
        message = json.loads(message)

        e = message['event']

        if e == 'join':
            reset()
            await join(ws, message['name'])
            info = json.dumps([board.__dict__])
            await ws.send(json.dumps({'event': 'act', 'info': info}))

        elif e == 'act':
            board.act(ACTIONS.index(message['act']))
            info = json.dumps([board.__dict__])

            if board.is_game_over():
                await ws.send(json.dumps({'event': 'gameover', 'info': info}))
                reset()

            if args.nodisplay:
                viewer.draw_game_window()

            if old_score != board.score:
                if args.nodisplay:
                    viewer.draw_status_window()
                old_score = board.score

            info = json.dumps([board.__dict__])
            await ws.send(json.dumps({'event': 'act', 'info': info}))

def init_render():
    curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.curs_set(0)

    init_colors()

def reset():
    global board, viewer, old_score
    board = Board()
    if args.nodisplay:
        viewer = RenderBoard(board)
    old_score = 0

async def main():
    async with websockets.serve(handler, args.host, args.port):
        await asyncio.Future()

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore')
    if args.nodisplay:
        init_render()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        curses.endwin()
