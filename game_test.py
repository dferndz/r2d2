from game_engine import Game

game = Game()
game.put_player(1, 0)
game.put_box(4, 6)
game.put_box(4, 7)
game.add_goal(1, 3)
game.add_goal(9, 9)
game.build_wall(2, 2, 1, 3)
game.build_wall(0, 4, 3, 1)
game.build_wall(4, 4, 3, 1)

while not game.win():
    print(game.board)
    move = input()

    if move == "w":
        game.up()

    if move == "s":
        game.down()

    if move == "a":
        game.left()

    if move == "d":
        game.right()
print(game.board)
