import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()
    blurred_frame = cv2.medianBlur(frame, 15)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 30])
    upper_red = np.array([5, 255, 255])
    mask_red_1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([175, 100, 30])
    upper_red = np.array([180, 255, 255])
    mask_red_2 = cv2.inRange(hsv, lower_red, upper_red)

    lower_green = np.array([40, 100, 30])
    upper_green = np.array([80, 255, 255])

    mask_red = mask_red_1 + mask_red_2
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area > 8000:
            cv2.drawContours(frame, contour, -1, (255,0,0), 3)

    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area > 8000:
            cv2.drawContours(frame, contour, -1, (0,255,0), 3)

    cv2.imshow("red mask", mask_red)
    cv2.imshow("green mask", mask_green)
    cv2.imshow("frame", frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()