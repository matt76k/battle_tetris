import random
ACTIONS = ['nop', 'rotate', 'down', 'left', 'right', 'drop']

class Player:
    def __init__(self, name):
        self.name = name
    
    def act(self, info):
        """
        infoはlistになっていて、最初が自分の情報、それ以外は相手の情報があります。
        情報は、6つあり
            board: 確定しているボード(2次元リスト)
            next: 次のブロック3つ（IやOといった形状を表す文字）
            score:現時点でのスコア
            block: 現在操作しているブロックの形（IやOといった形状を表す文字）
            shape: 現在操作しているブロックの形状 (2次元リスト)
            pos: 現在操作しているブロックの位置
        """

        return random.choice(ACTIONS)

