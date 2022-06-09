from tkinter import *
import tkinter.messagebox
import gui as gui
import json
import formenYetki as perScreen
import pi_face_recognition_main as faceRecEnt
import pi_face_recognition_exit_main as faceRecOut
import pi_face_recognition_ekmesai as ekmesaiEnter
import pi_face_recognition_exit_ekmesai as ekmesaiExit
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import msgbox

root1=Tk()
root1.withdraw()

formenBool = False

def Switchness():
	
	def GivePermission():
		perScreen.PerController()
	
	def FormenSwitch():
		global formenBool
		reader = SimpleMFRC522()
		try:
			id, tc = reader.read_with_delay()
		finally:
			GPIO.cleanup()
		
		formenTc = 00
		if tc != None and tc != '':
			formenTc = int(tc)
		exist = False
		
		with open("formenList.json", "r") as read_file:
			formenList = json.load(read_file)
		
		for formen in formenList:
			if int(formen) == formenTc:
				exist = True
				break
		
		if exist == False:
			msgbox.messagebox("Uyarı, Bu kullanıca formen yetkisi yok veya kart düzgün okunamadı.")
		elif exist == True:
			if formenBool == False:
				faceRecEnt.FormenTrue()
				faceRecOut.FormenTrue()
				ekmesaiEnter.FormenTrue()
				ekmesaiExit.FormenTrue()
				gui.FormenTrue()
				formenBool = True
				msgbox.messagebox("Uyarı, Formen Onayı: AÇIK")
				pencere.update_idletasks()
				pencere.destroy()
			elif formenBool == True:
				faceRecEnt.FormenFalse()
				faceRecOut.FormenFalse()
				ekmesaiEnter.FormenFalse()
				ekmesaiExit.FormenFalse()
				gui.FormenFalse()
				formenBool = False
				msgbox.messagebox("Uyarı, Formen Onayı: KAPALI")
				pencere.update_idletasks()
				pencere.destroy()
	
	def SwitchTrue():
		global formenBool
		global formenTxtVar
		formenPass = txtPass.get()
		print(formenPass)
		if formenBool == False:
			if formenPass == "":
				print("Formen şifresini giriniz...")
				msgbox.messagebox("Uyarı, Formen şifresini giriniz.")
				return;
			elif formenPass == "1937":
				faceRecEnt.FormenTrue()
				faceRecOut.FormenTrue()
				ekmesaiEnter.FormenTrue()
				ekmesaiExit.FormenTrue()
				gui.FormenTrue()
				formenBool = True
				msgbox.messagebox("Uyarı, Formen Onayı: AÇIK")
				pencere.update_idletasks()
				txtPass.delete(0, END)
				pencere.destroy()
			else:
				print("Şifre yanlış!")
				msgbox.messagebox("Uyarı, Şifre yanlış.")
		elif formenBool == True:
			msgbox.messagebox("Uyarı, Formen onayı zaten açık.")
			pencere.update()
			return
			
	def SwitchFalse():
		global formenBool
		global formenTxtVar
		formenPass = txtPass.get()
		print(formenPass)
		if formenBool == True:
			if formenPass == "":
				print("Formen şifresini giriniz...")
				msgbox.messagebox("Uyarı, Formen şifresini giriniz.")
				return;
			elif formenPass == "1937":
				faceRecEnt.FormenFalse()
				faceRecOut.FormenFalse()
				ekmesaiEnter.FormenFalse()
				ekmesaiExit.FormenFalse()
				gui.FormenFalse()
				formenBool = False
				msgbox.messagebox("Uyarı, Formen Onayı: KAPALI")
				pencere.update_idletasks()
				txtPass.delete(0, END)
				pencere.destroy()
			else:
				print("Şifre yanlış!")
				msgbox.messagebox("Uyarı, Şifre yanlış.")
		elif formenBool == False:
			msgbox.messagebox("Uyarı, Formen onayı zaten kapalı.")
			pencere.update()
			return
	
	pencere = Tk()
	pencere.geometry('590x180')
    
	lblInfo = Label(pencere, text = "Formen Onayı Aç-Kapa'ya bastıktan sonra formen kartını okutunuz.")
	lblInfo.grid(row=0,column=0)
    
	frame = Frame(pencere, width=20, height=14, padx=7, pady=7)
	frame.grid(row=2,column=0)
    
	btnClose = Button(frame, text = 'Çıkış', command=pencere.destroy, height=6,width=20)
	btnClose.grid(row=0,column=0)
    
	btnOpenClose = Button(frame, text = 'Formen Onayı Aç-Kapa', command=FormenSwitch,height=6,width=20)
	btnOpenClose.grid(row=0,column=1)

	btnConfirm = Button(frame, text = 'Formen Yetkisi Ver-Al', command=GivePermission,height=6,width=20)
	btnConfirm.grid(row=0,column=2)
	pencere.mainloop()
