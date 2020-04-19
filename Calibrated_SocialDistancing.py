# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:57:21 2020

@author: VISHAL
"""

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

#print("For this model initial calibration was done by taking width of object to be 17cm and the distance of 30cm away from camera so as to calculate the focal length. And then this focal length was used for calculating distance between the object and camera.")


def calibration(distance, width_of_face):
    count = 0
    pixcel_width = 0
    while count<20:
        _ , photo = cap.read()
        face_cor = face_model.detectMultiScale(photo)

        if len(face_cor) == 0:
            pass
        else:
            pixcel_width += face_cor[0][2]
            cv2.rectangle(photo, (face_cor[0][0],face_cor[0][1]), (face_cor[0][0] + face_cor[0][2], face_cor[0][1] + face_cor[0][3]), [0,255,0], 3)
            count += 1
        cv2.imshow('hi', photo)
        cv2.waitKey(5)
    cv2.destroyAllWindows()
    pixcel_width /= 20
    #cap.release()
    return ((pixcel_width * distance) / width_of_face)

def distanceCAL(width_of_face, focal_length, perWidth):
    #returning distance in inches
    return ((width_of_face * focal_length) / perWidth)

width_of_face = 20      #approximate value of bonding width we cover

print("CALIBRATION STARTED Stand at the mark at the distance of x centimeter from the camera and press 1")
if (input() == '1'):
    x = int(input("Enter the distance in cm: "))
    focal_length = calibration(x, width_of_face)

while True:    
    centroid = []
    person_in_contact=""
    status,photo = cap.read()
    photo = cv2.resize(photo,(400,400), interpolation = cv2.INTER_AREA)
    face_cor = face_model.detectMultiScale(photo)
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 1
    color = (0, 255, 0)
    thickness = 2
    text="Total Face Detected " +str(len(face_cor))
    centroid.clear()
    i = 1
    BirdImage = cv2.imread('C:/Users/KIIT/Desktop/eagle.jpg')
    BirdImage = cv2.resize(BirdImage,(400,400), interpolation = cv2.INTER_AREA)
    img = 0*cv2.imread('C:/Users/KIIT/Desktop/Black_photo.jpg')
    img = cv2.resize(img,(800,800), fx=800,fy=800, interpolation = cv2.INTER_AREA)
    alert = " "
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
            dis = "dis= " + "{:.2f}".format(distanceCAL(width_of_face, focal_length, (x2-x1))) + " cm"
            cv2.rectangle(photo, (x1,y1), (x2,y2), [0,255,0], 3)
            cv2.putText(photo, dis, (x1,y2-10), font, 0.65, (0,255,0), thickness)
            cv2.circle(photo, centroid[i-1], 4, (0, 255, 0), -1)
            cv2.circle(BirdImage, centroid[i-1], 4, (0, 0, 255), -1)
            cv2.putText(photo, f'Id: {i}', (int((x2+x1)/2)-10, int((y2+y1)/2)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            i += 1
        for i in range(len(centroid)):
            for j in range(i+1, len(centroid)):
                color = [0,255,0]
                d = math.sqrt( ((centroid[j][1]-centroid[i][1])**2)+((centroid[j][0]-centroid[i][0])**2) )
                dP = "{:.2f}".format(distanceCAL(width_of_face, focal_length, d)) + " cm"
                show = "ID:"+ str(i+1) + "- ID:" + str(j+1) + "=" +str(dP)
                print(show)
                #run if person is not maintaing social distancing 
                if (distanceCAL(width_of_face, focal_length,d)) < 40 :
                    color = [0,0,255]
                    person_in_contact += "Person " + str(i+1) + " and Person "+str(j+1)
                    person_in_contact += " are not following social distancing "
                    print(person_in_contact)
                    alert = "!!  ALERT PERSONS ARE IN CONTACT !!"
                    print(alert)
                
                cv2.line(photo, (centroid[i][0], centroid[i][1]), (centroid[j][0], centroid[j][1]), color, 2)
                cv2.putText(img, show, (50,450+j*25+i*25), font, 0.65, color, thickness)
                cv2.putText(photo, dP, (int((centroid[i][0]+centroid[j][0])/2),int((centroid[i][1]+centroid[j][1])/2)-10), font, 0.65, color, 2)
        img[0:400,0:400]= photo 
        img[0:400,400:800]= BirdImage
        cv2.putText(img, text, (300,410), font, 0.65, color, thickness)
        cv2.putText(img, alert, (100,700), font, 0.65, color, thickness)
        
        cv2.imshow("Social_Distancing with Eagle's Eye Map", img)
        if cv2.waitKey(5) == 13:
            break
cv2.destroyAllWindows()

cap.release()
