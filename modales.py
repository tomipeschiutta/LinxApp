from tkinter import *

class main(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=None)
        self.master.title("Probando Dialogos - Manejando datos")
        self.master.geometry("300x50")
        Button(root, text="cambiar valor", command=self.dialogo).pack()
        self.valor = StringVar()
        self.valor.set("Hola Manejando datos")
        Label(self.master, textvariable=self.valor).pack()

    def dialogo(self):
        d = MyDialog(root, self.valor, "Probando Dialogo", "Dame valor")
        root.wait_window(d.top)
        #self.valor.set(d.ejemplo)

class MyDialog:
    def __init__(self, parent, valor, title, labeltext = '' ):
        self.valor = valor

        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        if len(title) > 0: self.top.title(title)
        if len(labeltext) == 0: labeltext = 'Valor'
        Label(self.top, text=labeltext).pack()
        self.top.bind("<Return>", self.ok)
        self.e = Entry(self.top, text=valor.get())
        self.e.bind("<Return>", self.ok)
        self.e.bind("<Escape>", self.cancel)
        self.e.pack(padx=15)
        self.e.focus_set()
        b = Button(self.top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self, event=None):
        print("Has escrito ...", self.e.get())
        self.valor.set(self.e.get())
        self.top.destroy()

    def cancel(self, event=None):
        self.top.destroy()

root = Tk()
a = main(root)
root.mainloop()
