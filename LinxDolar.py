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

class LinxDolar(object):
    def __init__(self):
        super().__init__()

        self.cadenaConeccion = ""
        self.idmoneda = 0
        self.nombre = ""
        self.compra = 0
        self.venta = 0
        self.cursor = pyodbc.Cursor
        self.ventana = tk.Tk()
        self.dibujarventana()

        self.iniciar()


    def dibujarventana(self):


        self.nombre = tk.StringVar()
        self.compra = tk.IntVar()
        self.venta = tk.IntVar()

        self.ventana.title("Cotizacion Moneda Hoy")
        self.frame = Frame(self.ventana)
        self.frame.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self.frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion= self.canvas.bbox("all")))

        self.ventana = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.ventana, anchor="nw")


    def iniciar(self):

        URL = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
        json = requests.get(URL).json()
        for index, emoji in enumerate((json)):
            self.compra = json[index]['casa']['compra'][:-1]
            self.venta = json[index]['casa']['venta'][:-1]
            self.nombre = json[index]['casa']['nombre']
            self.nmb = tk.Label(self.ventana, text=self.nombre, font=("Verdana",14)).pack()
            self.lblCompra = tk.Label(self.ventana, text="Compra", font=("Verdana",12)).pack()
            self.lblVenta = tk.Label(self.ventana, text="Venta", font=("Verdana",12)).pack()
            self.cmp = tk.Button(self.ventana, text=self.compra, fg="red",font=("Arial",14), command=self.compras).pack()
            self.vnt = tk.Button(self.ventana, text=self.venta, fg="green",font=("Arial",14)).pack()

        self.ventana.mainloop()


    def parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--odbc", help="Cadena odbc",default="")
        args = parser.parse_args()
        self.cadenaConeccion=args.odbc

    def compras(self):
        print(self.compra)

def main():
    objeto = LinxDolar()
    return 0

if __name__ == "__main__":
    main()

