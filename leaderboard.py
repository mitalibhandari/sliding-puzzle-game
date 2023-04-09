import turtle 
from validation_service import ValidationService
from text_rectangle import TextRectangle

LEADERBOARD_TEXT_X_START = 180
LEADERBOARD_TEXT_Y_START = 270

class LeaderBoard:
    def __init__(self, leaderboard_file):
        """
        Constructor Function
        :param leaderboard_file: it is an object from ValidationService Class
        self.file_content is a nested list that stores names and moves
        """
        self.file = leaderboard_file
        self.file_content = []
    
    def read_leaderboard(self):
        """
        Function: read_leaderboard
        Read leaderboard_file to see if it is valid and
        Store info in self.file_content
        :return: None
        """
        self.file.validate_leaderboard_file()
        if self.file.get_valid_status():
            leaderboard_info = self.file.get_file_content()

            for content in leaderboard_info:
                content = content.split(" :")
                self.file_content.append(content)
        
        self.display_leaderboard()
    
    def display_leaderboard(self):
        """
        Function: display_leaderboard
        Display leaderboard info in self.file_content
        :return: None
        """
        t = turtle.Turtle()
        x = LEADERBOARD_TEXT_X_START
        y = LEADERBOARD_TEXT_Y_START

        
        TextRectangle(t, "Leaders:", x, y, 'blue', 18).write_text()
        y -= 30
        if len(self.file_content) > 0:
            for content in self.file_content:
                if len(content) > 1:
                    player_move = content[0]
                    user_name = content[1]
                    info = f"{player_move} : {user_name}"
                    TextRectangle(t, info, x, y, 'blue', 15).write_text()
                
                y -= 32
    
    def update_leaderboard(self, player_move, user_name):
        """
        Function: update_leaderboard
        Update the player record to the self.file_content
        :param player_move: int
        :param user_name: str
        :return: None
        """
        if len(self.file_content) > 0:
            for i in range(len(self.file_content)):
                score = int(self.file_content[i][0])

                # insert in the front of the first score that is greater than player moves
                if player_move <= score:
                    new_list = [player_move, user_name]
                    self.file_content.insert(i, new_list)
                    break 
                
                if i == len(self.file_content) - 1:
                    self.file_content.append([player_move, user_name])
        # empty file
        else:
            self.file_content.append([player_move, user_name])

        self.write_leaderboard()
    
    def write_leaderboard(self):
        self.file_content = self.file_content[:10]
        with open(self.file.file, mode='w') as f:
            for i in range(len(self.file_content)):
                content = self.file_content[i]
                if len(content) > 1:
                    f.write(f"{content[0]} : {content[1]} \n")
                    




