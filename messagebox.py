from mbox import MessageBox
from tkinter import *

root = Tk()


def mbox(msg, b1, b2, parent, cbo=False, cboList=[]):
    msgbox = MessageBox(msg, b1, b2, parent, cbo, cboList)
    msgbox.root.mainloop()
    msgbox.root.destroy()
    return msgbox.returning


prompt = {}

# it will only show 2 buttons & 1 label if (cbo and cboList) aren't provided
# click on 'x' will return ;`x`;
prompt['answer'] = mbox('Do you want to go?', ('Go', 'go'), ('Cancel', 'cancel'), root)
ans = prompt['answer']
print(ans)
if ans == 'go':
    # do stuff
    pass
else:
    # do stuff
    pass


allowedItems = ['phone','laptop','battery']
prompt['answer'] = mbox('Select product to take', ('Take', 'take'), ('Cancel', 'cancel'), root, cbo=True, cboList=allowedItems)
ans = prompt['answer']
print(ans)
if (ans == 'phone'):
    # do stuff
    pass
elif (ans == 'laptop'):
    # do stuff
    pass
else:
    # do stuff
    pass