import turtle
from draw_rectangle import DrawRectangle
from text_rectangle import TextRectangle
from button_service import ButtonService

LEADERBOARD_WIDTH = 250
LEADERBOARD_HEIGHT = 495
LEADERBOARD_X_START = 170
LEADERBOARD_Y_START = -185
GAME_X_START = -350

BUTTON_WIDTH = 770
BUTTON_HEIGHT = 105
BUTTON_Y_START = -310

TEXT_INPUT = "Enter the number of moves (chances) you want (5-200)?"
MOVE_TEXT_X_START = -340
MOVE_TEXT_Y_START = -275

class Board:
    def __init__(self, screen):
        """
        Constructor Function
        :param screen: this is turtle.screen from game
        """

        self.t = turtle.Turtle()
        self.screen = screen
        self.t.hideturtle()
        self.user_name = None
        self.number_of_moves = None
        self.x = 0
        self.y = 0
    
    def set_spalsh_screen(self, bgpic):
        """
        Function: set_splash_screen
        Set up the splash screen
        :param bgpic: splash_screen.gif
        :return: None
        """
        self.screen.addshape(bgpic)
        self.t.shape(bgpic)
        self.t.showturtle()
        self.t.penup()
        self.screen.ontimer(self.t.goto(0,0), 2000)
        turtle.clearscreen()

    def user_input(self):
        self.user_name = turtle.textinput(title="CS5001 Puzzle Slide", prompt="Your name:")
        # Assume the name is no leader if user input is blank
        if self.user_name is None:
            self.user_name = "No Leader"
        
        self.number_of_moves = int(turtle.numinput(
            title="CS5001 Puzzle Slide-Moves", 
            prompt="Enter the number of moves (chances) you want (5-200)?", 
            default=10, minval=5, maxval=200
            ))
    
    def make_leaderboard_area(self):
        """
        Function: make_leaderboard_area
        Draw the leaderboard area
        :return: None
        """
        leaderboard_area = DrawRectangle(
            LEADERBOARD_HEIGHT, LEADERBOARD_WIDTH, 
            LEADERBOARD_X_START, LEADERBOARD_Y_START, 
            'blue', 8)
        leaderboard_area.draw_shape()
    
    def make_game_area(self):
        """
        Function: make_game_area
        Draw the gameboard area
        :return: None
        """
        game_area = DrawRectangle(
            LEADERBOARD_HEIGHT, LEADERBOARD_HEIGHT, 
            GAME_X_START, LEADERBOARD_Y_START, 
            'black', 8)
        game_area.draw_shape()
    
    def make_button_area(self):
        """
        Function: make_button_area
        Draw the button and move area
        :return: None
        """
        button_area = DrawRectangle(
            BUTTON_HEIGHT, BUTTON_WIDTH, 
            GAME_X_START, BUTTON_Y_START, 
            'black', 8)
        button_area.draw_shape()
    
    def display_player_move(self, play_move):
        play_move_count = f"Player Moves: {play_move}"
        text = TextRectangle(self.t, play_move_count, MOVE_TEXT_X_START, MOVE_TEXT_Y_START, 'black', 20)
        text.remove_text()
        text.write_text()
    
    def get_input_name(self):
        return self.user_name
    
    def get_input_num(self):
        return self.number_of_moves
