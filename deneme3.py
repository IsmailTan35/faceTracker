from PIL.Image import EXTENSION
import cv2
import os
from PIL import ImageGrab
import numpy as np
from datetime import datetime
import face_recognition
import glob
from deepface import DeepFace

def createPictureFace(path,image,location):
    try:
        cv2.imwrite(os.path.join(path , 'unknown'+str(datetime.now()).replace(" ","").replace(".","-").replace(":","-")+'.jpg'),image[location[0]-20:location[2]+10,location[3]-10:location[1]+10])       
    except ValueError:
        print(ValueError)

def createFacePointer(image,location,color):
        cv2.rectangle(image,(location[1],location[0]),(location[3],location[2]),color,2)
        cv2.rectangle(image,(location[1]+1,location[2]),(location[3]-1,location[2]+10),color,-1)
        cv2.line(image,(location[1]+1,location[2]+10),(location[1]+10,location[2]+20),color,1)
        cv2.line(image,(location[1]+10,location[2]+20),(location[1]+20,location[2]+20),color,1)

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

def pictureEncode(image,location,path):
    try:
        unknown_encoding = face_recognition.face_encodings(image[location[0]-20:location[2]+10,location[3]-10:location[1]+10])
        for checkPicture in glob.glob("./face/unknown/*.jpg"):
            known_image = face_recognition.load_image_file(checkPicture)
            know_encoding = face_recognition.face_encodings(known_image)[0]
            results = face_recognition.compare_faces(know_encoding, unknown_encoding)
            if(results==True):
                print(results)
                return "yes"
        if(results==False):
            createPictureFace(path,image[location[0]-20:location[2]+10,location[3]-10:location[1]+10])
            return "not found"
            
    except:
        return "not found"

def findFaceAge(image,result,location):
    try:
        deneme =DeepFace.analyze(img_path=image,actions=["age"])
        deneme2 = deneme["age"]
    except:
        deneme2 = "null"
    
    createPutText(image,str(deneme2)+" "+result,
        (location[4],location[3]+10), 
        0.5,
        (255,255,255))


# os.mkdir(os.path.join("./", "Deneme"), 0o666)
# os.rmdir("./Deneme")
# if os.path.exists("./face/grup"):
#     print("yes")
# else:
#     print("no")

def Main():
    font                   = cv2.FONT_HERSHEY_COMPLEX
    bottomLeftCornerOfText = (50,50)
    bottomLeftCornerOfText2 = (50,100)
    fontScale              = 0.5
    fontScale2              = 0.9
    fontColor              = (255,255,255)
    lineType               = 1
    toplam=0
    path= "./face/unknown"
    color=(100,184,101)
    while True:
        img_final=catchScreen()
        denem=face_recognition.face_locations(img_final)
        sayac=0
        
        for location in denem :
            result =""
            toplam=toplam+1
            sayac= sayac+1

            createFacePointer(img_final,location,color)

            result=pictureEncode(img_final,location,path)

            # findFaceAge(img_final,result,location)
        
        cv2.rectangle(img_final,(35,10),(250,125),color,-1)

        createPutText(img_final,"Anlik: "+str(sayac),bottomLeftCornerOfText, 
                    fontScale,
                    fontColor)

        createPutText(img_final,"Toplam: "+str(toplam),bottomLeftCornerOfText2, 
                    fontScale,
                    fontColor)

        cv2.imshow("Face Catcher",img_final)
        if(cv2.waitKey(3)==ord('0')):
            cv2.destroyAllWindows()
            break
Main()