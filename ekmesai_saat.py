from tkinter import *
from tkinter.ttk import Combobox
from tkinter.font import Font
import json

def SaatBelirle():
	
	def SetHour():
		print("gieeeeiiiirrdi")
		saatler = {"Giriş": comEnter.get(), "Çıkış": comOut.get()}
		with open("ekmesaiSaat.json","w") as d:
			json.dump(saatler, d, ensure_ascii = False)
		pencere.destroy()
	
	
	pencere = Tk()
	pencere.geometry('400x410')
	
	enter = ["17:00","17:30","18:00","18:30","19:00","19:30"]
	comEnter = Combobox(pencere,width=14,font=("" , 18),values=enter,state="readonly",height=200)
	comEnter.grid(row=0,column=1)
	lblEnter = Label(pencere, text = "Başlangıç Saati: ")
	lblEnter.grid(row=0,column=0)
	
	out = ["19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00"]
	comOut = Combobox(pencere,width=14,font=("" , 18),values=out,state="readonly",height=200)
	comOut.grid(row=1,column=1)
	lblOut = Label(pencere, text = "Çıkış Saati: ")
	lblOut.grid(row=1,column=0)
	
	btnConfirm = Button(pencere, text = 'Kaydet ve Çık', command=SetHour,height=6,width=20)
	btnConfirm.grid(row=2,column=1)
	
	btnQuit = Button(pencere, text = 'Çıkış', command=pencere.destroy,height=6,width=20)
	btnQuit.grid(row=2,column=0)
	
	bigfont = Font(size=200)
	pencere.option_add("*TCombobox*Listbox*Font", bigfont)
	
	pencere.mainloop()
