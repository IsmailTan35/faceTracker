from PIL.Image import EXTENSION
import cv2
import os
from PIL import ImageGrab,Image
import numpy as np
from datetime import datetime
import glob
from deepface import DeepFace
import math
import face_recognition
# os.rmdir("./Deneme")

def createPictureFace(path,image,location):
    try:
        cv2.imwrite(os.path.join(path , 'unknown'+str(datetime.now()).replace(" ","").replace(".","-").replace(":","-")+'.jpg'),image)      
    except:
        print("denen")

def createFacePointer(image,location,color):
    cv2.rectangle(image,(location[1],location[0]),(location[3],location[2]),color,2)
    cv2.rectangle(image,(location[1],location[2]),(location[3],location[2]+20),color,-1)
    cv2.line(image,(location[0]+location[2]-1,location[1]+location[3]+20),(location[0]+location[2]+14,location[1]+location[3]+35),color,2)
    cv2.line(image,(location[0]+location[2]+14,location[1]+location[3]+35),(location[0]+location[2]+25,location[1]+location[3]+35),color,2)
    cv2.imshow("Face Catcher",image)

def createPutText(image,text,textLocation,fontScale,fontColor):
    cv2.putText(image,str(text), 
                textLocation, 
                cv2.FONT_HERSHEY_COMPLEX, 
                fontScale,
                fontColor,
                1)

def catchScreen():
    img=ImageGrab.grab(bbox=(0,0,1080,1080))
    img_np=np.array(img)
    img_final=cv2.cvtColor(img_np,cv2.COLOR_BGR2RGB)
    return img_final

def pictureEncode(image,path,unknown_locations,color):
    try:
        # createFacePointer(image,unknown_locations,color)
        unknown_encoding = face_recognition.face_encodings(image)
        for (j,location) in zip(unknown_encoding,unknown_locations):
            for i in glob.glob("./face/unknown/*.jpg"):
                known_image = face_recognition.load_image_file(i)
                memoryPicture_encoding = face_recognition.face_encodings(known_image)[0]
                results = face_recognition.compare_faces([j], memoryPicture_encoding)
                if(results=={True}):
                    print("asdasda")
            if(results==[False]):
                print("asd")
                img = Image.fromarray(image, 'RGB')
                img_cropped = img.crop((location[3], location[0], location[1], location[2]))
                img_np=np.array(img_cropped)
                img_final=cv2.cvtColor(img_np,cv2.IMREAD_COLOR)
                createPictureFace(path,img_final,location)

        # drawPicture(image[location[1]:location[1]+location[3],location[0]:location[0]+location[2]])
        # createPictureFace("./face/memory",image,location)
    except :
        print("TypeError")
    return "quit"

def findFaceAge(image,result,location):
    try:
        deneme =DeepFace.analyze(img_path=image,actions=["age"])
        deneme2 = deneme["age"]
    except:
        deneme2 = "null"
    
    createPutText(image,str(deneme2)+" "+result,
        (location[0],location[2]+10), 
        0.5,
        (255,255,255))

def createFolder():
    if not os.path.exists("./face"):
        os.mkdir(os.path.join("./", "face"), 0o666)
        os.mkdir(os.path.join("./face", "unknown"), 0o666)
        os.mkdir(os.path.join("./face", "memory"), 0o666)


def drawPicture(image,counter,total):
    cv2.rectangle(image,(35,10),(250,125),(100,184,101),-1)
    createPutText(image,"Anlik: "+str(counter),(50,50), 
                    0.5,
                    (255,255,255))

    createPutText(image,"Toplam: "+str(total),(50,100), 
                0.5,
                (255,255,255))
    winname = "Face Catcher"
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, 1500,30) 
    cv2.imshow(winname,image)

def decodeFace(program,image,color,path,total,counter):
    for location in program :
        total=total+1
        counter= counter+1
            # findFaceAge(img_final,result,location)
        createFacePointer(image,location,color)

def decodewhileFace(program,image,color,path,total,counter):
    while True:
        res = pictureEncode(image,path,program,color)
        
        if(res=="quit"):
            break
        # findFaceAge(img_final,result,location)
            
        if(cv2.waitKey(1)==ord('5')):
                break

def Main():
    createFolder()
    total=0
    path= "./face/unknown"
    color=(100,184,101)
    while True:
        img_final=catchScreen()
        program = face_recognition.face_locations(img_final)
        counter=0
        drawPicture(img_final,counter,total)
        if (cv2.waitKey(1)==ord('5')):
                decodewhileFace(program,img_final,color,path,total,counter)  
        else:
            decodeFace(program,img_final,color,path,total,counter)
        drawPicture(img_final,counter,total)
        if(cv2.waitKey(3)==ord('0')):
            cv2.destroyAllWindows()
            break
Main()