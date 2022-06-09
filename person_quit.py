from tkinter import *
import numpy as np
import tkinter.messagebox
import json
import msgbox

root1=Tk()
root1.withdraw()

def EraseDatabase(tc):
    with open("database.json", "r") as read_file:
        dataJson = json.load(read_file)

    knownEncodings = dataJson["encodings"]
    knownNames = dataJson["names"]
    knownSurnames = dataJson["surname"]
    knownTcs = dataJson["tc"]
    knownJobs = dataJson["job"]
    knownComps = dataJson["comp"]
    
    counter = 1
    while counter <= 4:                 #Fotoğraf sayısı kadar
        print(knownTcs)
        try:
            index = knownTcs.index(tc)
        except:
            msgbox.messagebox("Uyarı, Bu Tc numaralı biri bulunamadı.")
            return
        print(index)
        del(knownEncodings[index])
        del(knownNames[index])
        del(knownSurnames[index])
        del(knownTcs[index])
        del(knownJobs[index])
        del(knownComps[index])
        counter += 1

    knownEncodings1 = np.array(knownEncodings).tolist()
    knownNames1 = np.array(knownNames).tolist()
    knownSurnames1 = np.array(knownSurnames).tolist()
    knownTcs1 = np.array(knownTcs).tolist()
    knownJobs1 = np.array(knownJobs).tolist()
    knownComps1 = np.array(knownComps).tolist()
    
    data = {"encodings": knownEncodings1, "names": knownNames1, "surname": knownSurnames1, "tc": knownTcs1, "job": knownJobs1, "comp": knownComps1}
    
    with open("database.json", "w") as a:
        json.dump(data,a)
        
    msgbox.messagebox("Bilgi, Kişi başarıyla silindi.")
    
def DeleteUser():
    
    def Delete():
        print("deleted")
        varTc = txtTc.get()
        EraseDatabase(varTc)
        txtTc.delete(0, END)
    
    pencere = Tk()
    pencere.geometry('400x410')
    
    lblInfo = Label(pencere, text = "Silinecek kişinin TC numarasını giriniz")
    lblInfo.grid(row=0,column=0)
    txtTc = Entry(pencere,width=15,font=("" , 18))
    txtTc.grid(row=1,column=0)
    
    frame = Frame(pencere, width=20, height=14, padx=7, pady=7)
    frame.grid(row=2,column=0)
    
    btnClose = Button(frame, text = 'Çıkış', command=pencere.destroy, height=6,width=20)
    btnClose.grid(row=0,column=0)
	
    btnConfirm = Button(frame, text = 'Çalışanı Sil', command=Delete,height=6,width=20)
    btnConfirm.grid(row=0,column=1)

    pencere.mainloop()
