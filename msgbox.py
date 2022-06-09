from tkinter import *
from PIL import ImageTk
from PIL import Image



def messagebox(msg):
	def Close():
		pencere.destroy()
		
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

	load = Image.open("tik2.gif")
	render = ImageTk.PhotoImage(load)

	logoNewFrame = Frame(pencere, width=45, height=14)
	logoNewFrame.pack()

	lblLogo = Label(logoNewFrame, image = render)
	lblLogo.pack()

	lblInf = Label(pencere)
	lblInf.config(font=("", 14), text = mesaj.get())
	lblInf.pack()

	btnMainEnt = Button(pencere, text = 'Tamam', height = 6, width = 20, command = Close)
	btnMainEnt.pack()

	

	pencere.mainloop()
