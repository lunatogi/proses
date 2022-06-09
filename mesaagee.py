from tkinter import *
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from PIL import ImageTk
from PIL import Image


data = ""






def message(msg, currNumber):
	a=""
	def Close():
		global a
		print("Bitir")
		a="yes"
		print(a)
	
	global run
	global data
	print(msg)
	mesaj = StringVar()
	mesaj.set(str(msg))
	pencere = Toplevel()
	print("mesaj: "+str(mesaj))
	window_height = 300
	window_width = 700

	pencere.resizable(False, False)  # This code helps to disable windows from resizing


	screen_width = pencere.winfo_screenwidth()
	screen_height = pencere.winfo_screenheight()

	x_cordinate = int((screen_width/2) - (window_width/2))
	y_cordinate = int((screen_height/2) - (window_height/2))

	pencere.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
	
	load = Image.open("tik.gif")
	render = ImageTk.PhotoImage(load)

	logoNewFrame = Frame(pencere, width=45, height=14)
	logoNewFrame.pack()

	lblLogo = Label(logoNewFrame, image = render)
	lblLogo.pack()

	lblInf = Label(pencere)
	lblInf.config(font=("", 14), text = mesaj.get())
	lblInf.pack()

	btnMainEnt = Button(pencere, text = 'Bitir', height = 6, width = 20, command = Close)
	btnMainEnt.pack()

	

	
	
	run = True

	

	pencere.update()
	while run:
		global a
		pencere.update()
		print(a)
		if a == "yes":
			pencere.destroy()
			run = False
			return a
		GPIO.setwarnings(False)     
		reader = SimpleMFRC522()
		try:
			id, data = reader.read()
			print(data)
			print("kart data: "+str(data))
			if str(data) != "None" and data != '':

				print("currNum: "+str(currNumber))
				if int(currNumber) != int(data):
					pencere.destroy()
					run = False
					return data
					#pencere.destroy()
					#run = False
					#return data
		finally:
			GPIO.cleanup()
			
		
