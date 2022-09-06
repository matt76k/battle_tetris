import curses
import board
from board import ACTIONS
import time

TOP_MARGIN = 1
LEFT_MARGIN = 3

def init_colors():
    curses.init_pair(99, 8, curses.COLOR_BLACK) # 1 - grey
    curses.init_pair(98, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(97, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(96, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(95, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.init_pair(1, curses.COLOR_BLACK, 75) # 水色
    curses.init_pair(2, curses.COLOR_BLACK, 220) #黄色
    curses.init_pair(3, curses.COLOR_BLACK, 28) # 緑
    curses.init_pair(4, curses.COLOR_BLACK, 124) # 赤
    curses.init_pair(5, curses.COLOR_BLACK, 19) #青色
    curses.init_pair(6, curses.COLOR_BLACK, 215) # 橙色
    curses.init_pair(7, curses.COLOR_BLACK, 54) #紫

class RenderBoard:
    def __init__(self, game_board, player2 = False):
        self.game_board = game_board
        self.game_window_width = 2 * game_board.width + 2
        self.game_window_height = game_board.height + 2

        self.status_window_width = 2 * (3 + 2)
        self.status_window_height = 5 + 4 + 4 + 2

        self.player2 = player2

        self.game_window = self.__init_game_window()
        self.status_window = self.__init_status_window()
        self.draw_game_window()
        self.draw_status_window()

    def __init_game_window(self):
        window = curses.newwin(self.game_window_height, self.game_window_width, TOP_MARGIN, LEFT_MARGIN if not self.player2 else LEFT_MARGIN + self.game_window_width+ self.status_window_width + 5)
        window.nodelay(True)
        window.keypad(1)

        return window


    def __init_status_window(self):
        window = curses.newwin(self.status_window_height, self.status_window_width, TOP_MARGIN, self.game_window_width + 5 if not self.player2 else LEFT_MARGIN + 2 * self.game_window_width+ self.status_window_width + 5 + 2)
        return window

    def draw_game_window(self):
        self.game_window.border()

        for i in range(self.game_board.height):
            for j in range(self.game_board.width):
                if self.game_board.board[i][j] == 1:
                    self.game_window.addstr(i + 1, 2 * j + 1, "  ", curses.color_pair(96))
                else:
                    self.game_window.addstr(i + 1, 2 * j + 1, " .", curses.color_pair(99))

        # draw block
        for i in range(self.game_board.current_block.size()[0]):
            for j in range(self.game_board.current_block.size()[1]):
                if self.game_board.current_block.shape[i][j] == 1:
                    x = 2 * self.game_board.current_block_pos[1] + 2 * j + 1
                    y = self.game_board.current_block_pos[0] + i + 1
                    self.game_window.addstr(y, x, "  ", curses.color_pair(self.game_board.current_block.color))

        if self.game_board.is_game_over():
            go_title = " Game Over "

            self.game_window.addstr(int(self.game_window_height *.4), (self.game_window_width - len(go_title))//2, go_title, curses.color_pair(95))

        self.game_window.addstr(0, 0, f"Score: {self.game_board.score}")

        self.game_window.refresh()

    def draw_status_window(self):
        if self.game_board.is_game_over():
            return

        for row in range(1, self.status_window_height - 1):
            self.status_window.addstr(row, 2, "".rjust(self.status_window_width - 3, " "))

        self.status_window.border()

        base_row = 0
        for t in self.game_board.get_next():
            start_col = int(self.status_window_width / 2 - t.size()[1])
            base_row += 1

            for row in range(t.size()[0]):
                for col in range(t.size()[1]):
                    if t.shape[row][col] == 1:
                        self.status_window.addstr(row + base_row, start_col + 2 * col, "  ", curses.color_pair(t.color))
        
            base_row += t.size()[0]

        self.status_window.refresh()


if __name__ == "__main__":
    game_board = board.Board()
    game_board.reset()

    try:
        scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)

        init_colors()

        viewer = RenderBoard(game_board)

        while True:
            pass
    finally:
        curses.endwin()
