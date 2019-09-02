from tkinter import *
import numpy as np
import cv2
from playsound import playsound

mainSceen = Tk() 
mainSceen.geometry('300x150')
mainSceen.title("Bubble Detector")
alarmSound=False

def startWaterproof():
    cap = cv2.VideoCapture(0)   #"VID_20190816_204237.mp4" for video / 0 for webcam / 1 for external camera
    bubbles = 0
    time=0

    while(1):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)  
        edges = cv2.Canny(gray_blur,25,50)

        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1.5, 100,maxRadius=150)
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            bubbles -=1
            for (x, y, r) in circles:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                bubbles +=1
                
        print("Bubbles")
        print(bubbles)        
        time+=1
        print("time:")
        print(time)
        cv2.imshow('frame',frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            label['text'] = 'Beklemede'
            label['bg'] = "lightgray"
            label['fg'] = "black"
            break
        elif bubbles>15:
            label['text'] = 'Alarm'
            label['bg'] = "red"
            label['fg'] = "white"
            playsound('alarmsound.mp3',False)
            alarmSound=True
            break
        elif time==200:
            label['text'] = 'Test Başarılı'
            label['bg'] = "green"
            alarmSound=False
            break

    cap.release()
    cv2.destroyAllWindows()


label = Label(mainSceen,font=(None, 20),pady=20,width=100,text ="Beklemede")
label.pack()

button1 = Button(text='Başlat',font=(None, 15), command=startWaterproof)
button1.pack(pady=20)

mainSceen.mainloop() 


