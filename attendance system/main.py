import os
import face_recognition
import cv2
from datetime import datetime
import numpy as np
from tkinter import *
import tkinter.messagebox as msg

def facial_recog():
    names=[]
    images=[]
    origEncodeList=[]
    count=0
    path="Orignalimages"
    Orignal_images_list=os.listdir(path)
    for i in Orignal_images_list:
        image = face_recognition.load_image_file(f'{path}/{i}')
        names.append(os.path.splitext(i)[0])

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        images.append(image)
        encode = face_recognition.face_encodings(image)[0]
        origEncodeList.append(encode)
        count=count+1
    msg.showinfo("Encodding status",f'Encoddings of {count} images is done!!!')
    cap=cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        #face=cv2.resize(frame,(5,5),None,2,2)
        face=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_in_frameLoc=face_recognition.face_locations(face)
        face_in_frameEncode=face_recognition.face_encodings(face, face_in_frameLoc)
        for encodeFace,faceLoc in zip(face_in_frameEncode,face_in_frameLoc):
            comparison=face_recognition.compare_faces(origEncodeList,encodeFace)
            faceDis=face_recognition.face_distance(origEncodeList,encodeFace)
            ind=np.argmin(faceDis)
            if comparison[ind]:
                name=names[ind]
                cv2.rectangle(frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 255),3)
                cv2.putText(frame,name, (faceLoc[1], faceLoc[2]),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),2)
                with open('attendance.csv','r+') as file:
                    data=file.readlines()
                    nameList=[]


                    for line in data:
                        entry=line.split(',')
                        nameList.append(entry[0])
                    if name not in nameList:
                        time_now=datetime.now()
                        t=time_now.strftime('%H:%M:%S')
                        d=time_now.strftime('%d/%m/%y')

                        file.writelines(f'{name},{t},{d}\n')
            else:
                cv2.rectangle(frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 255),3)
                cv2.putText(frame,"NO MATCH", (faceLoc[1], faceLoc[2]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.imshow("Camera",frame)
        if cv2.waitKey(10)==13:
            break
    cap.release()

    msg.showinfo("Attendance System", "Thank you for using our system!")
    cv2.destroyAllWindows()

root=Tk()
root.title("ATTENDACE SYSTEM USING FACIAL RECOGNITION")
root.iconbitmap("icon.ico")
root.minsize(500,520)
root.maxsize(500,520)
mainFrame=Frame(root,borderwidth="20",relief=SUNKEN,bg="black")
mainFrame.pack()

topFrame=Frame(mainFrame, bg="black",borderwidth="5",relief=RIDGE)
topFrame.pack(side=TOP,pady="20",padx="30")
labelTopFrame=Label(topFrame, text="CASE Attendace System",bg="blue",fg="white",font=("Verdana",15,"bold"),pady="5",padx="7")
labelTopFrame.pack()


photo=PhotoImage(file="facialrecognition.png")
imageLabel=Label(mainFrame,image=photo,borderwidth="3",bg="black")
imageLabel.pack(side="top",padx="30")
buttomFrame=Frame(mainFrame,borderwidth="5",relief=RAISED)
buttomFrame.pack(pady="50")
buttonLabel=Button(buttomFrame,fg="white",text="START",bg="black",font=("verdana",12,"bold"),command=facial_recog)
buttonLabel.pack()
time_now=datetime.now()
d=time_now.strftime("%d/%m/%y")
noteFrame=Frame(mainFrame,bg="grey")
noteFrame.pack()
noteLabel=Label(noteFrame,text=f'Note: Press ENTER to end\t\t\t\t\tDate: {d}',bg="blue",fg="white",font=("Verdana",7,"bold"),padx="200")
noteLabel.pack()



root.mainloop()