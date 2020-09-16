class Board:
    def __init__(self, rows: int, cols: int, ch):
        self.board = [[ch for _ in range(cols + 2)] for __ in range(rows + 2)]
        self._r = rows + 2
        self._c = cols + 2
        self.r = rows
        self.c = cols

    def __getitem__(self, item: int):
        if 0 <= item < self._r:
            return self.board[item]
        return None

    def fetch(self, r: int, c: int):
        if 0 <= r < self.r and 0 <= c < self.c:
            return self.board[r + 1][c + 1]
        return None

    def set(self, r: int, c: int, val):
        if 0 <= r < self.r and 0 <= c < self.c:
            self.board[r + 1][c + 1] = val

    def make_edges(self, ch):
        for i in range(self._r):
            if i == 0 or i == self._r - 1:
                for j in range(self._c):
                    self.board[i][j] = ch
            else:
                self.board[i][0] = ch
                self.board[i][self._c - 1] = ch

    def __str__(self):
        text = ""
        for r in self.board:
            for c in r:
                text += c
            text += "\n"
        return text
