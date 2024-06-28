import tkinter

import tkinter as tk
from  tkinter import *
from tkinter.filedialog import askopenfilename,askopenfilenames
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

ventana = Tk()
ventana.moneda=tk.StringVar()
ventana.compra=tk.StringVar()
ventana.venta=tk.StringVar()

ventana.title("Cotizacion Moneda Hoy")
ventana.geometry("600x250")
ventana.resizable(False,False)
ventana.iconbitmap("linx.ico")

ventana.lblTitulo= Label(ventana,font=("Verdana",12),text="Precio Dolar Hoy")
ventana.lblOfficial= Label(ventana,font=("Verdana",10),text="DOLAR OFFICIAL")
ventana.lblOfficialC= Label(ventana,font=("Verdana",10),text="Compra")
ventana.lblOfficialV= Label(ventana,font=("Verdana",10),text="Venta")
ventana.lblBlue= Label(ventana,font=("Verdana",10),text="DOLAR BLUE")
ventana.lblBlueC= Label(ventana,font=("Verdana",10),text="Compra")
ventana.lblBlueV= Label(ventana,font=("Verdana",10),text="Venta")
ventana.lblLiqui= Label(ventana,font=("Verdana",10),text="CONTADO CON LIQUI")
ventana.lblLiquiV= Label(ventana,font=("Verdana",10),text="Venta")
ventana.lblPromedio= Label(ventana,font=("Verdana",10),text="DOLAR PROMEDIO")
ventana.lblBolsa= Label(ventana,font=("Verdana",10),text="DOLAR BOLSA")
ventana.lblTurista= Label(ventana,font=("Verdana",10),text="DOLAR TURISTA")
ventana.btnOfficialC =tk.Button(ventana, text="99.23",fg="red",font=("Arial",14))
ventana.btnOfficialV =tk.Button(ventana, text="105.23",fg="green",font=("Arial",14))
ventana.btnBlueC =tk.Button(ventana, text="194.50",fg="red",font=("Arial",14))
ventana.btnBlueV =tk.Button(ventana, text="197.50",fg="green",font=("Arial",14))
ventana.btnLiquiV =tk.Button(ventana, text="179.72",fg="green",font=("Arial",14))
ventana.btnPromedioC =tk.Button(ventana, text="Compra",fg="red",font=("Arial",14))
ventana.btnPromedioV =tk.Button(ventana, text="Venta",fg="green",font=("Arial",14))
ventana.btnBolsaC =tk.Button(ventana, text="Compra",fg="red",font=("Arial",14))
ventana.btnBolsaV =tk.Button(ventana, text="Venta",fg="green",font=("Arial",14))
ventana.btnTuristaC =tk.Button(ventana, text="Compra",fg="red",font=("Arial",14))
ventana.btnTuristaV =tk.Button(ventana, text="Venta",fg="green",font=("Arial",14))

ventana.lblTitulo.place(y=5,x=250)
ventana.lblOfficial.place(y=50,x=40)
ventana.lblOfficialC.place(y=70,x=20)
ventana.lblOfficialV.place(y=70,x=120)
ventana.lblBlue.place(y=50,x=250)
ventana.lblBlueC.place(y=70,x=220)
ventana.lblBlueV.place(y=70,x=320)
ventana.lblLiqui.place(y=50,x=420)
ventana.lblLiquiV.place(y=70,x=470)
ventana.lblPromedio.place(y=150,x=10)
ventana.lblBolsa.place(y=150,x=210)
ventana.lblTurista.place(y=150,x=410)
ventana.btnOfficialC.place(y=100,x=10,width=80,heigh=50)
ventana.btnOfficialV.place(y=100,x=100,width=80,heigh=50)
ventana.btnBlueC.place(y=100,x=210,width=80,heigh=50)
ventana.btnBlueV.place(y=100,x=300,width=80,heigh=50)
ventana.btnLiquiV.place(y=100,x=450,width=80,heigh=50)




ventana.mainloop()
