import cv2
import numpy as np
cap =cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,150)

myColors =[[105,72,0,144,255,255],
           [64,88,65,95,241,253],[90,48,0,118,255,255]]
myColorValues=[[255,0,0],[0,204,0],[255,0,0]]

mypoints=[]

def getContours(img):
    x,y,w,h=0,0,0,0
    contours,hierachy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)


        if area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            perimeter=cv2.arcLength(cnt,True)#perimetr

            approx=cv2.approxPolyDP(cnt,0.02*perimeter,True)#how many corner points

            #create a bounfing box around the object
            x ,y ,w ,h =cv2.boundingRect(approx)
    return x+w//2,y

def findcolor(img,myColors,myColorValues):
    count=0
    newpoints=[]
    imgHsV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHsV, lower, upper)
        #cv2.imshow(str(color[0]),mask)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count=count+1
    return newpoints

def drawoncanvas(mypoints,myColorValues):
    for point in mypoints:
        cv2.circle(imgResult,(point[0],point[1]), 10, myColorValues[point[2]], cv2.FILLED)




while True:
   success, img=cap.read()
   imgResult=img.copy()
   newpoints=findcolor(img,myColors,myColorValues)
   if len(newpoints)!=0:
       for new in newpoints:
           mypoints.append(new)
   if len(mypoints) != 0:
       drawoncanvas(mypoints,myColorValues)
   cv2.imshow("video",imgResult)
   if cv2.waitKey(1) & 0xFF ==ord('q'):
       break