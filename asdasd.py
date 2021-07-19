import cv2

yuzprogrami = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
gozprogrami = cv2.CascadeClassifier("haarcascade_eye.xml")
resim = cv2.imread("test.jpg")

griresim = cv2.cvtColor(resim,cv2.COLOR_BGR2GRAY)

program = yuzprogrami.detectMultiScale(griresim,1.3,3)
gozprogram = gozprogrami.detectMultiScale(griresim,1.3,3)
for (a,b,c,d) in program :
    cv2.rectangle(resim,(a,b),(a+c,b+d),(0,0,255),2)
for (a,b,c,d) in gozprogram :
    cv2.rectangle(resim,(a,b),(a+c,b+d),(0,0,255),2)

cv2.imshow("kapatmak için herhangi bir tuşa basiniz",resim)

cv2.waitKey(0)
cv2.destroyAllWindows()
