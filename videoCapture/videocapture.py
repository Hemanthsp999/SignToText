import cv2

# Basic video capturing
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:

    ret, img = cap.read()
    cv2.imshow('WebCam', img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
