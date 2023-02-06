import cv2
import os
import shutil
from email_sender import send_email
from threading import Thread

def clean_folder():
        shutil.rmtree("images")
        os.mkdir("images")

# Start viedo capturing
video = cv2.VideoCapture(0)

if os.path.exists("images"):
    clean_folder()
else:
    os.mkdir("images")

first_frame = None
status_list = [0, 0]

# Check whether camera is working
check = False
while check == False:
    check, frame = video.read()
count = 1
while True:
    stat = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 70, 255, cv2.THRESH_BINARY)[1]
    dilated_frame = cv2.dilate(thresh_frame, None, iterations=4)

    cont, con_check = cv2.findContours(
        dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cont:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, h+y), (0, 0, 255), 3)
        if rectangle.any():
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            stat = 1

    status_list.append(stat)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        
        last_image_number = len(os.listdir("images"))
        path = f"images/{last_image_number//2}.png"
        
        email_thread = Thread(target=send_email,args=(path,))
        email_thread.daemon = True
        
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()
        clean_thread.start()
        
        count = 1

    cv2.imshow("yes", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
