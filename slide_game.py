import turtle 
import math
import random
from draw_rectangle import DrawRectangle
from text_rectangle import TextRectangle
from button_service import ButtonService
from board import Board
from leaderboard import LeaderBoard
from validation_service import ValidationService
from slide import Slide

PATH_REC = "./Resources"
PATH_IMAGE = "./Images"

RELOAD_ERROR_MSG = '/file_error.gif'
RELOAD_WARN_MSG = '/file_warning.gif'
LEADERBOARD_FILE = 'leaderboard.txt'
LEADERBOARD_ERROR_MSG = '/leaderboard_error.gif'

QUIT_BUTTON = "/quitbutton.gif"
LOAD_BUTTON = "/loadbutton.gif"
RESET_BUTTON = "/resetbutton.gif"
QUIT_MSG = '/quitmsg.gif'
WIN_MSG = '/winner.gif'
LOSE_MSG = "/Lose.gif"
SPLASH = "/splash_screen.gif"
CREDIT = '/credits.gif'
DEFAULT_THEME = "mario.puz"
RELOAD_INPUT = "Enter the name of the puzzle you wish to load. Choices are:/n"

QUIT_X = 350
BUTTON_Y = -255
LOAD_X = 260
RESET_X = 170
LOGO_X = 360
LOGO_Y = 270
GAME_X_START = -350
LEADERBOARD_Y_START = -185
LEADERBOARD_HEIGHT = 495

class Game:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.s = turtle.Screen()
        turtle.title("Sliding Puzzle Game")

        self.user_name = None
        self.move_num = None
        self.player_moves = 0

        self.valid_puz_file = None
        self.valid_leader_file = None
        self.puz_info = []
        self.blank = None
        self.logo = None
        self.tile_size = None 
        self.unscrambled_slides = []
        self.slides = []
        self.num_of_slides = None

        self.board = Board(self.s)

        self.quit_button = ButtonService(PATH_REC + QUIT_BUTTON, QUIT_X, BUTTON_Y, self.s, PATH_REC + QUIT_MSG)
        self.load_button = ButtonService(PATH_REC + LOAD_BUTTON, LOAD_X, BUTTON_Y, self.s)
        self.reset_button = ButtonService(PATH_REC + RESET_BUTTON, RESET_X, BUTTON_Y, self.s)

        self.theme = ValidationService(DEFAULT_THEME, PATH_REC + RELOAD_ERROR_MSG, self.s, PATH_REC + RELOAD_WARN_MSG)
        self.leader_file = ValidationService(LEADERBOARD_FILE, PATH_REC + RELOAD_ERROR_MSG, self.s)
        self.leaderboard_text = LeaderBoard(self.leader_file)


    def start_screen(self):
        """
        Function: start_screen
        Set up splash screen and get input user name and moves
        :return: None
        """
        self.board.set_spalsh_screen(PATH_REC + SPLASH)
        self.leader_file.validate_leaderboard_file()
        self.board.user_input()
        self.user_name = self.board.get_input_name() 
        self.move_num = self.board.get_input_num()
    
    def make_screen(self):
        """
        Function: make_screen
        Draw and write the area on the game board
        :return: None
        """
        turtle.clearscreen()
        self.board.make_game_area()
        self.board.make_leaderboard_area()
        self.board.make_button_area()
        self.leaderboard_text.read_leaderboard()

    def make_button(self):
        """
        Function: make_button
        Display all three buttons
        :return: None
        """
        self.quit_button.display_button()
        self.load_button.display_button()
        self.reset_button.display_button()
    
    def intro_theme(self):
        """
        Function: intro_theme
        Validate directory file and access the slide info
        :return: None
        """
        self.theme.validate_directory_file()

        # clear slides
        self.slides = []
        self.unscrambled_slides = []

        if self.theme.valid:
            self.num_of_slides = int(self.theme.dict_entry["number"])
            thumb = self.theme.dict_entry["thumbnail"]
            self.tile_size = int(self.theme.dict_entry['size'])
            self.logo = ButtonService(thumb, LOGO_X, LOGO_Y, self.s)

            i = 1
            while i <= self.num_of_slides:
                name = self.theme.dict_entry[str(i)]
                self.theme.validate_image(name)

                slide = Slide(name, self.s, self.tile_size)
                slide.check_blank_status()
                self.unscrambled_slides.append(slide.name)
                self.slides.append(slide)
                i += 1

                # get blank slide 
                if slide.blank:
                    self.blank = slide 

    def create_slide_page(self):
        slide_x_start = GAME_X_START + self.tile_size
        slide_y_start = LEADERBOARD_Y_START + LEADERBOARD_HEIGHT - 90

        self.logo.display_button()

        row_num = math.sqrt(self.num_of_slides)
        for i in range(self.num_of_slides):
            self.slides[i].position_slide(slide_x_start, slide_y_start)

            # record blank slide coordinate 
            if self.slides[i].blank:
                self.blank.x = slide_x_start
                self.blank.y = slide_y_start
            
            # draw row and column 

            if (i+1) % row_num == 0:
                slide_x_start = GAME_X_START + self.tile_size
                slide_y_start -= self.tile_size + 3 
            else:
                slide_x_start += self.tile_size + 3 
    
    def create_page(self):
        """
        Function: create_page
        shuffle the slides list and create game area
        :return:
        """
        random.shuffle(self.slides)
        self.create_slide_page()




                



