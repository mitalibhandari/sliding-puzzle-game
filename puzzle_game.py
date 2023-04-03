"""
    Mitali Bhandari
    CS 5001 -- Fall 21
    Project
    Puzzle Game - main file 
"""
import turtle
import time
import random
PLAYER_NAME = []
MOVES = 0
REMAINING_MOVES = 0
NUM_ROWS = 4  # Max 4
NUM_COLS = 4  # Max 4
TILE_WIDTH = 100  # Actual image size
TILE_HEIGHT = 100  # Actual image size
FONT_SIZE = 24
FONT = ('Helvetica', FONT_SIZE, 'normal')
SCRAMBLE_DEPTH = 100
images = []

for i in range(NUM_ROWS * NUM_COLS - 1):
    file = f"Images/mario/{i+1}.gif"
    images.append(file)
images.append(f"Images/mario/blank.gif")

reset = []
for i in range(NUM_ROWS * NUM_COLS-1):
    file = f"Images/mario/{i+1}.gif"
    reset.append(file)
reset.append(f"Images/mario/blank.gif")


def register_images():
    global screen
    for i in range(len(images)):
        screen.addshape(images[i])


def index_2d(my_list, v):
    """Returns the position of an element in a 2D list."""
    for i, x in enumerate(my_list):
        if v in x:
            return (i, x.index(v))


def swap_tile(tile):
    """Swaps the position of the clicked tile with the empty tile."""
    global screen

    current_i, current_j = index_2d(board, tile)
    empty_i, empty_j = find_empty_square_pos()
    empty_square = board[empty_i][empty_j]

    if is_adjacent([current_i, current_j], [empty_i, empty_j]):
        temp = board[empty_i][empty_j]
        board[empty_i][empty_j] = tile
        board[current_i][current_j] = temp

        draw_board()


def is_adjacent(el1, el2):
    """Determines whether two elements in a 2D array are adjacent."""
    if abs(el2[1] - el1[1]) == 1 and abs(el2[0] - el1[0]) == 0:
        return True
    if abs(el2[0] - el1[0]) == 1 and abs(el2[1] - el1[1]) == 0:
        return True
    return False


def find_empty_square_pos():
    """Returns the position of the empty square."""
    global board
    for row in board:
        for candidate in row:
            if candidate.shape() == f"Images/mario/blank.gif":
                empty_square = candidate

    return index_2d(board, empty_square)


def scramble_board():
    t = turtle.Turtle()
    """Scrambles the board in a way that leaves it solvable."""
    global board, screen, REMAINING_MOVES

    for i in range(SCRAMBLE_DEPTH):
        for row in board:
            for candidate in row:
                if candidate.shape() == f"Images/mario/blank.gif":
                    empty_square = candidate

        empty_i, empty_j = find_empty_square_pos()
        directions = ["up", "down", "left", "right"]

        if empty_i == 0:
            directions.remove("up")
        if empty_i >= NUM_ROWS - 1:
            directions.remove("down")
        if empty_j == 0:
            directions.remove("left")
        if empty_j >= NUM_COLS - 1:
            directions.remove("right")

        direction = random.choice(directions)

        if direction == "up":
            swap_tile(board[empty_i - 1][empty_j])
            REMAINING_MOVES += 1
        if direction == "down":
            swap_tile(board[empty_i + 1][empty_j])
            REMAINING_MOVES += 1

        if direction == "left":
            swap_tile(board[empty_i][empty_j - 1])
            REMAINING_MOVES += 1

        if direction == "right":
            swap_tile(board[empty_i][empty_j + 1])
            REMAINING_MOVES += 1


def draw_board():
    global screen, board

    # Disable animation
    screen.tracer(0)

    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            tile = board[i][j]
            tile.showturtle()
            tile.goto(-280 + j * (TILE_WIDTH + 2), 250 - i * (TILE_HEIGHT + 2))

    # Restore animation
    screen.tracer(1)


