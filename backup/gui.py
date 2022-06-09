#python3 gui.py --dataset dataset --encodings encodings.json --detection-method hog --cascade haarcascade_frontalface_default.xml

from tkinter import *
import encode_faces_main as encode
import pi_face_recognition_main as faceRecEnt
import pi_face_recognition_exit_main as faceRecOut

txtNameVar = ""

def CallEncode():
    txtNameVar = txtName.get()
    encode.EncodeProccess(txtNameVar)
    txtName.delete(0, END)

def CallFaceRecEnter():
    faceRecEnt.FaceRecEnter()
    
def CallFaceRecOut():
    faceRecOut.FaceRecOut()

pencere = Tk()
pencere.geometry('380x300')

btnClose = Button(pencere,text = 'Kapat', command=pencere.destroy,height=6,width=20)
btnClose.grid(row=2,column=1)

btnAdd = Button(pencere,text = 'Kişi ekle',height=6,width=20, command = CallEncode)
btnAdd.grid(row=0,column=1)

btnMainEnt = Button(pencere,text = 'Giriş al',height=6,width=20, command = CallFaceRecEnter)
btnMainEnt.grid(row=1,column=0)

btnMainOut = Button(pencere,text = 'Çıkış al',height=6,width=20, command = CallFaceRecOut)
btnMainOut.grid(row=1,column=1)


txtName = Entry(pencere,textvariable = txtNameVar)
txtName.grid(row=0,column=0)

pencere.mainloop()