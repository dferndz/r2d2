from typing import List

from game_engine.board import Board

ROWS = 10
COLS = 10
PLAYER_CHAR = '😀'
WALL_CHAR = '🟥'
BOX_CHAR = '📦'
GOAL_CHAR = '💎'
BLANK_CHAR = '⬛'


class Coord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Game:
    goals: List[Coord] = []
    num_goals = 0

    def __init__(self):
        self.board = Board(ROWS, COLS, BLANK_CHAR)
        self.board.make_edges(WALL_CHAR)
        self.r = ROWS
        self.c = COLS
        self.player = None

    def in_range(self, x: int, y: int):
        return 0 <= x < self.c and 0 <= y < self.r

    def win(self):
        return self.num_goals == len(self.goals)

    def check_collision(self, x: int, y: int):
        if self.board.fetch(y, x) != BLANK_CHAR:
            return True
        return False

    def put_player(self, x: int, y: int):
        if self.in_range(x, y):
            if self.player:
                self.board.set(self.player.y, self.player.x, BLANK_CHAR)
                self.player.x = x
                self.player.y = y
            else:
                self.player = Coord(x, y)
            self.board.set(y, x, PLAYER_CHAR)

    def put_box(self, x: int, y: int):
        if self.in_range(x, y):
            self.board.set(x, y, BOX_CHAR)

    def build_wall(self, from_x: int, from_y: int, x: int, y: int):
        for i in range(from_y, from_y + y):
            for j in range(from_x, from_x + x):
                self.board.set(i, j, WALL_CHAR)

    def add_goal(self, x: int, y: int):
        if self.in_range(x, y):
            if self.board.fetch(y, x) == BLANK_CHAR:
                self.goals.append(Coord(x, y))
                self.update_goals()

    def update_goals(self):
        self.num_goals = 0
        for g in self.goals:
            if self.board.fetch(g.y, g.x) == BLANK_CHAR:
                self.board.set(g.y, g.x, GOAL_CHAR)
            elif self.board.fetch(g.y, g.x) == BOX_CHAR:
                self.num_goals += 1

    def move_obj(self, from_x: int, from_y: int, x: int, y: int):
        new_x = from_x + x
        new_y = from_y + y

        if self.in_range(new_x, new_y):
            if not self.check_collision(new_x, new_y) or self.board.fetch(new_y, new_x) == GOAL_CHAR:
                c = self.board.fetch(from_y, from_x)
                self.board.set(from_y, from_x, BLANK_CHAR)
                self.board.set(new_y, new_x, c)
                return True
        return False

    def move(self, x: int, y: int):
        if self.player:
            new_x = self.player.x + x
            new_y = self.player.y + y

            if self.in_range(new_x, new_y):
                if not self.check_collision(new_x, new_y):
                    self.put_player(new_x, new_y)
                else:
                    if self.board.fetch(new_y, new_x) == BOX_CHAR:
                        if self.move_obj(new_x, new_y, x, y):
                            self.put_player(new_x, new_y)
                    if self.board.fetch(new_y, new_x) == GOAL_CHAR:
                        self.put_player(new_x, new_y)
        self.update_goals()

    def up(self):
        self.move(0, -1)

    def down(self):
        self.move(0, 1)

    def left(self):
        self.move(-1, 0)

    def right(self):
        self.move(1, 0)



