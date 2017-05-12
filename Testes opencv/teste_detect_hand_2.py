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
cv2.createTrackbar('h', 'HSV_TrackBar', 150, 179, nothing)
cv2.createTrackbar('s', 'HSV_TrackBar', 230, 255, nothing)
cv2.createTrackbar('v', 'HSV_TrackBar', 225, 255, nothing)

while (1):

    h = cv2.getTrackbarPos('h','HSV_TrackBar')
    s = cv2.getTrackbarPos('s','HSV_TrackBar')
    v = cv2.getTrackbarPos('v','HSV_TrackBar')

    print((h,s,v))
    # Measure execution time
    start_time = time.time()

    # Capture frames from the camera
    ret, frame = cap.read()

    # Blur the image
    blur = cv2.blur(frame, (3, 3))

    # Convert to HSV color space
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Create a binary image with where white will be skin colors and rest is black
    mask2 = cv2.inRange(hsv, np.array([2, 80, 80]), np.array([h, s, v]))

    # Kernel matrices for morphological transformation
    kernel_square = np.ones((11, 11), np.uint8)
    kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # Perform morphological transformations to filter out the background noise
    # Dilation increase skin color area
    # Erosion increase skin color area
    dilation = cv2.dilate(mask2, kernel_ellipse, iterations=1)
    erosion = cv2.erode(dilation, kernel_square, iterations=1)
    dilation2 = cv2.dilate(erosion, kernel_ellipse, iterations=1)
    filtered = cv2.medianBlur(dilation2, 5)



    # Find contours of the filtered frame
    #im2,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw Contours
    #cv2.drawContours(frame, contours, -1, (122,122,0), 3)
    cv2.imshow("Mask - in range", mask2)
    cv2.imshow("Frame",frame)

    # close the output video by pressing 'ESC'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()