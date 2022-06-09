from tkinter import *
import tkinter.messagebox
from imutils import paths
from tkinter.ttk import Combobox
from tkinter.font import Font
import face_recognition
import gui as gui
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
#import mxnet as mx
import argparse
import pickle
import numpy as np
import json
import cv2
import os
import shutil
import time
from mbox import MessageBox
import mesaagee
import msgbox

root1=Tk()
root1.withdraw()
root=Tk()
root.withdraw()

def mbox(msg, b1, b2, parent, cbo=False, cboList=[]):
    msgbox = MessageBox(msg, b1, b2, parent, cbo, cboList)
    msgbox.root.mainloop()
    msgbox.root.destroy()
    return msgbox.returning

def EncodeProccess(name, surname, tc, job, comp):

        
    #messagebox.showinfo("Uyarı", "Kartı okutunuz.")
    #root1.lift()
    result=mesaagee.message("Kartınızı Okutunuz...", 00)
    if result == 'yes':
        return
    else:
        pass
    reader = SimpleMFRC522()
    cardRead = False
    while cardRead == False:
        #try:
        try:
            reader.write(tc)
            print("Yazıldı")
        except:
            return
        cardRead = True
        workerName = name
        print(workerName)
        print("Eğer isim kısmına sadece 'q' yazarsanız işlem bitirilir")
        print("İsminizi girdikten sonra ilk fotoğrafı çekmeye hazırlanın...")
        #workerName = input("İsminizi girin : ")
        #if workerName == "q":
            #break
        os.makedirs('./dataset/'+workerName)
        os.system('raspistill -w 320 -h 240 -o ./dataset/'+workerName+'/0000.jpg')
        time.sleep(2)
        os.system('raspistill -w 320 -h 240 -o ./dataset/'+workerName+'/0001.jpg')
        time.sleep(2)
        os.system('raspistill -w 320 -h 240 -o ./dataset/'+workerName+'/0002.jpg')
        time.sleep(2)
        os.system('raspistill -w 320 -h 240 -o ./dataset/'+workerName+'/0003.jpg')

        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-c", "--cascade", required=False,
            help = "path to where the face cascade resides")
        ap.add_argument("-i", "--dataset", required=False,
            help="path to input directory of faces + images")
        ap.add_argument("-e", "--encodings", required=False,
            help="path to serialized db of facial encodings")
        ap.add_argument("-d", "--detection-method", type=str, default="hog",
            help="face detection model to use: either `hog` or `cnn`")
        args = vars(ap.parse_args())

        # grab the paths to the input images in our dataset
        print("[INFO] quantifying faces...")
        imagePaths = list(paths.list_images("dataset"))
        
        try:
            with open("database.json", "r") as read_file:
                dataJson = json.load(read_file)
            knownEncodings = dataJson["encodings"]
            knownNames = dataJson["names"]
            knownSurnames = dataJson["surname"]
            knownTcs = dataJson["tc"]
            knownJobs = dataJson["job"]
            knownComps = dataJson["comp"]
        except:
            knownEncodings = []
            knownNames = []
            knownSurnames = []
            knownTcs = []
            knownJobs = []
            knownComps = []
        
        print(str(knownTcs))

        # initialize the list of known encodings and known names


        # loop over the image paths
        counter = 0
        for (i, imagePath) in enumerate(imagePaths):
            
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1,
                len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb,
                model='hog')

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            
            # loop over the encodings
            for encoding in encodings:
                counter += 1
                # add each encoding + name to our set of known names and
                # encodings
                knownEncodings.append(encoding)
                knownNames.append(name)
                knownSurnames.append(surname)
                knownTcs.append(tc)
                knownJobs.append(job)
                knownComps.append(comp)
            
        print("counter : "+str(counter))
        if counter < 4:
            d = './dataset'
            shutil.rmtree(d)
            msgbox.messagebox("Uyarı, Fotoğrafların hepsinde yüzünüz algılanamadığı için kaydınız alınamamıştır. Lütfen yeniden deneyiniz.")
            return False
        
        result=mesaagee.message("Kartınızı Kontrol İçin Okutunuz...", 00)
        if result == 'yes':
            return
        else:
            pass
        
        try:
            id, data = reader.read_with_delay()
        finally:
            GPIO.cleanup()
            
        if int(data) != int(tc):
            d = './dataset'
            shutil.rmtree(d)
            msgbox.messagebox("Uyarı, Kartınıza düzgün yazılamadığın lütfen tekrar deneyin.")
            return False
            
            
        knownEncodings1 = np.array(knownEncodings).tolist()
        knownNames1 = np.array(knownNames).tolist()
        knownSurnames1 = np.array(knownSurnames).tolist()
        knownTcs1 = np.array(knownTcs).tolist()
        knownJobs1 = np.array(knownJobs).tolist()
        knownComps1 = np.array(knownComps).tolist()
        
        data = {"encodings": knownEncodings1, "names": knownNames1, "surname": knownSurnames1, "tc": knownTcs1, "job": knownJobs1, "comp": knownComps1}

        with open("database.json", "w") as a:
            json.dump(data,a)
            
        d = './dataset'
        shutil.rmtree(d)
        msgbox.messagebox("Bilgi, Kaydınız alınmıştır.")
        return True
        #except:
         #   messagebox.showinfo("Uyarı", "Kartı okutunuz.")
          #  root1.lift()
        #finally:
         #   GPIO.cleanup()
    
    #except:
    #print("not exist")
        #with open("database.json", "w") as a:
            #json.dump(data,a)
    
    #messagebox.showinfo("Bilgi", "Kaydınız alınmıştır.")
    #root1.lift()

        



