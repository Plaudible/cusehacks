import cv2

cascPath = "./data/haarcascade_frontalface_alt.xml"
eyePath = "./data/haarcascade_eye_tree_eyeglasses.xml"

faceCascade = cv2.CascadeClassifier(cascPath)
eyeCascade = cv2.CascadeClassifier(eyePath)

testImage = "matt.jpg"


def show_camera():
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        # frame = cv2.imread(testImage)


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=0
        )

        # eye = eyeCascade.detectMultiScale(
        #     gray,
        #     scaleFactor=1.1,
        #     minNeighbors=5,
        #     minSize=(30, 30),
        #     flags=0
        # )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            faceROI = gray[y:y+int(h/2), x:x+w]
            eyes = eyeCascade.detectMultiScale(faceROI)
            for (x2, y2, w2, h2) in eyes:
                eye_center = (x + x2 + w2//2, y + y2 + h2//2)
                radius = int(round((w2 + h2)*0.25))
                frame = cv2.circle(frame, eye_center, radius, (255, 0, 0), 4)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        scale_percent = 100  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)

        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Display the resulting frame
        cv2.imshow('Video', frame)


def get_face(image):
    eye_list = []
    frame = cv2.imread(image)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=0
    )
    for (x, y, w, h) in faces:
        faceROI = gray[y:y+int(h/2), x:x+w]
        eyes = eyeCascade.detectMultiScale(faceROI)
        for (x2, y2, w2, h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            eye_radius = int(round((w2 + h2)*0.25))
            frame = cv2.circle(frame, eye_center, eye_radius, (255, 0, 0), 4)
            
            eye_list.append(tuple(list(eye_center)+[eye_radius]))
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return eye_list

def resize_img(filename):
    oriimg = cv2.imread(filename)
    W = 1000.
    _, width, _ = oriimg.shape
    imgScale = W/width
    newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
    newimg = cv2.resize(oriimg,(int(newX),int(newY)))
    filename = "new" + filename
    cv2.imwrite(filename,newimg)


# show_camera()
eye_list = get_face(testImage)
resize_img(testImage)
print(eye_list)
