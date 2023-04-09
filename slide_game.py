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

    def click_check(self, x, y):
        """
        Function: click_check
        Check whether the click hits the blank slide or the button
        :param x: (float) click x coordinate
        :param y: (float) click y coordinate
        :return: None
        """
        
        quit_boundary = self.quit_button.get_button_boundary()
        reset_boundary = self.reset_button.get_button_boundary()
        load_boundary = self.load_button.get_button_boundary()
        
        # if click is on the quit button
        if (
            quit_boundary[1] <= x <= quit_boundary[0] and 
            quit_boundary[3] <= y <= quit_boundary[2]
        ):
            self.quit_button.quit_service()

        # if click is on the reset button
        elif (
            reset_boundary[1] <= x <= reset_boundary[0] and 
            reset_boundary[3] <= y <= reset_boundary[2]
        ):
            self.reset_slides()
        
        # if click is on the load button
        elif (
            load_boundary[1] <= x <= load_boundary[0] and 
            load_boundary[3] <= y <= load_boundary[2]
        ):
            self.load_slides()
        
        # if the click is on the blank slide
        else:
            self.swap_slides(x, y) 
    
    def swap_slides(self, x, y):
        blank_boundary = self.blank.get_boundary()
        blank_x_lower = blank_boundary[1]
        blank_y_lower = blank_boundary[3]

        for i in range(len(self.slides)):
            slide = self.slides[i]
            slide_boundary = slide.get_boundary()
            x_upper = slide_boundary[0]
            x_lower = slide_boundary[1]
            y_upper = slide_boundary[2]
            y_lower = slide_boundary[3]

            # if click hits one slide and it's around blank slide

            if (x_lower + y_lower - self.tile_size - 3 == blank_x_lower + blank_y_lower
                ) or (x_lower + y_lower + self.tile_size + 3 == blank_x_lower + blank_y_lower):
                if x_lower <= x <= x_upper and y_lower <= y <= y_upper:

                    # swap slides 
                    temp_name = self.blank.name
                    self.blank.switch_position(slide.name)
                    slide.switch_position(temp_name)

                    slide.blank = True 
                    self.blank.blank = False 

                    # redefine blank slide
                    self.blank = slide
                    self.player_moves += 1
                    self.board.display_player_move(self.player_moves)
                    self.check_win_or_lose()
                    break 

    def reset_slides(self):
        """
        function: reset_slides
        Helper function to reset slides once user clicks on the reset button 
        """
        # make sure nothing happens when user hits reset button twice in a row
        reset = True 
        for i in range(len(self.slides)):
            if self.slides[i].name != self.unscrambled_slides[i]:
                reset = False 
    
        # if first time hitting reset
        if not reset:
            self.slides = []
            for i in range(self.num_of_slides):
                # create new slide with unscrambled slides
                slide = Slide(self.unscrambled_slides[i], self.s, self.tile_size)
                slide.check_blank_status()
                self.slides.append(slide)
                if slide.blank:
                    self.blank = slide 
            self.create_slide_page() 

    def load_slides(self):
        """
        function: load_slides
        Helper function to load new slides once user clicks on the reset button 
        """
        # check that theme is valid
        self.theme.reload_warning() 
            
        # remove existing slides and logo 
        for i in range(len(self.slides)):
            self.slides[i].remove_slide()
        self.logo.remove_image()

        # clear player moves
        self.player_moves = 0
        self.board.display_player_move(self.player_moves)

        # display new slides and logo  
        self.intro_theme()
        self.create_page() 

    def on_click_position(self):
        self.s.onclick(self.click_check)

    def check_win_or_lose(self):
        self.lose_game()
        self.win_game()
    
    def check_move_num(self):
        """
        Function: check_move_num
        Check if the player moves are less than or equal to total moves 
        :return: None
        """
        return self.player_moves <= self.move_num 
    
    def check_win_game(self):
        """
        Function: check_win_game
        Check if the slide list is the same with the unscrambled list
        :return: None
        """
        for i in range(self.num_of_slides):
            if self.slides[i].name != self.unscrambled_slides[i]:
                return False 
        return True 

    def lose_game(self):
        """
        Function: lose_game
        if the player has lost the game then show lose image and exit
        :return: None
        """
        if not self.check_move_num() and not self.check_win_game():
            self.s.ontimer(self.set_screen(PATH_REC + LOSE_MSG), 2000) 
            self.s.ontimer(self.set_screen(PATH_REC + CREDIT), 2000) 
            self.s.ontimer(turtle.bye, 1000)

    def win_game(self):
        """
        Function: win_game
        if the user wins the game then show the win image and exit 
        :return: None
        """
        if self.check_move_num() and self.check_win_game():
            self.leaderboard_text.update_leaderboard(self.player_moves, self.user_name) 
            self.s.ontimer(self.set_screen(PATH_REC + WIN_MSG), 2000) 
            self.s.ontimer(self.set_screen(PATH_REC + CREDIT), 2000) 
            self.s.ontimer(turtle.bye, 1000)

    def set_screen(self, bgpic):
        """
        Function: set_screen
        Set screen for losing or winning or ending game
        :param bgpic: (str) background pic name
        :return: None
        """
        self.s.addshape(bgpic)
        self.t.shape(bgpic)
        self.t.showturtle()
        self.t.penup()
        self.s.ontimer(self.t.goto(0,0), 2000)




                



