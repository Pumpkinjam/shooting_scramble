import numpy as np

# All Objects in game (Character, Item, Bullets...) must be extended by this class
class GameObject:
    # todo... set "img" field (from image_src (or pixel_info))
    def __init__(self, width, height):
        self.appearance = 'circle'
        self.state = None
        self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])
        
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#FFFFFF"

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            self.outline = "#FFFFFF" #Í≤??†ï?Éâ?ÉÅ ÏΩîÎìú!
        
        else:
            self.state = 'move'
            self.outline = "#FF0000" #Îπ®Í∞ï?Éâ?ÉÅ ÏΩîÎìú!

            if command['up_pressed']:
                self.position[1] -= 5
                self.position[3] -= 5

            if command['down_pressed']:
                self.position[1] += 5
                self.position[3] += 5

            if command['left_pressed']:
                self.position[0] -= 5
                self.position[2] -= 5
                
            if command['right_pressed']:
                self.position[0] += 5
                self.position[2] += 5
                
        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]) 