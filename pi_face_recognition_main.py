#!/usr/bin/env python3

# USAGE
# python3 pi_face_recognition_main.py --cascade haarcascade_frontalface_default.xml --encodings encodings.json

# import the necessary packages
import mesaagee
from imutils.video import VideoStream
from imutils.video import FPS
from googleapiclient.discovery import build  
from httplib2 import Http  
from oauth2client import file, client, tools  
from oauth2client.service_account import ServiceAccountCredentials
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import tkinter as tk
import numpy as np
import tkinter.messagebox
import gui as gui
import face_recognition
import argparse
import imutils
import pickle
import json
import time
import chardet
import cv2
import datetime
import msgbox

root1=tk.Tk()
root1.withdraw()

root2=tk.Tk()
root2.withdraw()

root=tk.Tk()
root.withdraw()

formenConf = False
writeDataBool = True

run = True

endDateData = []
endDataSheet = []

MY_SPREADSHEET_ID = '1y-J0WfXE7Yc1T4_gV8P7SmNAb-qUffZR0y-cIGodcRc'

def mbox(msg, b1, b2, parent, cbo=False, cboList=[]):
    msgbox = MessageBox(msg, b1, b2, parent, cbo, cboList)
    msgbox.root.mainloop()
    msgbox.root.destroy()
    return msgbox.returning

def FormenTrue():
    global formenConf
    formenConf = True

def FormenFalse():
    global formenConf
    formenConf = False
    
def ReadCard():               #Reads data from rfid reader
    GPIO.setwarnings(False)     
    reader = SimpleMFRC522()
        
    try:
        id, text = reader.read()
        return text
    except:
        return None
    finally:
        GPIO.cleanup()
        
    
def UpdateSheet(date, name, surname, tc, job, comp, enter, f):
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    creds = ServiceAccountCredentials.from_json_keyfile_name( 
            'Proses-e8298344399a.json', SCOPES)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API, append the next row of sensor data
    # values is the array of rows we are updating, its a single row
    fullName = name + " " + surname
    values = [ [date, fullName, tc, job, comp, enter, f] ]
    body = { 'values': values }
    # call the append API to perform the operation
    result = service.spreadsheets().values().append(
                spreadsheetId=MY_SPREADSHEET_ID, 
                range='ngiriş' + '!A1:F1',
                valueInputOption='USER_ENTERED', 
                insertDataOption='INSERT_ROWS',
                body=body).execute()  

def EndProcess():
    global run
    global endDateData
    global endDataSheet
    enter_currDate = str(datetime.datetime.now().date())
    print("sheet test")
    print(endDataSheet)
    with open(enter_currDate+".json", "w") as d:
        json.dump(endDateData, d, ensure_ascii = False)
    try:
        sheetJson = []
        try:
                with open("ngsheet.json", "r") as read_file:
                    sheetJson = json.load(read_file)
                for item in sheetJson:
                    endDataSheet.append(item)
        except Exception as ar:
                print(ar)
                pass
        for item in endDataSheet:
                #UpdateSheet(enter_currDate, item["İsim"], item["Soyisim"], item["Tc"], item["Meslek"], item["Şantiye"], item["Gerçek giriş saati"], item["Formen"])
                pass
        try:
            os.remove("ngsheet.json")
        except:
                pass
    except Exception as error:
        print(error)
        #tk.messagebox.showinfo("Hata", "Veriler internet problemi nedeniyle Google Sheets'e atılamadı.")
        #root2.lift()
        #with open("ngsheet.json", "w") as d:
            #json.dump(endDataSheet, d, ensure_ascii = False)
        pass
        endDataSheet = []
    run = False