def create_tiles():
    """
    Creates and returns a 2D list of tiles based on turtle objects
    in the winning configuration.
    """
    board = [["#" for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            tile_num = NUM_COLS * i + j
            tile = turtle.Turtle(images[tile_num])
            tile.penup()
            board[i][j] = tile

            def click_callback(x, y, tile=tile):
                """Passes `tile` to `swap_tile()` function."""
                return swap_tile(tile)

            tile.onclick(click_callback)

    return board


def window_setting(my_turtle, window, splash_screen):
    window.setup(width=800, height=800)
    window.title("CS5001 Sliding Puzzle Game")
    add_image(window, splash_screen, 0, 0)
    screen.bgcolor("aliceblue")
    screen.tracer(0)
    time.sleep(3)


def add_image(window, gif, x_pt, y_pt):

    t = turtle.Turtle()
    window = turtle.Screen()
    t.up()
    window.addshape(gif)
    t.penup()
    t.goto(x_pt, y_pt)
    t.shape(gif)


def draw_rectangle(myTurtle, xPt, yPt, width, height, color, size):

    myTurtle.up()
    myTurtle.goto(xPt, yPt)
    myTurtle.down()
    myTurtle.pencolor(color)
    myTurtle.pensize(size)
    myTurtle.forward(width)
    myTurtle.right(90)
    myTurtle.forward(height)
    myTurtle.right(90)
    myTurtle.forward(width)
    myTurtle.right(90)
    myTurtle.forward(height)
    myTurtle.right(90)


def add_namebox(my_turtle, window):
    global PLAYER_NAME
    name = window.textinput("5001 Puzzle Slide", "Your Name:")
    PLAYER_NAME.append(name)
    return name


def leaders(t):
    global PLAYER_NAME, screen
    for i in range(len(PLAYER_NAME)):
        t.penup()
        t.goto(130, 230)
        t.down()
        t.pencolor("blue")
        t.write(f"Leaders:\n\n1. {PLAYER_NAME[i]}",
                align='left', font=('Arial', 25, 'bold'))
        add_image(screen, "Images/mario/mario_thumbnail.gif", 300, 300)


def add_moves_box(my_turtle, window):
    global MOVES
    MOVES = window.textinput("5001 Puzzle Slide - Moves",
                             "Enter the number of moves(chances) you want(5-200)")

    return MOVES


def draw_game_board(window, my_turtle):
    window_setting(my_turtle, window,
                   "Resources/splash_screen.gif")
    window.clear()
    my_turtle.up()
    my_turtle.goto(-250, 250)
    my_turtle.down()

    PLAYER_NAME.append(add_namebox(my_turtle, window))
    MOVES = int(add_moves_box(my_turtle, window))
    my_turtle.speed(15)
    my_turtle.goto(-335, 335)
    my_turtle.down()
    draw_rectangle(my_turtle, -335, 335, 415, 500, 'black', 8)
    draw_rectangle(my_turtle, 110, 335, 225, 500, 'blue', 7)
    draw_rectangle(my_turtle, -335, -240, 670, 100, 'black', 8)


def quitbutton():
    global screen
    quit_button = turtle.Turtle("Resources/quitbutton.gif")
    quit_button.penup()
    quit_button.goto(270, -290)
    quit_button.onclick(lambda x, y: set_quit())


def set_quit():
    global screen
    screen.clear()
    add_image(screen, "Resources/quitmsg.gif", 0, 0)
    time.sleep(2)
    add_image(screen, "Resources/credits.gif", 0, 0)
    time.sleep(2)


def main():
    global screen, board
    t = turtle.Turtle()
    screen = turtle.Screen()

    draw_game_board(screen, t)
    t.up()
    t.goto(270, -290)
    add_image(screen,
              "Resources/quitbutton.gif", 270, -290)
    add_image(screen,
              "Resources/loadbutton.gif", 180, -290)
    add_image(screen,
              "Resources/resetbutton.gif", 90, -290)

    t.goto(-300, -300)
    t.pendown()

    t.write(f"Player Moves: {MOVES}",
            align='left', font=('Arial', 25, 'bold'))
    leaders(t)
    register_images()

    # Initialise game and display
    board = create_tiles()
    scramble_board()
    draw_board()
    quitbutton()
    screen.tracer(1)  # Restore animation


main()
turtle.done()
