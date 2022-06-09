#!/usr/bin/env python3

#python3 gui.py --dataset dataset --encodings encodings.json --detection-method hog --cascade haarcascade_frontalface_default.xml
import msgbox
from tkinter import *
import tkinter.messagebox
import encode_faces_main as encode
from PIL import ImageTk
from PIL import Image
import os
import pi_face_recognition_main as faceRecEnt
import pi_face_recognition_exit_main as faceRecOut
import pi_face_recognition_ekmesai as ekmesaiEnter
import pi_face_recognition_exit_ekmesai as ekmesaiExit
import person_add as personAdd
import person_quit as personQuit
import ekmesai_saat as eksaat
import formen_screen as frmScr
#import spreadsheet as sheet

root1=Tk()
root1.withdraw()

pencere = Toplevel()
pencere.geometry('{0}x{1}+0+0'.format(pencere.winfo_screenwidth(), pencere.winfo_screenheight()))
txtNameVar = ""
formenTxtVar = StringVar()
formenTxtVar.set("Formen Onayı: KAPALI")
bilgiTxtVar = StringVar()
bilgiTxtVar.set("İkinci fotoğraf çekimi için hazırlanın.")

#print("lol : "+formenTxtVar)

formenPass = ""
formenBool = False


print("get : "+formenTxtVar.get())

def FormenSwitch():
    frmScr.Switchness()
        
def FormenTrue():
    global formenBool
    print("formen true")
    formenBool = True
    
def FormenFalse():
    global formenBool
    print("formen false")
    formenBool = False

def ChangeInfo(info):
    global bilgiTxtVar
    bilgiTxtVar.set(info)

def CallEncode():
    personAdd.StartUserEnter()
    
def CallQuit():
    personQuit.DeleteUser()

def CallFaceRecEnter():
    faceRecEnt.FaceRecEnter()

def CallFaceRecOut():
    faceRecOut.FaceRecOut()
    
def EkMesaiSaat():
    eksaat.SaatBelirle()

def CallMesaiEnter():
    global formenBool
    print(formenBool)
    if formenBool == False:
        msgbox.messagebox("Uyarı, Ek mesai girişi için formen onayı gerekmektedir.")
    else:
        ekmesaiEnter.FaceRecEnter()

def CallMesaiExit():
    global formenBool
    if formenBool == False:
        msgbox.messagebox("Uyarı, Ek mesai girişi için formen onayı gerekmektedir.")
    else:
        ekmesaiExit.FaceRecOut()


        

#txtName = Entry(pencere,textvariable = txtNameVar)
#txtName.grid(row=0,column=0)

load = Image.open("logo.gif")
render = ImageTk.PhotoImage(load)

logoNewFrame = Frame(pencere, width=45, height=14)
logoNewFrame.grid(row=1, column=0)

lblLogo = Label(logoNewFrame, text = "   "    , font=("", 30))
lblLogo.grid(row=1,column=0)

lblLogo = Label(logoNewFrame, image = render)
lblLogo.grid(row=2,column=0)

frame = Frame(pencere, width=45, height=14, padx=7, pady=7)
frame.grid(row=1, column=2)

btnEkSaat = Button(frame, text = 'Ek Mesai Saatini Belirle', height = 6, width = 20, command = EkMesaiSaat)
btnEkSaat.grid(row=2,column=0)

infFrame = Frame(logoNewFrame, borderwidth=5, relief="sunken", width=45,height=5)
infFrame.grid(row=0, column=0)

lblInf = Label(infFrame, text = "PROSES İKLİMLENDİRME"    , font=("", 14))
lblInf.grid(row=0,column=0)

#lblFormen = Label(pencere, textvariable = formenTxtVar, font=("", 14))
#lblFormen.grid(row=2,column=1)

btnMainEnt = Button(frame, text = 'Giriş al', height = 6, width = 20, command = CallFaceRecEnter)
btnMainEnt.grid(row=0,column=0)

btnMainOut = Button(frame, text = 'Çıkış al', height = 6, width = 20, command = CallFaceRecOut)
btnMainOut.grid(row=0,column=1)

btnMesaiEnt = Button(frame, text = 'Ek Mesai Giriş al', height = 6, width = 20, command = CallMesaiEnter)
btnMesaiEnt.grid(row=1,column=0)

btnMesaiOut = Button(frame, text = 'Ek Mesai Çıkış al', height = 6, width = 20, command = CallMesaiExit)
btnMesaiOut.grid(row=1,column=1)

btnFormen = Button(frame, text = 'Formen Onayı', height = 6, width = 20, command = FormenSwitch)
btnFormen.grid(row=2,column=1)

#txtFormen = Entry(frame,textvariable = formenPass, show="*")
#txtFormen.grid(row=2,column=0)

btnAdd = Button(frame, text = 'Kişi ekle', height = 6, width = 20, command = CallEncode)
btnAdd.grid(row=3,column=0)

btnQuit = Button(frame, text = 'Kişi çıkar', height = 6, width = 20, command = CallQuit)
btnQuit.grid(row=3,column=1)

logoFrame = Frame(pencere, borderwidth=5, width=45,height=5)
logoFrame.grid(row=3, column=0)

lblLogo = Label(logoFrame, text = "                                                             "    , font=("", 15))
lblLogo.grid(row=0,column=0)


#btnClose = Button(pencere, text = 'Kapat', command=pencere.destroy,height=6,width=20)
#btnClose.grid(row=4,column=1)

pencere.mainloop()
