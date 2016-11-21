import cv2
import time

def camara():
    
    faceCascade = cv2.CascadeClassifier('/media/pi/DANIEL2/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)
    ladron=False
    while not ladron:
        _, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            print "Encontre una cara"
            cv2.imwrite('save/fotoLadron.png',frame)
            ladron=True
        
        #cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
    return

def foto():
    video_capture = cv2.VideoCapture(0)
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('save/fotoManual.png',frame)
    video_capture.release()
    cv2.destroyAllWindows()
    return
