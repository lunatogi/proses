import tkinter
import tkinter.ttk as ttk

class MessageBox(object):

    def __init__(self, msg, b1, b2, parent, cbo, cboList):

        root = self.root = tkinter.Toplevel(parent)

        root.title('Choose')
        root.geometry('100x100')
        root.resizable(False, False)
        root.grab_set() # modal

        self.msg = str(msg)
        self.b1_return = True
        self.b2_return = False
        # if b1 or b2 is a tuple unpack into the button text & return value
        if isinstance(b1, tuple): b1, self.b1_return = b1
        if isinstance(b2, tuple): b2, self.b2_return = b2
        # main frame
        frm_1 = tkinter.Frame(root)
        frm_1.pack(ipadx=2, ipady=2)
        # the message
        message = tkinter.Label(frm_1, text=self.msg)
        if cbo: message.pack(padx=8, pady=8)
        else: message.pack(padx=8, pady=20)
        # if entry=True create and set focus
        if cbo:
            self.cbo = ttk.Combobox(frm_1, state="readonly", justify="center", values= cboList)
            self.cbo.pack()
            self.cbo.focus_set()
            self.cbo.current(0)
        # button frame
        frm_2 = tkinter.Frame(frm_1)
        frm_2.pack(padx=4, pady=4)
        # buttons
        btn_1 = tkinter.Button(frm_2, width=8, text=b1)
        btn_1['command'] = self.b1_action
        if cbo: btn_1.pack(side='left', padx=5)
        else: btn_1.pack(side='left', padx=10)
        if not cbo: btn_1.focus_set()
        btn_2 = tkinter.Button(frm_2, width=8, text=b2)
        btn_2['command'] = self.b2_action
        if cbo: btn_2.pack(side='left', padx=5)
        else: btn_2.pack(side='left', padx=10)
        # the enter button will trigger the focused button's action
        btn_1.bind('<KeyPress-Return>', func=self.b1_action)
        btn_2.bind('<KeyPress-Return>', func=self.b2_action)
        # roughly center the box on screen
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        root.update_idletasks()
        root.geometry("210x110+%d+%d" % (parent.winfo_rootx()+7,
                                         parent.winfo_rooty()+70))

        root.protocol("WM_DELETE_WINDOW", self.close_mod)

        # a trick to activate the window (on windows 7)
        root.deiconify()

    def b1_action(self, event=None):
        try: x = self.cbo.get()
        except AttributeError:
            self.returning = self.b1_return
            self.root.quit()
        else:
            if x:
                self.returning = x
                self.root.quit()

    def b2_action(self, event=None):
        self.returning = self.b2_return
        self.root.quit()

    def close_mod(self):
        # top right corner cross click: return value ;`x`;
        # we need to send it a value, otherwise there will be an exception when closing parent window
        self.returning = ";`x`;"
        self.root.quit()