# USAGE
# sudo python3 pi_face_recognition_exit_main.py --cascade haarcascade_frontalface_default.xml --encodings encodings.json

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import json
import time
import chardet
import cv2
import os
import datetime
import xlsxwriter


def FaceRecOut():
    
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", required=True,
        help = "path to where the face cascade resides")
    ap.add_argument("-e", "--encodings", required=True,
        help="path to serialized db of facial encodings")
    ap.add_argument("-i", "--dataset", required=False,
        help="path to input directory of faces + images")
    ap.add_argument("-d", "--detection-method", type=str, default="cnn",
        help="face detection model to use: either `hog` or `cnn`")
    args = vars(ap.parse_args())

    # load the known faces and embeddings along with OpenCV's Haar
    # cascade for face detection
    print("[INFO] loading encodings + face detector...")
    #data = json.loads(open(args["encodings"]).read())
    detector = cv2.CascadeClassifier(args["cascade"])

    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    # start the FPS counter
    fps = FPS().start()

    writeDataBool = True
    endDateData = []
    currDate = str(datetime.datetime.now().date())
    with open(currDate+".json", "r") as read_file:
            endDateData = json.load(read_file)
    print(endDateData)
    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        if writeDataBool:
        
            frame = imutils.resize(frame, width=500)
    
        # convert the input frame from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect faces in the grayscale frame
            rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                minNeighbors=5, minSize=(150, 150),
                flags=cv2.CASCADE_SCALE_IMAGE)

        # OpenCV returns bounding box coordinates in (x, y, w, h) order
        # but we need them in (top, right, bottom, left) order, so we
        # need to do a bit of reordering
            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []
            
        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            lastNum = ""
            countNum = 0
            with open("number.json", "r") as read_file:
                        data = json.load(read_file)
                        lastNum = str(data["number"])
            countNum = int(lastNum)
            counter = 1
            while counter < countNum:
                countStr = str(counter)
                try:
                    with open(countStr+".json", "r") as read_file:
                            data = json.load(read_file)
                except:
                    counter += 1
                    countStr = str(counter)
                    break
                matches = face_recognition.compare_faces(data["encodings"],
                    encoding)
                name = "Unknown"
                counter += 1
                # check to see if we have found a match
                if True in matches:
                
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    if writeDataBool:
                        name = max(counts, key=counts.get)
                        enter_currTime = str(datetime.datetime.now().time())
                        # update the list of names
                        names.append(name)
                        for item in endDateData:
                            if item["İsim"] == name:
                                item["Çıkış saati"] = str(datetime.datetime.now().time())
                        writeDataBool = False
                
                        # loop over the recognized faces
                        for ((top, right, bottom, left), name) in zip(boxes, names):
                            # draw the predicted face name on the image
                            cv2.rectangle(frame, (left, top), (right, bottom),
                                (0, 255, 0), 2)
                            y = top - 15 if top - 15 > 15 else top + 15
                            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, (0, 255, 0), 2)

        # display the image to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF


        if key == ord("k"):
            writeDataBool = True
    
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            enter_currDate = str(datetime.datetime.now().date())
            with open(enter_currDate+".json", "w") as d:
                json.dump(endDateData, d, ensure_ascii = False)
            
            workbook = xlsxwriter.Workbook('/../../../../media/pi/LUNAWINDOWS/'+enter_currDate+'.xlsx')
            worksheet = workbook.add_worksheet()
        
            row = 0
            col = 0
            worksheet.write(row, col, "Isim")
            worksheet.write(row, col+1, "Giris Saati")
            worksheet.write(row, col+2, "Cikis Saati")
            worksheet.write(row, col+3, "Toplam Saat")
            row = 1
            col = 0
            for item in endDateData:
                worksheet.write(row, col, item["İsim"])
                row += 1
            row = 1
            col = 1            
            for item in endDateData:
                worksheet.write(row, col, item["Giriş saati"])
                row += 1
            row = 1
            col = 2            
            for item in endDateData:
                worksheet.write(row, col, item["Çıkış saati"])
                row += 1
            row = 1
            col = 3            
            for item in endDateData:
                valEnt = datetime.datetime.strptime(item["Giriş saati"], '%H:%M:%S.%f')
                valOut = datetime.datetime.strptime(item["Çıkış saati"], '%H:%M:%S.%f')
                sumHour =  valOut - valEnt
                print(str(sumHour))
                worksheet.write(row, col, str(sumHour))
                row += 1
            
            workbook.close()
            
            os.remove(enter_currDate+".json")
        
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
