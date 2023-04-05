import turtle 
class ButtonService:
    def __init__(self, button, x, y, screen, message=None):
        """
        Constructor Function
        :param button: (str) picture name of the button
        :param x: (int) x coordinate of the button
        :param y: (int) y coordinate of the button
        :param screen: turtle.screen of the game board
        :param message: (str) warning pic name of the button
        Default to None
        """

        self.screen = screen 
        self.button = button 
        self.x = x
        self.y = y
        self.message = message

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.screen.addshape(self.button)
        self.boudary = []
        self.file = None
    
    def display_button(self):
        """
        Function: display_button
        Display the button on the screen
        :return: None
        """
        self.t.penup()
        self.t.goto(self.x, self.y)
        self.t.shape(self.button)
        self.t.pendown()
        self.t.showturtle()
    

        