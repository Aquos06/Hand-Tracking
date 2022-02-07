import mouse as ms
import numpy as np
import math
import pyautogui
import cv2

#find the size of the screen
width,height = pyautogui.size()

clicked = False
mouse_flag = False
prev_coorx, prev_coory = 0, 0
click_counter = 0
#struct the mouse class
class Mouse(object):
                
    def mouse_move(self, hand_coordinate, frame_shape, frame):
        global mouse_flag, prev_coorx, prev_coory
        def mouse_click(hand_coordinate):
            #open >= 40, click <= 35
            global clicked, click_counter
        
            hand_opened = math.hypot(hand_coordinate[12][1]-hand_coordinate[8][1], hand_coordinate[12][2]-hand_coordinate[8][2])
            
            if hand_opened >= 40:
                clicked = False
                click_counter = 0
            if hand_opened <= 30:
                click_counter += 1
                if not clicked and click_counter == 3:
                    ms.click()
                elif clicked and click_counter >= 3:
                    ms.press()
                    
        # def scroll (hand_coordinate):
            
                
        #8-7 >= 15, 12-11 >= 15, 8-6 >= 50, 12-10 >= 60
        if hand_coordinate[7][2]-hand_coordinate[8][2] >= 10 and hand_coordinate[6][2]-hand_coordinate[8][2]>=30 :
            movex = np.interp(hand_coordinate[8][1],[50,550],[width,0]) #produce the movement of mouse on x-axis
            movey = np.interp(hand_coordinate[8][2],[100,330],[0, height]) #produce the movement of mouse on y-axis
            
            if not mouse_flag:
                prev_coorx = movex
                prev_coory = movey
                coor_nowx = prev_coorx
                coor_nowy = prev_coory
                mouse_flag = True
            else:
                coor_nowx = prev_coorx + ((movex - prev_coorx) / 8)
                coor_nowy = prev_coory + ((movey - prev_coory) / 8)
            
            # coordinatex = np.interp(coor_nowx,(50,590),(0,width))
            # coordinatey = np.interp(coor_nowy,(100,430),(0,height))            
            #check if click
            mouse_click(hand_coordinate)
            #move the mouse   
            ms.move(coor_nowx, coor_nowy)
            prev_coorx = coor_nowx
            prev_coory = coor_nowy
            cv2.rectangle(frame, (50,100),(550,330), (0,255,0), 2)
        else :
            mouse_flag = False            
        return frame
            



   
