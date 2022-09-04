import curses
from board import ACTIONS, Board
from renderer import RenderBoard, init_colors
import asyncio
import websockets
import json
import time

players = {}
board = None
viewer = None
old_score = 0

async def join(ws, name):
    players[name] = ws

async def handler(ws):
    global old_score

    async for message in ws:
        message = json.loads(message)

        e = message['event']

        if e == 'join':
            await join(ws, message['name'])
            info = json.dumps([board.__dict__])
            await ws.send(json.dumps({'event': 'act', 'info': info}))

        elif e == 'act':
            board.act(ACTIONS.index(message['act']))
            info = json.dumps([board.__dict__])

            if board.is_game_over():
                await ws.send(json.dumps({'event': 'gameover', 'info': info}))
                reset()
        
            viewer.draw_game_window()

            if old_score != board.score:
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
    viewer = RenderBoard(board)
    old_score = 0

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore')
    init_render()
    reset()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        curses.endwin()
