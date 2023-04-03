"""
Mitali Bhandari
CS5001 Slider Puzzle
Fall 2021
This is TextRectangle helper file to display text in the game
"""
import turtle
class TextRectangle:

    def __init__(self, text, x, y, color, pensize):
        """
        Constructor Function
        :param text: text sentence that is displayed
        :param x: text starting point, x-coordinate
        :param y: text starting point, y-coordinate
        :param color: color of the text
        :param pensize: pensize of the text
        :return none.,
        """
        self.t = turtle.Turtle()

        self.text = text 
        self.x = x 
        self.y = y
        self.color = color
        self.pensize = pensize

        self.t.speed(0)
        self.t.penup()
        self.t.hideturtle()
        self.t.pencolor(self.color)

    def write_text(self):
        self.t.goto(self.x, self.y)
        self.t.write(self.text, move=False, align="left", font=("Ariel", self.pensize, "normal"))
    
    def remove_text(self):
        self.t.hideturtle()
        self.t.clear()