def FaceRecEnter():
    global formenConf
    global writeDataBool
    global run
    global endDateData
    global endDataSheet
    formenOnay = False
    formenOnay = formenConf
    enterF = ""
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", required=False,
        help = "path to where the face cascade resides")
    ap.add_argument("-e", "--encodings", required=False,
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
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    # vs = VideoStream(src=0).start()
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    # start the FPS counter
    fps = FPS().start()
    if formenOnay == True:
        print("waiting can be deleted later maybe")
        

    writeDataBool = True
    rfidNumber = 00
    
    currDate = str(datetime.datetime.now().date())
    try:
        with open(currDate+".json", "r") as read_file:
            endDateData = json.load(read_file)
    except:
        endDateData = []
    # loop over frames from the video file stream
    enter_currTime = ''
    run = True
    #result = tk.messagebox.askquestion("Uyarı", "Başlamak için 'yes'e çıkmak için 'no'ya basınız.")
    #root1.lift()
    result=mesaagee.message("Başlamak için bir kart okutun, çıkmak için 'Bitir'e basın.", 00)
    if result == 'yes':
        run = False
    else:
        run = True
    while run == True:
    
        timeForEnter = datetime.datetime.now().time()
        firstEnterTime = datetime.datetime.strptime('6:30', '%H:%M').time()
        lastEnterTime = datetime.datetime.strptime('8:30', '%H:%M').time()
        
        currDateTimeForEnter = datetime.datetime.now().time()
        # enter_currTime = '16:00'
        enter_currTime = '8:00'
        if currDateTimeForEnter >= firstEnterTime:
            print("pt1")
            if currDateTimeForEnter <= lastEnterTime:
                print("pt2")
                enter_currTime = '8:00'
            elif formenOnay == False:
                print("pt3")
                enter_currTime = "Geç giriş"
                #print("Giriş saatini geçtiniz lütfen formen onayını alın.")
                #run = False
                #return;
            elif formenOnay == True:
                enter_currTime = '8:00'
                enterF = 'F'
        elif formenOnay == False:
            enter_currTime = "Geç giriş"                    # buraya giriş saatini bekleyiniz mesajı koy
            #print("Giriş saatini geçtiniz lütfen formen onayını alın.")
            #run = False
            #return;
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
        
        name = "Unknown"                 #BURDA KALDIN
        surname = "Surname"
        tc = "Tc"
        job = "Job"
        comp = "Comp"
        
        readerValue = str(ReadCard())
        if readerValue != "None":
            rfidNumber = ReadCard()
        
        #cardReader = threading.Thread(target=ReadCard)
        #if cardReader.is_alive() == False:
            #cardReader.start()
        
        print("rfid: "+str(rfidNumber))
        actualIndex = None
        
        known_faces = []
        database = []
        with open("database.json", "r") as read_file:
            database = json.load(read_file)
        counter = 0
        try:#LOL
            if int(rfidNumber) != 00:
                for i in database["tc"]:
                    print("card code: "+str(rfidNumber))
                    print("i in database: "+str(i))
                    if int(i) == int(rfidNumber):
                        print("Buldu")
                        actualIndex = counter
                    else:
                        counter += 1
        except:#LOL
            pass#LOL
        print("Index :"+str(actualIndex))
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            #print(known_faces)
            #known_faces1 = known_faces.tolist()
            databasePerson = []
            known_faces = []
            try:#LOL
                print("actl Index: "+str(actualIndex))
                databasePerson.append(database["encodings"][actualIndex])
                databasePerson.append(database["encodings"][actualIndex+1])
                databasePerson.append(database["encodings"][actualIndex+2])
                databasePerson.append(database["encodings"][actualIndex+3])
            except:#LOL
                pass#LOL
            known_faces = databasePerson
                #print("Database bulunamadı")
                #known_faces = []
            #print("faces"+str(known_faces))
            matches = []
            if actualIndex != None:
                matches = face_recognition.compare_faces(known_faces,
                    encoding)
            else:
                matches = [False]
            
            print(matches)
            #print(type(known_faces1))
            #print(type(matches))
            #print(matches)
            # check to see if we have found a match
            
            trueCounter = 0
            for vari in matches:
                if vari == True:
                    trueCounter += 1
            print("trueCounter: "+str(trueCounter))
            if trueCounter >= 3:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                #matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                #counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                #for i in matchedIdxs:                           # Birden fazla kişi için bir şeyler diyor olma sebebei burası yüzünden olabilir (ilk satırdan sonra "[i] olmaması)
                 #   tc = database["tc"][i]                          # data["names"] --> match olmuş databasedeki yüzü alır 
                  #  counts[tc] = counts.get(tc, 0) + 1

                #encodeCounter -= 1
                #print(str(encodeCounter))
                surname = database["surname"][actualIndex]
                name = database["names"][actualIndex]
                job = database["job"][actualIndex]
                comp = database["comp"][actualIndex]
                tc = database["tc"][actualIndex]

                print("name :"+name)
                print("comp :"+comp)
        
                exist = False
                for item in endDateData:                        # endDateData --> Okunmuş kişilerin listesi                 Bir de burası exist'liği kontrol ediyor
                    if tc == item["Tc"]:
                        exist = True
                        break

                if exist == True:
                        #result = tk.messagebox.askquestion("Uyarı", "Zaten giriş yapmış bulunmaktasınız. Devam etmek için 'yes'e, bitirmek için 'no'ya basınız.")
                        #root1.lift()
                        result=mesaagee.message("Zaten giriş yapmış bulunmaktasınız. \nDevam etmek için yeni bir kart okutun, bitirmek için 'Bitir'e basınız.", rfidNumber)
                        if result == 'yes':
                            EndProcess()
                        else:
                            rfidNumber = 00
                            actualIndex = None
                            pass
                elif exist == False:
                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    if writeDataBool:
                        # enter_currTime = str(datetime.datetime.now().time())
                        enter_currDate = str(datetime.datetime.now().date())
                        print("İsim : " + name + " -- Giriş Saati : " + enter_currTime)
                        actualEnterTime = str(datetime.datetime.now().time())[0:5]
                        expDateData = {"Çıkış saati":"", "Gerçek çıkış saati":"", "Giriş saati": enter_currTime, "Gerçek giriş saati": actualEnterTime,  "İsim": name, "Soyisim": surname, "Tc": tc, "Meslek": job, "Şantiye": comp, "Formen":enterF}
                        endDateData.append(expDateData)
                        endDataSheet.append(expDateData)
                        print(str(endDateData))
                        # update the list of names
                        names.append(name)
                        #result = tk.messagebox.askquestion("Bilgi", "İsim: "+name+" "+surname+"- Giriş saat: "+enter_currTime+"- Gerçek Giriş Saati: "+actualEnterTime+" - Devam edilsin mi?")
                        #root1.lift()
                        #prompt = {}
                        #prompt['answer'] = mbox("İsim: "+name+" "+surname+"- Giriş saat: "+enter_currTime+"- Gerçek Giriş Saati: "+actualEnterTime+" - Çıkış yapılsın mı?", ('Bitir', 'yes'),('ddd', 'no'), root)
                        #result = prompt['answer']
                        #rfidNumber = "None"
                        result=mesaagee.message("İsim: "+name+" "+surname+"- Giriş saat: "+enter_currTime+"-\n Gerçek Giriş Saati: "+actualEnterTime+" - Çıkış yapılsın mı?", rfidNumber)
                        print(result)
                        if result == 'yes':
                            EndProcess()
                        else:
                            rfidNumber = result
                            actualIndex = None
                            rfidNumber = 00
                            pass
                        #writeDataBool = False
                        print("new rfid: "+str(rfidNumber))
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
            try:
                with open(enter_currDate+".json", "w") as d:
                    json.dump(endDateData, d, ensure_ascii = False)
                break
            except:
                print("Hiçbir yüz taranmadı, kamera kapatılıyor...")
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
