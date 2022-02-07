import cv2
import mediapipe as mp
import time


class Handtracking(object):
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.7, trackCon = 0.5):
        self.mode = mode
        self.maxHands = 2
        self.detectionCon = 0.5
        self.trackCon = 0.5
        
        #object for hand detections
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        
    def Detecting_Hands(self,frame, draw = True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
         
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw :    
                    self.mpDraw.draw_landmarks(frame, handlms, 
                                               self.mpHands.HAND_CONNECTIONS)
        return frame
    
    def Position(self, frame, handID = 0, draw = True):
        coordinatlist = []

        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handID]
            for id, lm in enumerate(myhand.landmark):
                #finding the coordinate
                h,w,c = frame.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                coordinatlist.append([id,cx,cy])
                
                if draw :
                    cv2.circle(frame, (cx,cy), 5, (255,0,255), cv2.FILLED)
                    
        return coordinatlist


def main():
    #opening camera
    camera = cv2.VideoCapture(0)
    
    #FPS
    prevtime = 0
    currtime = 0
    detector = Handtracking()
    
    while True:
        ret, frame = camera.read()
        
        #finding the hands
        detector.Detecting_Hands(frame)
        
        #typing the FPS
        currtime = time.time()
        fps = 1/(currtime - prevtime)
        prevtime = currtime
        fps_new = "fps : " + str(int(fps))
        
        cv2.putText(frame,fps_new,(10,25),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
        
        cv2.imshow("camera", frame)
        
        if cv2.waitKey(2) & 0xFF == ord("q"):
            break
        
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()