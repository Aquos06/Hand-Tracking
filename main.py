import cv2
import time
from hand_tracking import Handtracking as ht
from volume import Volume 
from my_mouse import Mouse as ms
def main():
    #opening camera
    camera = cv2.VideoCapture(0)
    
    #FPS
    prevtime = 0
    currtime = 0
    detector = ht()
    volume = Volume()
    mouse = ms()
    while True:
        ret, frame = camera.read()
        #finding the hands
        frame = detector.Detecting_Hands(frame)
        
        #coordinate of the hands
        hand_coordinate = detector.Position(frame,draw = False)
        
        # print(hand_coordinate)  
        if len(hand_coordinate) != 0:
            #finding the standardev and mean of all y-axis 
            standardev_of_y, mean_of_y= volume.inilization(hand_coordinate)
            #checking the hand signq
            volume.setVolume(standardev_of_y, mean_of_y)
            #8-7 >= 15, 12-11 >= 15, 8-6 >= 50, 12-10 >= 60
            mouse.mouse_move(hand_coordinate, frame.shape, frame)
            # print(ms.mouse_click(hand_coordinate,hand_coordinate))

        #typing the FPS
        currtime = time.time()
        fps = 1/(currtime - prevtime)
        prevtime = currtime
        fps_new = "fps : " + str(int(fps))
        
        cv2.putText(frame,fps_new,(10,25),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),1)
        
        cv2.imshow("camera", frame)
        
        if cv2.waitKey(2) & 0xFF == ord("q"): 
            break
        
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()