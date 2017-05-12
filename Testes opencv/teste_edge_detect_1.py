import cv2
import numpy as np
import time

# Open Camera object
cap = cv2.VideoCapture(0)

# Decrease frame size


def nothing(x):
    pass


# Function to find angle between two vectors
def Angle(v1, v2):
    dot = np.dot(v1, v2)
    x_modulus = np.sqrt((v1 * v1).sum())
    y_modulus = np.sqrt((v2 * v2).sum())
    cos_angle = dot / x_modulus / y_modulus
    angle = np.degrees(np.arccos(cos_angle))
    return angle


# Function to find distance between two points in a list of lists
def FindDistance(A, B):
    return np.sqrt(np.power((A[0][0] - B[0][0]), 2) + np.power((A[0][1] - B[0][1]), 2))


# Creating a window for HSV track bars
cv2.namedWindow('HSV_TrackBar')

# Starting with 100's to prevent error while masking
h, s, v = 100, 100, 100


# Creating track bar
cv2.createTrackbar('up', 'HSV_TrackBar', 150, 179, nothing)
cv2.createTrackbar('lower', 'HSV_TrackBar', 230, 255, nothing)


while (1):

    upper = cv2.getTrackbarPos('up','HSV_TrackBar')
    lower = cv2.getTrackbarPos('lower','HSV_TrackBar')

    print((upper,lower))
    # Measure execution time

    # Capture frames from the camera
    ret, frame = cap.read()

    # Blur the image
    blur = cv2.blur(frame, (3, 3))

    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    edges = cv2.Canny(gray, lower, upper)




    # Draw Contours
    #cv2.drawContours(frame, contours, -1, (122,122,0), 3)
    cv2.imshow("edge", edges)
    cv2.imshow("Frame",frame)

    # close the output video by pressing 'ESC'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()