import pyodbc
import datetime
import argparse
from  urllib import request
import tkinter as tk
from  tkinter import *
from tkinter.filedialog import askopenfilename,askopenfilenames
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
#from PIL import ImageTk, Image
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

from email import encoders
import os
import configparser
import re

DEMO = False
TIMEOUT = 30

class LinxMail(object):
    def __init__(self):
        super().__init__()
        self.procesocompleto=True
        self.cadenaConeccion = ""
        self.Usuario = 0
        self.idCliente=0
        self.Enviar1=0
        self.servidorsmtp=""
        self.usuariosmtp=""
        self.requiereautenticacion=0
        self.passwordsmtp=""
        self.puertosmtp=0
        self.clienteemail=""
        self.cobranzasemail=""
        self.contactoemail=""
        self.firma={}
                          
        self.cursor = pyodbc.Cursor
        self.ventana = tk.Tk()
        self.dibujarventana()

        self.iniciar()

    def dibujarventana(self):
        self.ventana.Enviar1=tk.IntVar()
        self.ventana.Enviar2=tk.IntVar()
        self.ventana.Enviar3=tk.IntVar()
        self.ventana.EnviarCC=tk.IntVar()
        self.ventana.Leyenda=tk.StringVar()

        self.ventana.title("Envio de mails")
        self.ventana.geometry("450x450")
        self.ventana.resizable(False,False)
        self.ventana.iconbitmap("linx.ico")
        self.ventana.Leyenda.set("")

        self.ventana.chkEnviar1 = Checkbutton(self.ventana,text="Mail del Cliente",variable=self.ventana.Enviar1)
        self.ventana.chkEnviar2 = Checkbutton(self.ventana,text="Mail de Administracion",variable=self.ventana.Enviar2)
        self.ventana.chkEnviar3 = Checkbutton(self.ventana,text="Mail de Cobranzas",variable=self.ventana.Enviar3)
        self.ventana.chkEnviarCC = Checkbutton(self.ventana,text="Con Copia",variable=self.ventana.EnviarCC)

        self.ventana.txtAsunto = Entry(self.ventana)
        self.ventana.txtMail1 = Entry(self.ventana)
        self.ventana.txtMail2= Entry(self.ventana)
        self.ventana.txtMail3=Entry(self.ventana)
        self.ventana.txtMailCC= Entry(self.ventana)
        self.ventana.txtAdjunto = Entry(self.ventana,text="Archivo adjunto")
        self.ventana.txtMensaje= ScrolledText(self.ventana,width=41,height=6)

        self.ventana.lblLeyenda= Label(self.ventana,fg="green",font=("Verdana",11),textvariable=self.ventana.Leyenda)
        self.ventana.lblAsunto= Label(self.ventana,text="Asunto",font=("Verdana",8))
        self.ventana.lblMensaje= Label(self.ventana,text="Mensaje",font=("Verdana",8))
        self.ventana.lblArchivo= Label(self.ventana,font=("Verdana",10),text="Seleccionar Adjunto")
        self.ventana.btnFirma =tk.Button(self.ventana, text="Firma",fg="blue",font=("Arial",14), command=lambda: FirmaShow(self.usuario))
        self.ventana.btnEnviar =tk.Button(self.ventana, text="Enviar",fg="green",font=("Arial",14), command=self.enviar)
        self.ventana.btnSalir =tk.Button(self.ventana, text="Cerrar",fg="red",font=("Arial",14), command=self.salir)
        self.ventana.btnBuscaArchivo = Button(self.ventana, text='...',bg="blue",fg="white",command=self.getfile)

        self.ventana.chkEnviar1.place(y=10,x=10)
        self.ventana.txtMail1.place(y=10,x=170,width=250)
        self.ventana.chkEnviar2.place(y=40,x=10)
        self.ventana.txtMail2.place(y=40,x=170,width=250)
        self.ventana.chkEnviar3.place(y=70,x=10)
        self.ventana.txtMail3.place(y=70,x=170,width=250)
        self.ventana.chkEnviarCC.place(y=100,x=10)
        self.ventana.txtMailCC.place(y=100,x=170,width=250)
        self.ventana.lblAsunto.place(y=130,x=15)
        self.ventana.txtAsunto.place(y=130,x=90,width=330)
        self.ventana.lblMensaje.place(y=160,x=15)
        self.ventana.txtMensaje.place(y=160,x=90)
        self.ventana.lblArchivo.place(y=270,x=150)
        self.ventana.txtAdjunto.place(y=300,x=30,width=360)
        self.ventana.btnBuscaArchivo.place(y=295,x=400)
        self.ventana.lblLeyenda.place(y=340,x=30,width=400)
        self.ventana.btnFirma.place(y=370,x=50,width=100,heigh=50)
        self.ventana.btnEnviar.place(y=370,x=160,width=100,heigh=50)
        self.ventana.btnSalir.place(y=370,x=270,width=100,heigh=50)

    def salir(self):
        self.ventana.destroy()

    def iniciar(self):
        self.parser()
        if self.ConeccionODBC():
            if self.ConfigGet():
                if self.idCliente:
                    self.ClienteGet()
                else:
                    self.ventana.Enviar1.set(1)
                if self.archivo:
                    if not self.idCliente:
                        self.ventana.txtMensaje.insert("1.0","Enviamos el archivo solicitado\n\nAtte.")
                    self.ventana.txtAdjunto.insert(0,self.archivo)
            self.ventana.Leyenda.set("")
            self.ventana.mainloop()

    def parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--odbc", help="Cadena odbc",default="DSN=margarita")
        parser.add_argument("-c", "--idcliente", help="Cliente",default=0)
        parser.add_argument("-a", "--archivo", help="Archivo",default="")
        parser.add_argument("-s", "--asunto", help="Asunto",default="")
        parser.add_argument("-u", "--usuario", help="Usuario",default=0)

        args = parser.parse_args()
        self.cadenaConeccion=args.odbc
        self.idCliente=args.idcliente
        self.archivo=args.archivo
        self.usuario=str(args.usuario)
        self.ventana.txtAsunto.insert(0,args.asunto)

    def progreso(self,mensaje):
        self.ventana.lblLeyenda.config(fg='green')
        self.ventana.Leyenda.set(mensaje)

    def error(self,mensaje="Error"):
        self.ventana.lblLeyenda.config(fg='red')
        self.ventana.Leyenda.set(mensaje)
        self.ventana.config(cursor="")

    def ConeccionODBC(self):
        try:
            self.progreso("Conectando a "+self.cadenaConeccion)
            cnxn = pyodbc.connect(self.cadenaConeccion, autocommit=True)
            self.cursor = cnxn.cursor()
            return True
        except:
            self.error('No existe la cadena de coneccion:'+self.cadenaConeccion)
            return False

    def ClienteGet(self):
        cadenaSQL= """ 
                   select  nombrecliente, 
                           email, 
                           contactoemail,
                           cobranzasemail
                           from vclientes 
                           where idcliente= ?
                   """

        self.cursor.execute(cadenaSQL,self.idCliente)

        row = self.cursor.fetchone()
        if row:
            if row.email:
                self.clienteemail=row.email
                self.ventana.Enviar1.set(1)
                self.ventana.txtMail1.insert(0,row.email)
            if row.contactoemail:
                self.contactoemail=row.contactoemail
                self.ventana.Enviar2.set(1)
                self.ventana.txtMail2.insert(0,row.contactoemail)
            if row.cobranzasemail:
                self.cobranzasemail=row.cobranzasemail
                self.ventana.Enviar3.set(1)
                self.ventana.txtMail3.insert(0,row.cobranzasemail)

            self.ventana.txtMensaje.insert("1.0","Sres "+row.nombrecliente+" enviamos el archivo solicitado\n\nAtte.")

        self.ventana.update()

    def ClientePut(self):
        if  (self.idCliente and
                not ((self.clienteemail == self.ventana.txtMail1.get()) and
                    (self.contactoemail == self.ventana.txtMail2.get()) and
                    (self.cobranzasemail == self.ventana.txtMail3.get()))):
            if messagebox.askyesno("Actualizar","Desea actualizar los datos del cliente"):
                cadenaSQL= """
                        update vclientes set
                                email=?,
                                contactoemail=?,
                                cobranzasemail=?
                                where idcliente= ?
                        """
                parametros=(self.ventana.txtMail1.get(),self.ventana.txtMail2.get(),self.ventana.txtMail3.get(),self.idCliente)
                self.cursor.execute(cadenaSQL,parametros)

    def ConCopiaGet(self):
        ccfirma = configparser.ConfigParser()
        ccfirma.read('firmas.ini')
        try:
            ccfirma.get(self.usuario, 'cc')
        except:
            return ""
        return ccfirma.get(self.usuario, 'cc')

    def ConCopiaPut(self):
        ccfirma = configparser.ConfigParser()
        ccfirma.read('firmas.ini')
        ccfirma.set(self.usuario, 'cc', self.ventana.txtMailCC.get())
        with open('firmas.ini', 'w') as configfirma:
            ccfirma.write(configfirma)

    def ConfigGet(self):
        cadenaSQL= """
                   select  servidorsmtp, 
                           {fn convert(puertosmtp,SQL_INTEGER)} as puertosmtp,
                           {fn convert(requiereautenticacion,SQL_INTEGER)} as requiereautenticacion,
                           usuariosmtp,
                           passwordsmtp
                           from vSetup 
                           where servidorsmtp<>''
                   """

        self.cursor.execute(cadenaSQL)

        row = self.cursor.fetchone()
        if row:
            self.servidorsmtp=row.servidorsmtp
            self.puertosmtp=row.puertosmtp
            self.requiereautenticacion=row.requiereautenticacion
            self.usuariosmtp=row.usuariosmtp
            self.passwordsmtp=row.passwordsmtp
            self.ventana.txtMailCC.delete(0,tk.END)
            self.ventana.txtMailCC.insert(0,self.ConCopiaGet()) #Con copiadel ini
            if self.usuariosmtp and self.ventana.txtMailCC.get()=="":
                self.ventana.txtMailCC.insert(0,row.usuariosmtp)
            if not self.ventana.txtMailCC.get()=="":
                self.ventana.EnviarCC.set(1)
        if self.servidorsmtp=="":
            self.error("No esta configurado el servidor de correo")
            return False
        return True


    def getfile(self):
        files=askopenfilenames()
        for file in files:
            if self.ventana.txtAdjunto.get():
                self.ventana.txtAdjunto.insert(tk.END,";")
            self.ventana.txtAdjunto.insert(tk.END,file)

    def enviar(self):
        self.progreso("Enviando mail...")

        if not self.FirmaOK():
            self.progreso("No tiene Configurada la firma")
            return

        msg=self.MensajeGet()

        if self.ConfigGet():
           if ((self.ventana.Enviar1.get()==1 and self.ventana.txtMail1.get()) or
                (self.ventana.Enviar2.get()==1 and self.ventana.txtMail2.get()) or
                (self.ventana.Enviar3.get()==1 and self.ventana.txtMail3.get())):
                try:
                    s = smtplib.SMTP(host=self.servidorsmtp, port=self.puertosmtp,timeout=TIMEOUT)  # servidor y puerto
                except:
                    self.error("SMTPException")
                    return

                """except smtplib.SMTPException:
                    self.error("SMTPException")
                    return
                except smtplib.SMTPResponseException:
                    self.error("SMTPResponseException")
                    return
                except smtplib.SMTPSenderRefused:
                    self.error("SMTPSenderRefused")
                    return
                except smtplib.SMTPRecipientsRefused:
                    self.error("SMTPRecipientsRefused")
                    return
                except smtplib.SMTPConnectError:
                    self.error("SMTPConnectError")
                    return
                except smtplib.SMTPHeloError:
                    self.error("SMTPHeloError")
                    return
                except smtplib.SMTPNotSupportedError:
                    self.error("SMTPNotSupportedError")
                    return
                except smtplib.SMTPAuthenticationError:
                    self.error("SMTPAuthenticationError")
                    return
                """
                if self.requiereautenticacion==1:
                    try:
                        s.starttls()  # Conexion tls
                    except smtplib.SMTPNotSupportedError:
                        self.error("El servidor NO requiere autenticacion")
                        return
                try:
                    s.login(
                        self.usuariosmtp, self.passwordsmtp
                    )  # Iniciar sesion con los datos de acceso al servidor SMTP
                except smtplib.SMTPAuthenticationError:
                    self.error("Error de Autenticacion")
                    return
                except smtplib.SMTPNotSupportedError:
                    self.error("El servidor requiere autenticacion")
                    return
                except Exception as error:
                    self.error(error)
                    return

                try:
                    if DEMO==False:
                        s.send_message(msg)
                    self.progreso("Mail enviado!")
                    self.ventana.config(cursor="")
                    #Grabo con copia
                    if self.ventana.EnviarCC.get()==1 and not self.ventana.txtMailCC.get() == "":
                        self.ConCopiaPut()
                    if self.idCliente:
                        self.ClientePut()
                except Exception as error:
                    self.error("Enviar "+error)
           else:
                self.error("No hay direcciones seleccionadas para enviar")
        else:
            self.error("Error de configuracion")

    def MensajeGet(self):
        msg = MIMEMultipart()
        # Configurar los parametros del mensaje
        msgTo=[]
        #<<Ajuntos
        if self.ventana.txtAdjunto.get():
            for archivo in self.ventana.txtAdjunto.get().split(";"):
                if archivo:
                    adjunto=archivo.replace("\\","/")
                    if os.path.exists(adjunto):
                        msg.attach(load_file(adjunto,'"'+os.path.basename(adjunto)+'"'))
                    else:
                        self.error("No existe el archivo "&adjunto)


        if self.ventana.txtAsunto.get():
            msg["Subject"] = self.ventana.txtAsunto.get()
        if self.firma["mail"]:
            msg["From"] = self.firma["nombre"]+' <'+self.firma["mail"]+'>'
        else:
            msg["From"] = self.firma["nombre"]+' <'+self.usuariosmtp+'>'

        if self.ventana.Enviar1.get()==1 and self.ventana.txtMail1.get():
            msgTo.append(self.ventana.txtMail1.get())
        if self.ventana.Enviar2.get()==1 and self.ventana.txtMail2.get():
            msgTo.append(self.ventana.txtMail2.get())
        if self.ventana.Enviar3.get()==1 and self.ventana.txtMail3.get():
            msgTo.append(self.ventana.txtMail3.get())
        msg["To"]=','.join(msgTo)

        if self.ventana.EnviarCC.get()==1 and self.ventana.txtMailCC.get():
            msg["Cc"] = self.ventana.txtMailCC.get()
        if self.ventana.txtMensaje.get("1.0",tk.END):
            msg.attach(MIMEText(self.ventana.txtMensaje.get("1.0",tk.END),'plain'))

        html = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">'
        html =html+self.firma['htmlcabezera']
        html=html+'<a href="'+self.firma['pagina']+'" target="_blank"><img src="cid:logo1" width="'+self.firma['logoancho']+'" height="'+self.firma['logoalto']+'" style="padding-top:15px;" alt=""></a></td>'
        if self.firma['logosolo']=='0':
            html=html+'<td width="430" height="170" style="padding-left:25px; font-family: Helvetica, Arial, sans-serif; font-size:10px; border:1px solid #333c87; border-left: none; border-right: none; line-height:10px;" valign="bottom">'
            html=html+'<p style="font-size:12px;"><b>'+self.firma['titulo']+' '+self.firma['nombre']+'</b></p>'
            if self.firma['cargo']:
                html=html+'<p style="font-size=10px;"><b>'+self.firma['cargo']+'</b></p>'
            if self.firma['mail']:
                html=html+'<p style="line-height:10px;"><b>Mail: '+self.firma['mail']+'</b></p>'
            if self.firma['telefono']:
                html=html+'<p style="line-height:10px;"><b>Teléfono: '+self.firma['telefono']+'</b></p>'
            if self.firma['localidad']:
                html=html+self.firma['localidad']+'&middot; '+self.firma['provincia']+'&middot; '+self.firma['pais']+'</p>'
            html=html+'</td>'
        if self.firma['logo']:
            logo = open(self.firma['logo'], 'rb')
            msgImage = MIMEImage(logo.read())
            logo.close()
            msgImage.add_header('Content-ID', '<logo1>')
            msg.attach(msgImage)

        if self.firma['contacto1'] or self.firma['contacto2'] or self.firma['contacto3']:
            html=html+'<td><p><b>Síguenos en:</b></p>'
            if self.firma['contacto1'] or self.firma['contacto2'] or self.firma['contacto3']:
                html=html+'<p>'
            if self.firma['contacto1']:
                html=html+'<a href="'+self.firma['contacto1']+'" target="_blank"><img src="cid:logof" width="32" height="32" alt=""></a>'
                try:
                    logo = open('contacto1.png', 'rb')
                    msgImage = MIMEImage(logo.read())
                    logo.close()
                    msgImage.add_header('Content-ID', '<logof>')
                    msg.attach(msgImage)
                except:
                    self.progreso('No existe el icono (png) de contacto1 en la carpeta')
            if self.firma['contacto2']:
                html=html+'<a href="'+self.firma['contacto2']+'" target="_blank"><img src="cid:logot" width="32" height="32" alt=""></a>'
                try:
                    logo = open('contacto2.png', 'rb')
                    msgImage = MIMEImage(logo.read())
                    logo.close()
                    msgImage.add_header('Content-ID', '<logot>')
                    msg.attach(msgImage)
                except:
                    self.progreso('No existe el icono (png) de contacto2 en la carpeta')
            if self.firma['contacto3']:
                html=html+'<a href="'+self.firma['contacto3']+'" target="_blank"><img src="cid:logog" width="32" height="32" alt=""></a>'
                try:
                    logo = open('contacto3.png', 'rb')
                    msgImage = MIMEImage(logo.read())
                    logo.close()
                    msgImage.add_header('Content-ID', '<logog>')
                    msg.attach(msgImage)
                except:
                    self.progreso('No existe el icono (png) de contacto3 en la carpeta')
            if self.firma['contacto1'] or self.firma['contacto2'] or self.firma['contacto3']:
                html=html+'</p></td>'

        html=html+'</tr></table></html>'
        msg.attach(MIMEText(html,'html'))

        return msg


    def FirmaOK(self):
        firma = configparser.ConfigParser()
        firma.read('firmas.ini')
        if self.usuario not in firma.sections():
            return FALSE
        if not firma[self.usuario]["nombre"]:
            return FALSE
        self.firma=dict(firma.items(self.usuario))
        self.firma["nombre"]=re.sub(r"[^a-zA-Z0-9 ]","",self.firma["nombre"])
        if '@' not in self.firma['mail']:
            return FALSE

        return TRUE

