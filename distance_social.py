# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:57:21 2020

@author: KIIT
"""

import cv2
import math

cap = cv2.VideoCapture(0)

face_model = cv2.CascadeClassifier('D:/AnacondaInstall/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

print("******************************************************")
print("         Welcome to the Social Distancing App         ")
print("******************************************************")
print("\n")

print("For this model initial calibration was done by taking width of object to be 17cm and the distance of 30cm away from camera so as to calculate the focal length. And then this focal length was used for calculating distance between the object and camera.")

while True:    
    centroid = []
    person_in_contact=""
    status,photo = cap.read()
    face_cor = face_model.detectMultiScale(photo)
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    text="Total Face Detected " +str(len(face_cor))
    centroid.clear()
    i = 1
    if len(face_cor) == 0:
        pass
    else:
        for (x,y,w,h) in face_cor:    
            x1 = x
            y1 = y
            x2 = x + w
            y2 = y + h
            centroid.append((int((x2+x1)/2), int((y2+y1)/2)))
            #distance was calculated using focal length. focal length = 400cm. Focal_length = (Pixcel_width x  Distance from camera) / Width of obejct . width =17cm distance=30cm, pixcel=200px
            dis = "dis= " + "{:.2f}".format(17*400/(x2-x1)) + " cm"
            cv2.rectangle(photo, (x1,y1), (x2,y2), [0,255,0], 3)
            cv2.putText(photo, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
            cv2.putText(photo, dis, (x1,y2-10), font, 0.65, (0,255,0), thickness)
            cv2.circle(photo, centroid[i-1], 4, (0, 255, 0), -1)
            cv2.putText(photo, f'Id: {i}', (int((x2+x1)/2)-10, int((y2+y1)/2)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            i += 1
        for i in range(len(centroid)):
            for j in range(i+1, len(centroid)):
                d = math.sqrt( ((centroid[j][1]-centroid[i][1])**2)+((centroid[j][0]-centroid[i][0])**2) )
                dP = "{:.2f}".format(17*400/d) + " cm"
                print("ID:",i+1,"- ID:",j+1,"=",dP)
                
                cv2.line(photo, (centroid[i][0], centroid[i][1]), (centroid[j][0], centroid[j][1]), (0, 0, 255), 2)
                cv2.putText(photo, dP, (int((centroid[i][0]+centroid[j][0])/2),int((centroid[i][1]+centroid[j][1])/2)-10), font, 0.65, (0,255,0), 2)
                if (17*400/d) < 40 :
                    person_in_contact += "Person "+str(i+1)+" and Person "+str(j+1)+" ; "
                    person_in_contact += " are not following social distancing "
                    print(person_in_contact)
                    print("!!  ALERT  !!")
        cv2.imshow('hi', photo)
        if cv2.waitKey(5) == 13:
            break
cv2.destroyAllWindows()

cap.release()