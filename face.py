import cv2

cascPath = "./data/haarcascade_frontalface_alt.xml"
eyePath = "./data/haarcascade_eye_tree_eyeglasses.xml"

faceCascade = cv2.CascadeClassifier(cascPath)
eyeCascade = cv2.CascadeClassifier(eyePath)

testImage = "matt.jpg"

def get_face(image):
    eye_list = []
    frame = cv2.imread(image)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(frame)
    for (x, y, w, h) in faces:
        faceROI = frame[y:y+int(h/2), x:x+w]
        eyes = eyeCascade.detectMultiScale(faceROI)
        for (x2, y2, w2, h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            eye_radius = int(round((w2 + h2)*0.25))
            eye_list.append(tuple(list(eye_center)+[eye_radius]))
    return eye_list

def resize_img(filename):
    frame = cv2.imread(filename)
    W = 1000.
    _, width, _ = frame.shape
    imgScale = W/width
    newX,newY = frame.shape[1]*imgScale, frame.shape[0]*imgScale
    frame = cv2.resize(frame,(int(newX),int(newY)))
    filename = "new" + filename
    cv2.imwrite(filename,frame)


if __name__ == "__main__":
    eye_list = get_face(testImage)
    resize_img(testImage)
    print(eye_list)