def FirmaShow(usuario):
    global wFirmas
    firma = configparser.ConfigParser()
    firma.read('firmas.ini')

    if usuario not in firma.sections():
        firma.add_section(usuario)
        firma.set(usuario, 'nombre', '')
        firma.set(usuario, 'titulo', '')
        firma.set(usuario, 'cargo', '')
        firma.set(usuario, 'telefono', '')
        firma.set(usuario, 'mail', '')
        firma.set(usuario, 'provincia', '')
        firma.set(usuario, 'localidad', '')
        firma.set(usuario, 'pais', '')
        firma.set(usuario, 'contacto1', '')
        firma.set(usuario, 'contacto2', '')
        firma.set(usuario, 'contacto3', '')
        firma.set(usuario, 'pagina', '')
        firma.set(usuario, 'logo', '')
        firma.set(usuario, 'logosolo', '0')
        firma.set(usuario, 'logoalto', '100')
        firma.set(usuario, 'logoancho', '150')

    wFirmas = tk.Toplevel()
    wFirmas.title("Configuracion de Firmas de Mails")
    wFirmas.geometry("450x450")
    wFirmas.resizable(False,False)
    wFirmas.iconbitmap("linx.ico")
    wFirmas.logosolo=tk.IntVar()

    wFirmas.txtNombre = Entry(wFirmas,width=50)
    wFirmas.txtTitulo = Entry(wFirmas,width=50)
    wFirmas.txtCargo = Entry(wFirmas,width=50)
    wFirmas.txtTelefono = Entry(wFirmas,width=50)
    wFirmas.txtMail = Entry(wFirmas,width=50)
    wFirmas.txtProvincia = Entry(wFirmas,width=50)
    wFirmas.txtLocalidad = Entry(wFirmas,width=50)
    wFirmas.txtPais = Entry(wFirmas,width=50)
    wFirmas.txtcontacto1 = Entry(wFirmas,width=50)
    wFirmas.txtcontacto2 = Entry(wFirmas,width=50)
    wFirmas.txtcontacto3 = Entry(wFirmas,width=50)
    wFirmas.txtPagina = Entry(wFirmas,width=50)
    wFirmas.txtLogo = Entry(wFirmas,width=50)
    wFirmas.txtLogoAlto = Entry(wFirmas,width=15)
    wFirmas.txtLogoAncho = Entry(wFirmas,width=15)

    wFirmas.chkLogoSolo= Checkbutton(wFirmas,text="Solo el logo",variable=wFirmas.logosolo)

    wFirmas.lblNombre = Label(wFirmas,text="Nombre",font=("Verdana",8))
    wFirmas.lblTitulo = Label(wFirmas,text="Título",font=("Verdana",8))
    wFirmas.lblCargo = Label(wFirmas,text="Cargo",font=("Verdana",8))
    wFirmas.lblTelefono = Label(wFirmas,text="Telefono",font=("Verdana",8))
    wFirmas.lblMail = Label(wFirmas,text="Mail",font=("Verdana",8))
    wFirmas.lblProvincia = Label(wFirmas,text="Provincia",font=("Verdana",8))
    wFirmas.lblLocalidad = Label(wFirmas,text="Localidad",font=("Verdana",8))
    wFirmas.lblPais = Label(wFirmas,text="Pais",font=("Verdana",8))
    wFirmas.lblcontacto1 = Label(wFirmas,text="contacto1",font=("Verdana",8))
    wFirmas.lblcontacto2 = Label(wFirmas,text="contacto2",font=("Verdana",8))
    wFirmas.lblcontacto3 = Label(wFirmas,text="contacto3+",font=("Verdana",8))
    wFirmas.lblPagina = Label(wFirmas,text="Pagina Web",font=("Verdana",8))
    wFirmas.lblLogo = Label(wFirmas,text="Logo",font=("Verdana",8))
    wFirmas.lblLogoAlto = Label(wFirmas,text="Alto",font=("Verdana",8))
    wFirmas.lblLogoAncho = Label(wFirmas,text="Ancho",font=("Verdana",8))
    wFirmas.btnLogo = Button(wFirmas, text='...',bg="blue",fg="white",command=FirmaGetFile)

    wFirmas.btnOk   =tk.Button(wFirmas, text="Grabar",fg="green",font=("Arial",14), command=lambda: FirmaOk(usuario,firma))
    wFirmas.btnSalir=tk.Button(wFirmas, text="Salir",fg="red",font=("Arial",14), command=wFirmas.destroy)

    wFirmas.txtNombre.insert(0,firma.get(usuario, 'nombre'))
    wFirmas.txtTitulo.insert(0,firma.get(usuario, 'titulo'))
    wFirmas.txtCargo.insert(0,firma.get(usuario, 'cargo'))
    wFirmas.txtTelefono.insert(0,firma.get(usuario, 'telefono'))
    wFirmas.txtMail.insert(0,firma.get(usuario, 'mail'))
    wFirmas.txtProvincia.insert(0,firma.get(usuario, 'provincia'))
    wFirmas.txtLocalidad.insert(0,firma.get(usuario, 'localidad'))
    wFirmas.txtPais.insert(0,firma.get(usuario, 'pais'))
    wFirmas.txtcontacto1.insert(0,firma.get(usuario, 'contacto1'))
    wFirmas.txtcontacto2.insert(0,firma.get(usuario, 'contacto2'))
    wFirmas.txtcontacto3.insert(0,firma.get(usuario, 'contacto3'))
    wFirmas.txtPagina.insert(0,firma.get(usuario, 'pagina'))
    wFirmas.txtLogo.insert(0,firma.get(usuario, 'logo'))
    wFirmas.logosolo.set(firma.get(usuario, 'logosolo'))
    wFirmas.txtLogoAncho.insert(0,firma.get(usuario, 'logoancho'))
    wFirmas.txtLogoAlto.insert(0,firma.get(usuario, 'logoalto'))
    wFirmas.lblNombre.place(x=10,y=10)
    wFirmas.txtNombre.place(x=120,y=10)
    wFirmas.lblTitulo.place(x=10,y=35)
    wFirmas.txtTitulo.place(x=120,y=35)
    wFirmas.lblCargo.place(x=10,y=60)
    wFirmas.txtCargo.place(x=120,y=60)
    wFirmas.lblTelefono.place(x=10,y=85)
    wFirmas.txtTelefono.place(x=120,y=85)
    wFirmas.lblMail.place(x=10,y=110)
    wFirmas.txtMail.place(x=120,y=110)
    wFirmas.lblProvincia.place(x=10,y=135)
    wFirmas.txtProvincia.place(x=120,y=135)
    wFirmas.lblLocalidad.place(x=10,y=160)
    wFirmas.txtLocalidad.place(x=120,y=160)
    wFirmas.lblPais.place(x=10,y=185)
    wFirmas.txtPais.place(x=120,y=185)
    wFirmas.lblcontacto1.place(x=10,y=210)
    wFirmas.txtcontacto1.place(x=120,y=210)
    wFirmas.lblcontacto2.place(x=10,y=235)
    wFirmas.txtcontacto2.place(x=120,y=235)
    wFirmas.lblcontacto3.place(x=10,y=260)
    wFirmas.txtcontacto3.place(x=120,y=260)
    wFirmas.lblPagina.place(x=10,y=285)
    wFirmas.txtPagina.place(x=120,y=285)
    wFirmas.chkLogoSolo.place(x=10,y=310)
    wFirmas.txtLogo.place(x=120,y=310)
    wFirmas.btnLogo.place(x=430,y=310)
    wFirmas.lblLogoAlto.place(x=10,y=335)
    wFirmas.txtLogoAlto.place(x=120,y=335)
    wFirmas.lblLogoAncho.place(x=10,y=360)
    wFirmas.txtLogoAncho.place(x=120,y=360)

    wFirmas.btnOk.place(x=100,y=385,width=100,heigh=50)
    wFirmas.btnSalir.place(x=250,y=385,width=100,heigh=50)
    wFirmas.mainloop()

