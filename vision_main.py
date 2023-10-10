import cv2
import socket
import pickle
import numpy as np
from pyzbar.pyzbar import decode

host ='172.20.2.1'
port = 5000
max_length = 65540

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

frame_info = None
buffer = None
frame = None

print("-> waiting for connection")

while True:
    data, address = sock.recvfrom(max_length)

    if len(data) < 100:
        frame_info = pickle.loads(data)

        if frame_info:
            nums_of_packs = frame_info["packs"]

            for i in range(nums_of_packs):
                data, address = sock.recvfrom(max_length)

                if i == 0:
                    buffer = data
                else:
                    buffer += data

            frame = np.frombuffer(buffer, dtype=np.uint8)
            frame = frame.reshape(frame.shape[0], 1)

            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            frame = cv2.flip(frame, 1)

            if frame is not None and type(frame) == np.ndarray:
                cv2.imshow("Stream", frame)

                # Convert the imageFrame in
                # BGR(RGB color space) to
                # HSV(hue-saturation-value)
                # color space
                hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # Set range for red color and
                # define mask
                #red_lower = np.array([136, 87, 111], np.uint8)
                red_lower = np.array([136, 50, 50], np.uint8)
                red_upper = np.array([180, 255, 255], np.uint8)
                red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

                # Set range for green color and
                # define mask
                green_lower = np.array([25, 52, 72], np.uint8)
                green_upper = np.array([102, 255, 255], np.uint8)
                green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

                # Set range for blue color and
                # define mask
                blue_lower = np.array([94, 80, 2], np.uint8)
                blue_upper = np.array([120, 255, 255], np.uint8)
                blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

                # Morphological Transform, Dilation
                # for each color and bitwise_and operator
                # between imageFrame and mask determines
                # to detect only that particular color
                kernel = np.ones((5, 5), "uint8")

                # For red color
                red_mask = cv2.dilate(red_mask, kernel)
                res_red = cv2.bitwise_and(frame, frame,
                                          mask=red_mask)

                # For green color
                green_mask = cv2.dilate(green_mask, kernel)
                res_green = cv2.bitwise_and(frame, frame,
                                            mask=green_mask)

                # For blue color
                blue_mask = cv2.dilate(blue_mask, kernel)
                res_blue = cv2.bitwise_and(frame, frame,
                                           mask=blue_mask)

                # Creating contour to track red color
                contours, hierarchy = cv2.findContours(red_mask,
                                                       cv2.RETR_TREE,
                                                       cv2.CHAIN_APPROX_SIMPLE)

                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if (area > 300):
                        x, y, w, h = cv2.boundingRect(contour)
                        imageFrame = cv2.rectangle(frame, (x, y),
                                                   (x + w, y + h),
                                                   (0, 0, 255), 2)

                        cv2.putText(imageFrame, "Red Colour", (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                    (0, 0, 255))

                        # Creating contour to track green color
                contours, hierarchy = cv2.findContours(green_mask,
                                                       cv2.RETR_TREE,
                                                       cv2.CHAIN_APPROX_SIMPLE)

                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if (area > 300):
                        x, y, w, h = cv2.boundingRect(contour)
                        imageFrame = cv2.rectangle(frame, (x, y),
                                                   (x + w, y + h),
                                                   (0, 255, 0), 2)

                        cv2.putText(imageFrame, "Green Colour", (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1.0, (0, 255, 0))

                # Creating contour to track blue color
                contours, hierarchy = cv2.findContours(blue_mask,
                                                       cv2.RETR_TREE,
                                                       cv2.CHAIN_APPROX_SIMPLE)
                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if (area > 300):
                        x, y, w, h = cv2.boundingRect(contour)
                        imageFrame = cv2.rectangle(imageFrame, (x, y),
                                                   (x + w, y + h),
                                                   (255, 0, 0), 2)

                        cv2.putText(imageFrame, "Blue Colour", (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1.0, (255, 0, 0))

                # Program Termination
                #cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)


                #qr
                decoded_objects = decode(imageFrame)

                # Draw a rectangle around the QR code
                for obj in decoded_objects:
                    cv2.rectangle(imageFrame, obj.rect, (0, 255, 0), 2)

                    # Print the decoded data
                    data = obj.data.decode('utf-8')
                    cv2.putText(imageFrame, data, (obj.rect.left, obj.rect.top), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 255, 0), 2)

                # Show the frame
                cv2.imshow('frame', imageFrame)
                if cv2.waitKey(1) == 27:
                    break

