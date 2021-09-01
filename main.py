import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while True:
    area_red = 0
    area_green = 0

    _, frame = cap.read()
    blurred_frame = cv2.medianBlur(frame, 15)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    windowWidth = frame.shape[1]
    windowHeight = frame.shape[0]

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

    if len(contours_red) != 0:
        for contour in contours_red:
            area = cv2.contourArea(contour)
            if area > 8000:
                cv2.drawContours(frame, contour, -1, (255, 0, 0), 3)
                area_red = area

    if len(contours_green) != 0:
        for contour in contours_green:
            area = cv2.contourArea(contour)
            if area > 8000:
                cv2.drawContours(frame, contour, -1, (255, 0, 0), 3)
                area_green = area

    if area_red > area_green:
        if len(contours_red) != 0:
            c = max(contours_red, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            red_x_midpt = (x + x + w) / 2
            red_y_midpt = (y + y + h) / 2
            print(red_x_midpt, red_y_midpt)
            if red_x_midpt > windowWidth / 5:
                print("Turn right")
            else:
                print("Go straight")

    elif area_green > area_red:
        if len(contours_green) != 0:
            c = max(contours_green, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            green_x_midpt = (x + x + w) / 2
            green_y_midpt = (y + y + h) / 2
            print(green_x_midpt, green_y_midpt)
            if green_x_midpt < windowWidth / 5 * 4:
                print("Turn left")
            else:
                print("Go straight")

    cv2.imshow("red mask", mask_red)
    cv2.imshow("green mask", mask_green)
    cv2.imshow("frame", frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()