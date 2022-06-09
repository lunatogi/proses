import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import tkinter.messagebox
from tkinter import *
import json
import msgbox

root1=Tk()
root1.withdraw()


def PerController():
	
	def GivePer():
		formenPass = txtPass.get()
		exist = False
		print(formenPass)
		try:
			with open("formenList.json", "r") as read_file:
				formenList = json.load(read_file)
		except:
			formenList = []
		reader = SimpleMFRC522()
		try:
			id, tc = reader.read_with_delay()
		finally:
			GPIO.cleanup()
			
		for formen in formenList:
			if int(tc) == int(formen):
				exist = True	
			
			
			
		if exist == False:
			if formenPass == "":
				print("Şifresini giriniz...")
				msgbox.messagebox("Uyarı, Şifreyi giriniz.")
				return;
			elif formenPass == "1937":
				formenList.append(tc)
				with open("formenList.json", "w") as a:
					json.dump(formenList,a)
				msgbox.messagebox("Bilgi, Kişiye formen yetkisi verildi.")
				pencere.update_idletasks()
				txtPass.delete(0, END)
				pencere.destroy()
			else:
				print("Şifre yanlış!")			
				msgbox.messagebox("Uyarı, Şifre yanlış.")
		elif exist == True:
			msgbox.messagebox("Uyarı, Bu kişinin zaten formen yetkisi var.")
			pencere.update()
			return
			
	def TakePer():
		formenPass = txtPass.get()
		exist = False
		print(formenPass)
		try:
			with open("formenList.json", "r") as read_file:
				formenList = json.load(read_file)
		except:
			formenList = []
		reader = SimpleMFRC522()
		try:
			id, tc = reader.read_with_delay()
		finally:
			GPIO.cleanup()
			
		for formen in formenList:
			if int(tc) == int(formen):
				exist = True	
			
			
			
		if exist == True:
			if formenPass == "":
				print("Şifresini giriniz...")
				msgbox.messagebox("Uyarı, Şifreyi giriniz.")
				return;
			elif formenPass == "1937":
				formenList.remove(tc)
				with open("formenList.json", "w") as a:
					json.dump(formenList,a)
				msgbox.messagebox("Bilgi, Kişinin formen yetkisi alındı.")
				pencere.update_idletasks()
				txtPass.delete(0, END)
				pencere.destroy()
			else:
				print("Şifre yanlış!")
				msgbox.messagebox("Uyarı, Şifre yanlış.")
		elif exist == False:
			msgbox.messagebox("Uyarı, Bu kişinin zaten formen yetkisi yok.")
			pencere.update()
			return
	
	
	
	
	
	pencere = Tk()
	pencere.geometry('630x180')
    
	lblInfo = Label(pencere, text = "Şifreyi girip gerekli tuşa bastıktan sonra yetki vermek veya almak istediğiniz kişinin kartını okutunuz.")
	lblInfo.grid(row=0,column=0)
	txtPass = Entry(pencere,width=15,font=("" , 18), show="*")
	txtPass.grid(row=1,column=0)
    
	frame = Frame(pencere, width=20, height=14, padx=7, pady=7)
	frame.grid(row=2,column=0)
    
	btnClose = Button(frame, text = 'Çıkış', command=pencere.destroy, height=6,width=20)
	btnClose.grid(row=0,column=0)
    
	btnGive = Button(frame, text = 'Formen Yetkisi Ver', command=GivePer,height=6,width=20)
	btnGive.grid(row=0,column=2)    

	btnGive = Button(frame, text = 'Formen Yetkisini Al', command=TakePer,height=6,width=20)
	btnGive.grid(row=0,column=3)

	pencere.mainloop()
