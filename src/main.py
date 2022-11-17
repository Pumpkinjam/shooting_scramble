from pkjgame import *

'''
from PIL import Image, ImageDraw, ImageFont
import time
import random
import cv2 as cv
import numpy as np
from colorsys import hsv_to_rgb
'''

def main():
    gm = GameManager(30, 240, 240)
    gm.start()
    
    
if __name__ == '__main__':
    main()
    '''
    enemy_1 = Enemy((50, 50))
    enemy_2 = Enemy((200, 200))
    enemy_3 = Enemy((150, 50))

    enemys_list = [enemy_1, enemy_2, enemy_3]

    bullets = []
    while True:
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        
        if not joystick.button_U.value:  # up pressed
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value:  # down pressed
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True

        if not joystick.button_A.value: # A pressed
            bullet = Bullet(my_circle.center, command)
            bullets.append(bullet)

        my_circle.move(command)
        for bullet in bullets:
            bullet.collision_check(enemys_list)
            bullet.move()
        
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
        my_draw.ellipse(tuple(my_circle.position), outline = my_circle.outline, fill = (0, 0, 0))
        
        for enemy in enemys_list:
            if enemy.state != 'die':
                my_draw.ellipse(tuple(enemy.position), outline = enemy.outline, fill = (255, 0, 0))

        for bullet in bullets:
            if bullet.state != 'hit':
                my_draw.rectangle(tuple(bullet.position), outline = bullet.outline, fill = (0, 0, 255))


        joystick.disp.image(my_image)
        '''

