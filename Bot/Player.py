import random
ACTIONS = ['nop', 'rotate', 'down', 'left', 'right', 'drop']

class Player:
    def __init__(self, name):
        self.name = name
    
    def act(self, info):
        """
        infoはlistになっていて、最初が自分の情報、それ以外は相手の情報があります。
        情報は、5つあり
            board: 確定しているボード(2次元リスト)
            next: 次のブロック3つ（IやOといった形）
            score:現時点でのスコア
            block: 現在操作しているブロックの形
            shape: 現在操作しているブロックの形状
            pos: 現在操作しているブロックの位置
        """

        return random.choice(ACTIONS)

