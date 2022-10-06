import curses
from board import ACTIONS, Board, Block
from renderer import RenderBoard, init_colors
import asyncio
import websockets
import json
import sys

scr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
curses.curs_set(0)
init_colors()

game_window = curses.newwin(20, 20, 0, 0)
game_window.nodelay(True)
game_window.keypad(1)

async def main():


    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send(json.dumps({'event': 'join', 'name': 'human'}))
        async for message in ws:
            message = json.loads(message)

            e = message['event']
            if e == 'act':
                act = None
                while act is None:
                    key_event = game_window.getch()

                    if key_event == curses.ERR:
                        await asyncio.sleep(0.1)
                    elif key_event == curses.KEY_UP:
                        act = 'rotate'
                    elif key_event == curses.KEY_DOWN:
                        act = 'down'
                    elif key_event == curses.KEY_LEFT:
                        act = 'left'
                    elif key_event == curses.KEY_RIGHT:
                        act = 'right'
                    elif key_event == ord(" "):
                        act = 'drop'
                    
                await ws.send(json.dumps({'event': 'act', 'act': act}))
            elif e == 'gameover':
                curses.endwin()
                break

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except KeyboardInterrupt:
    curses.endwin()