def StartUserEnter():
    
    def CallEncode():
        txtNameVar = txtName.get()
        txtSurnameVar = txtSurname.get()
        txtTcVar = txtTc.get()
        txtJobVar = comJob.get()
        txtCompVar = txtComp.get()
        
        if all(c.isdigit() for c in txtTcVar) == False:
            msgbox.messagebox("Uyarı, TC numarasında sayı dışında bir karakter bulunamaz.")
            return
            
        if any(c.isdigit() for c in txtNameVar) == True:
            msgbox.messagebox("Uyarı, İsim hanesinde sayı dışında bir karakter bulunamaz.")
            return
            
        if any(c.isdigit() for c in txtSurnameVar) == True:
            msgbox.messagebox("Uyarı, Soyisimde sayı bulunamaz.")
            return
        
        if len(txtTcVar) != 11:
            msgbox.messagebox("Uyarı, TC numarası 11 haneli olmalıdır.")
            return
        
        if len(txtJobVar) < 1:
            msgbox.messagebox("Uyarı, Lütfen kişinin mesleğini seçiniz.")
            return
        txtName.delete(0, END)
        txtSurname.delete(0, END)
        txtTc.delete(0, END)
        comJob.delete(0, END)
        txtComp.delete(0, END)
        EncodeProccess(txtNameVar, txtSurnameVar, txtTcVar, txtJobVar, txtCompVar)
            
    
    
    pencere = Tk()
    pencere.geometry('400x410')
    
    txtNameVar = ""
    txtSurnameVar = ""
    txtTcVar = ""
    txtJobVar = ""
    txtCompVar = ""

    txtName = Entry(pencere,width=15,font=("" , 18))
    txtName.grid(row=0,column=1)
    lblName = Label(pencere, text = "İsim : ")
    lblName.grid(row=0,column=0)
    
    txtSurname = Entry(pencere,width=15,font=("" , 18))
    txtSurname.grid(row=1,column=1)
    lblSurname = Label(pencere, text = "Soyisim : ")
    lblSurname.grid(row=1,column=0)
    
    txtTc = Entry(pencere,width=15,font=("" , 18))
    txtTc.grid(row=2,column=1)
    lblTc = Label(pencere, text = "Tc Numarası : ")
    lblTc.grid(row=2,column=0)
    
    bigfont = Font(size=200)
    
    cusListbox = Listbox(font=("Courier",100))
    options = ["Tesisatçı","Kanalcı","İzolasyon","Kaynakçı","Formen"]
    comJob = Combobox(pencere,width=14,font=("" , 18),values=options,state="readonly",height=200)
    pencere.option_add("*TCombobox*Listbox*Font", bigfont)
    comJob.grid(row=3,column=1)
    lblJob = Label(pencere, text = "Meslek : ")
    lblJob.grid(row=3,column=0)
    
    txtComp = Entry(pencere,width=15,font=("" , 18))
    txtComp.grid(row=4,column=1)
    lblComp = Label(pencere, text = "Şantiye : ")
    lblComp.grid(row=4,column=0)
    
    btnClose = Button(pencere, text = 'Çıkış', command=pencere.destroy,height=6,width=20)
    btnClose.grid(row=6,column=0)
    
    btnConfirm = Button(pencere, text = 'Kaydet ve Fotoğrafa Geç', command=CallEncode,height=6,width=20)
    btnConfirm.grid(row=6,column=1)
    
    pencere.mainloop()
