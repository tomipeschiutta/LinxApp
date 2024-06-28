import tkinter
import pyodbc
import datetime
import argparse
import requests
from  urllib import request
import tkinter as tk
from  tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename,askopenfilenames
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
#from PIL import ImageTk, Image
import threading
import os
import configparser
import re



URL = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'

json = requests.get(URL).json()

ventana = tk.Tk()
nombre = tk.StringVar()
compra = tk.IntVar()
venta = tk.IntVar()

ventana.title("Cotizacion Moneda Hoy")
frame = Frame(ventana)
frame.pack(fill=BOTH, expand=1)
canvas = Canvas(frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)
scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))

ventana = Frame(canvas)
canvas.create_window((0,0), window=ventana, anchor="nw")

for index, emoji in enumerate((json)):
    compra = json[index]['casa']['compra'][:-1]
    venta = json[index]['casa']['venta'][:-1]
    nombre = json[index]['casa']['nombre']
    nmb = tk.Label(ventana, text=nombre, font=("Verdana",14)).pack()
    lblCompra = tk.Label(ventana, text="Compra", font=("Verdana",12)).pack()
    lblVenta = tk.Label(ventana, text="Venta", font=("Verdana",12)).pack()
    cmp = tk.Button(ventana, text=compra, fg="red",font=("Arial",14)).pack()
    vnt = tk.Button(ventana, text=venta, fg="green",font=("Arial",14)).pack()

ventana.mainloop()