def FirmaOk(usuario,firma):
    firma.set(usuario, 'nombre', wFirmas.txtNombre.get())
    firma.set(usuario, 'titulo', wFirmas.txtTitulo.get())
    firma.set(usuario, 'cargo', wFirmas.txtCargo.get())
    firma.set(usuario, 'telefono', wFirmas.txtTelefono.get())
    firma.set(usuario, 'mail', wFirmas.txtMail.get())
    firma.set(usuario, 'provincia', wFirmas.txtProvincia.get())
    firma.set(usuario, 'localidad', wFirmas.txtLocalidad.get())
    firma.set(usuario, 'pais', wFirmas.txtPais.get())
    firma.set(usuario, 'contacto1', wFirmas.txtcontacto1.get())
    firma.set(usuario, 'contacto2', wFirmas.txtcontacto2.get())
    firma.set(usuario, 'contacto3', wFirmas.txtcontacto3.get())
    firma.set(usuario, 'pagina', wFirmas.txtPagina.get())
    firma.set(usuario, 'logo', wFirmas.txtLogo.get())
    firma.set(usuario, 'logoancho', wFirmas.txtLogoAncho.get())
    firma.set(usuario, 'logoalto', wFirmas.txtLogoAlto.get())
    firma.set(usuario, 'logosolo', str(wFirmas.logosolo.get()))
    try:
        firma.get(usuario, 'htmlcabezera')
    except:
        firma.set(usuario, 'htmlcabezera','<html><table><tr><td width="100" height="180" style="border:1px solid #333c87; border-right: none; border-left: none;" align="right" valign="top">')

    with open('firmas.ini', 'w') as configfirma:
        firma.write(configfirma)
    wFirmas.destroy()

def FirmaGetFile():
    file=askopenfilename()
    wFirmas.txtLogo.delete(0,tk.END)
    wFirmas.txtLogo.insert(0,file)

def load_file(file, file_name):

    read_file = open(file, "rb")
#    attach = MIMEBase("multipart", "encrypted")
    attach = MIMEBase('application', 'octet-stream')
    attach.set_payload(read_file.read())
    read_file.close()
    encoders.encode_base64(attach)
#    attach.add_header("Content-Disposition", "attachment", filename=file_name)
    attach.add_header("Content-Disposition", "attachment; filename= {0}".format(file_name))

    return attach

def main():
    objeto = LinxMail()
    return 0

if __name__ == "__main__":
    main()

