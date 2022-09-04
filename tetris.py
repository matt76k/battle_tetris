import curses
from board import ACTIONS, Board
from renderer import RenderBoard, init_colors

if __name__ == "__main__":
    game_board = Board()
    old_score = 0

    try:
        scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)

        init_colors()

        viewer = RenderBoard(game_board)

        quit_game = False
        while not quit_game:
            key_event = viewer.game_window.getch()

            if key_event == ord("q"):
                quit_game = True

            if not game_board.is_game_over():
                if key_event == curses.KEY_UP:
                    game_board.act(ACTIONS.index('rotate'))
                elif key_event == curses.KEY_DOWN:
                    game_board.act(ACTIONS.index('down'))
                elif key_event == curses.KEY_LEFT:
                    game_board.act(ACTIONS.index('left'))
                elif key_event == curses.KEY_RIGHT:
                    game_board.act(ACTIONS.index('right'))
                elif key_event == ord(" "):
                    game_board.act(ACTIONS.index('drop'))

            else:
                viewer.game_window.nodelay(False)
            
            viewer.draw_game_window()

            if old_score != game_board.score:
                viewer.draw_status_window()
                old_score = game_board.score
    finally:
        curses.endwin()
