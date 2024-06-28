import tkinter
import pyodbc
import datetime
import argparse
import requests
from urllib import request
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askopenfilenames
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
# from PIL import ImageTk, Image
import threading
import os
import configparser
import re
from datetime import datetime

URL="https://api-dolar-argentina.herokuapp.com/api/"

class LinxDolar(object) :
    def __init__(self) :
        super().__init__()

        self.cadenaConeccion = ""
        self.URL=""
        self.idmoneda = ""
        self.nombre = ""
        self.conversionSistema = 0
        self.compra = 0
        self.venta = 0
        self.ultimafecha=''
        self.ultimahora=''
        self.ultimousuario=''
        self.variacion=0
        self.usuario = ""
        self.cursor = pyodbc.Cursor
        self.ventana = tk.Tk()
        self.dibujarventana()

        self.iniciar()

    def parser(self) :
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--odbc", help="Cadena odbc", default="")
        parser.add_argument("-u", "--url", help="Url", default="")
        parser.add_argument("-id", "--id", help="Id moneda", default="")
        parser.add_argument("-user", "--user", help="Usuario", default="")

        args = parser.parse_args()
        self.cadenaConeccion = args.odbc
        self.URL = URL+args.url
        self.idmoneda = args.id
        self.usuario = args.user

    def dibujarventana(self) :
        self.nombre = tk.StringVar()
        self.compra = tk.IntVar()
        self.venta = tk.IntVar()
        self.ventana.Leyenda=tk.StringVar()

        self.ventana.title("Cotizacion Moneda Hoy")
        self.ventana.geometry('200x250')
        self.ventana.resizable(0, 0)
        self.ventana.iconbitmap("linx.ico")
        self.ventana.Leyenda.set("")

        self.ventana.lblLeyenda= Label(self.ventana,fg="red",font=("Verdana",11),textvariable=self.ventana.Leyenda)
        self.ventana.lblConversionA = tk.Label(self.ventana, text="Cotizacion Actual", font=("Verdana", 10))
        self.ventana.lblCompra = tk.Label(self.ventana, text="Compra", font=("Verdana", 10))
        self.ventana.lblVenta = tk.Label(self.ventana, text="Venta", font=("Verdana", 10))
        self.ventana.lblConversionS = tk.Label(self.ventana, text="Ult. Cotizacion", font=("Verdana", 7))
        self.ventana.btnGrabar = tk.Button(self.ventana, text='Grabar',
                                   command=self.grabar)
        self.ventana.btnSalir = tk.Button(self.ventana, text='Salir',
                                  command=self.salir)

        self.ventana.lblConversionA.place(y=25, x=40)
        self.ventana.lblCompra.place(y=45, x=30)
        self.ventana.lblVenta.place(y=45, x=120)
        self.ventana.lblConversionS.place(y=105, x=0)
        self.ventana.btnGrabar.place(y=200, x=10, width=80,heigh=30)
        self.ventana.btnSalir.place(y=200, x=110, width=80,heigh=30)
        self.ventana.lblLeyenda.place(y=200,x=30,width=150)


    def iniciar(self) :
        self.parser()
        if self.ConeccionODBC():
            json = requests.get(self.URL).json()
            self.compra = json['compra']
            self.venta = json['venta']
            self.MonedaGet()

            self.ventana.lblMoneda = Label(self.ventana,text=self.nombre, bg="#1F9CDC", fg="white", font=("Verdana",14))
            self.ventana.btnCompra = tk.Button(self.ventana, text=self.compra, fg="red", font=("Arial", 14))
            self.ventana.btnVenta = tk.Button(self.ventana, text=self.venta, fg="green", font=("Arial", 14))
            self.ventana.lblConversion = Label(self.ventana,text=self.conversionSistema,fg="blue", font=("Verdana",14))
            self.ventana.lblUltimaFecha = Label(self.ventana,text=self.ultimafecha, font=("Verdana",7))
            self.ventana.lblUltimaHora = Label(self.ventana,text=self.ultimahora, font=("Verdana",7))

            self.ventana.lblMoneda.place(y=0,x=0,width=200)
            self.ventana.lblConversion.place(y=120,x=0,width=200)
            self.ventana.btnCompra.place(y=65,x=20)
            self.ventana.btnVenta.place(y=65,x=100)
            self.ventana.lblUltimaHora.place(y=105,x=148)
            self.ventana.lblUltimaFecha.place(y=105,x=78)

            self.ventana.Leyenda.set("")
            self.ventana.mainloop()
        else:
            print("No existe Conexion ODBC")


    def grabar(self) :
        hora = datetime.today().strftime("%H:%M")
        fecha = datetime.today().strftime("%Y-%m-%d")
        #Actualizo la tabla gmoneda
        cadenaSQL= """
                        update gmoneda set
                                conversionmoneda=?
                                where idmoneda= ?
                        """
        parametros=(self.venta,self.idmoneda)
        self.cursor.execute(cadenaSQL,parametros)

        #Busco si existen datos en gmonedamovimientos
        cadenaSQL=  """
                        select  idautonumber
                                from gmonedamovimientos
                                where idmoneda=? 
                                and {fn convert(fecha,SQL_DATE)}=?
                                and hora=?
                                
                    """
        parametros=(self.idmoneda,fecha,hora)
        self.cursor.execute(cadenaSQL,parametros)
        row = self.cursor.fetchone()
        if row:
            try:
                cadenaSQL= """
                                update gmonedamovimientos set
                                       conversionmoneda=?
                                       where idautonumber= ?
                            """
                parametros=(float(self.venta),row.idautonumber)
                self.cursor.execute(cadenaSQL,parametros)
                self.salir()
                return True
            except:
                self.error('No se puede grabar movimiento en moneda: '+self.idmoneda)
                return False
        else:
            cadenaSQL=  """
                            select  max(idautonumber)+1 as id
                                    from gmonedamovimientos
                        """
            self.cursor.execute(cadenaSQL)
            row = self.cursor.fetchone()
            cadenaSQL= """
                            insert into gmonedamovimientos
                                   (
                                   hora,
                                   usuario,
                                   idautonumber,
                                   idmoneda,
                                   conversionmoneda,
                                   fecha
                                   ) values 
                                   (
                                   ?,
                                   ?,
                                   ?,
                                   ?,
                                   ?,
                                   ?)
                        """
            parametros=(hora,self.usuario,row.id,self.idmoneda,float(self.venta),fecha)
            self.cursor.execute(cadenaSQL,parametros)
            self.salir()
            return True

    def salir(self) :
        self.ventana.destroy()

    def ConeccionODBC(self):
        try:
            cnxn = pyodbc.connect(self.cadenaConeccion, autocommit=True)
            self.cursor = cnxn.cursor()
            return True
        except:
            self.error('No existe la cadena de coneccion:'+self.cadenaConeccion)
            return False

    def MonedaGet(self):
        cadenaSQL= """
                   select  idmoneda,
                           descripcion,
                           conversionmoneda
                           from gmoneda
                           where idmoneda= ?
                   """
        self.cursor.execute(cadenaSQL,self.idmoneda)
        row = self.cursor.fetchone()
        if row:
            self.nombre=row.descripcion
            self.conversionSistema=row.conversionmoneda
            cadenaSQL= """
                      select  fecha,
                              hora,
                              usuario,
                              conversionmoneda
                              from gmonedamovimientos 
                              where idmoneda= ?
                              order by fecha desc,hora desc
                      """
            self.cursor.execute(cadenaSQL,self.idmoneda)
            row = self.cursor.fetchone()
            if row:
                self.ultimafecha=row.fecha
                self.ultimahora=row.hora
                self.ultimousuario=row.usuario
            else:
                self.ultimafecha='S/D'
                self.ultimahora=''
                self.ultimousuario=''
        else:
            messagebox.showerror(message="LA MONEDA: "+self.idmoneda+ " NO EXISTE", title="ERROR")
            self.salir()

    def error(self,mensaje="Error"):
        self.ventana.lblLeyenda.config(fg='red')
        self.ventana.Leyenda.set(mensaje)
        self.ventana.config(cursor="")

def check_sql_string(sql, values):
    unique = "%PARAMETER%"
    sql = sql.replace("?", unique)
    for v in values: sql = sql.replace(unique, repr(v), 1)
    return sql


def main() :
    objeto = LinxDolar()
    return 0


if __name__ == "__main__" :
    main()
