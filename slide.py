import turtle 

class Slide:
    def __init__(self, name, screen, size):
        """
        Constructor Function
        :param name: (str) the file name of each slide
        :param screen: turtle.screen from gameboard
        :param size: (int) the size of each slide
        """
        self.name = name
        self.screen = screen
        
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.screen.addshape(self.name)

        self.size = size
        self.x = 0
        self.y = 0
        self.boundaries = []
        self.clicked = False
        self.blank = False 

        
    
    
    def position_slide(self, x, y):
        """
        Function: position_slide
        :param x: (int) x coordinate of the slide
        :param y: (int) y coordinate of the slide
        :return: None
        """
        self.x = x 
        self.y = y 

        self.t.speed(0)
        self.t.penup()
        self.t.goto(self.x - self.size/2, self.y - self.size/2)
        self.t.pendown()
        self.t.pensize(2)
        for i in range(4):
            self.t.forward(self.size)
            self.t.left(90)
        
        self.t.penup()
        self.t.goto(self.x, self.y)
        self.t.shape(self.name)
        self.t.pendown()
        self.t.showturtle()
    
    def get_boundary(self):
        """
        Function: get_boundary
        Get the boundary of each slide according to the coordinate and size
        :return: self.boundaries(list) list that consists of
        the bottom, top, left, right coordinate
        """

        x_upper_boundary = self.x + (self.size/2)
        self.boundaries.append(x_upper_boundary)

        x_lower_boundary = self.x - (self.size/2)
        self.boundaries.append(x_lower_boundary)

        y_upper_boundary = self.y + (self.size/2)
        self.boundaries.append(y_upper_boundary)

        y_lower_boundary = self.y - (self.size/2)
        self.boundaries.append(y_lower_boundary)

        return self.boundaries

    def switch_position(self, name):
        """
        Function: switch_position
        Switch shape and name of two slides
        :param name: file name of the other slide that is switched
        :return: None
        """
        self.t.shape(name)
        self.name = name 
    
    def check_blank_status(self):
        """
        Function: check_blank_status
        Check if the slide is blank according to its name
        :return: None
        """
        if "blank" in self.name or self.blank:
            self.blank = True 
    
    def remove_slide(self):
        """
        Function: remove_slide
        Hide and clear the slide on the screen
        :return: None
        """
        self.t.hideturtle()
        self.t.clear()


