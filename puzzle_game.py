"""
    Mitali Bhandari
    CS 5001 -- Fall 21
    Project
    This is game driver for the project
"""

import turtle
from slide_game import Game

def main():

    game = Game()
    
    game.start_screen()
    game.make_screen()

    game.make_button()

    game.intro_theme()
    game.create_page()
    game.on_click_position() 

    turtle.mainloop()

if __name__ == "__main__":
    main()
