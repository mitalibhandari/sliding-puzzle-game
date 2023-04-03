import turtle
class DrawRectangle: 

    def __init__(self, height, width, x, y, color, pensize):
        self.width = width 
        self.height = height
        self.x = x 
        self.y = y 
        self.color = color 
        self.pensize = pensize

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.pencolor(self.color)
        self.t.pensize(self.pensize)
        self.t.speed(0)
    
    def draw_shape(self):
        self.t.penup()
        self.t.goto(self.x, self.y) 
        self.t.pendown()

        for side in range(4):
            if side % 2 == 0:
                self.t.forward(self.width)
                self.t.left(90)
            else:
                self.t.forward(self.height)
                self.t.left(90)
