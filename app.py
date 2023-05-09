from tkinter import *
from datetime import datetime
import time
import vlc
import threading


class App:
    
    def __init__(self):
        # Raiz principal
        self.root = Tk()
        
        # Configurando raiz principal
        self.root.title('Reloj-Despertador')
        self.root.resizable(False, False) # Impide redimensionar la ventana raiz

        
        # Configurando frame principal
        self.frame_principal = Frame(self.root, width=400, height=300)
        self.frame_principal.pack() # Empaquetamos el frame dentro de la raiz principal que es el contenedor padre
        self.frame_principal.config(bg='#aaaa7f', cursor='hand2') # El contenedor raiz se adaptará al de su frame hijo
        
        # Configurando widgets del frame principal
        self.fecha = Label(self.frame_principal)
        self.fecha.place(relx = 0.5, y=25, anchor = CENTER) # Usamos el método place para respetar las dimensiones que le dimos al frame (400*250)
        self.fecha_actual() 
        
        self.reloj = Label(self.frame_principal)
        self.reloj.place(relx = 0.5, y = 75, anchor = CENTER) # Centramos el label que muestra el reloj
        self.hora_actual()
        
        self.alarma = Button(self.frame_principal, command=self.ventana)
        self.alarma.place(relx = 0.5, y = 125, anchor = CENTER)
        self.alarma.config(text='Alarma')
        
        self.etiqueta1 = Label(self.frame_principal)
        self.etiqueta1.place(x=25, y=175)
        self.etiqueta1.config(text='Alarma activa:', font='arial 14 bold', bg='#aaaa7f')
        
        self.alarma_on = Label(self.frame_principal)
        self.alarma_on.place(x=160, y=175)
        self.alarma_on.config(bg='#aaaa7f', text='ON', font='arial 14 bold')
        
        self.etiqueta2 = Label(self.frame_principal)
        self.etiqueta2.place(x=200, y=175)
        self.etiqueta2.config(bg='red', text='OFF', font='arial 14 bold')
        
        self.mostrar_alarma = Label(self.frame_principal)
        self.mostrar_alarma.place(x=250, y=175)
        self.mostrar_alarma.config(bg='black', text='SIN ALARMA', font='arial 14 bold', fg='#4db80b', padx=5)
        
        self.stop_alarma = Button(self.frame_principal, command=self.parar_alarma)
        self.stop_alarma.place(relx = 0.5, y = 250, anchor = CENTER)
        self.stop_alarma.config(text='Stop')
        
         # HILO SECUNDARIO QUE SE ENCARGA DE HACER SONAR LA ALARMA
        self.hilo_secundario = threading.Thread(target=self.sonar_alarma)
        self.hilo_secundario.setDaemon(True) # HACEMOS FUNCIONAR EL HILO EN SEGUNDO PLANO COMO UN DAEMON DE LO CONTRARIO NOS DA EL ERROR: RuntimeError: main thread is not in main loop
        self.hilo_secundario.start()
           
        self.root.mainloop()
    
    # Fecha actual   
    def fecha_actual(self):
        fecha = datetime.now()
        salida = fecha.strftime('%d/%m/%Y')
        self.fecha.config(text=salida, font='arial 14 bold', bg='#aaaa7f')
        self.fecha.after(1000, self.fecha_actual)
    
    # Hora actual
    def hora_actual(self):
        h = time.strftime('%H:%M:%S', time.localtime())
        self.reloj.config(text=h, font='arial 16 bold', fg='#4db80b', bg='black')
        self.reloj.after(200, self.hora_actual) # El método after nos permite ejecutar la función hora_actual cada 200 milisegundos
    
    # Función que crea una instancia de la clase que inica la ventana modal
    def ventana(self):
        self.alarma_cfg = Toplevel(self.root, width=300, height=200)
        self.alarma_cfg.grab_set() # El método grab_set evita que se puedan abrir más de una ventana modal
        self.alarma_cfg.transient(self.root) # El método transiet se inicia siempre sobre la ventana padre y se oculta cuando esta última es minimizada.
        
        # Configurando los widgets
        self.etiqueta_hora = Label(self.alarma_cfg, text='Hora')
        self.etiqueta_hora.place(x=25, y=25)
        
        self.hora = Spinbox(self.alarma_cfg, from_=1, to=24, width=2)
        self.hora.place(x=75, y=25)
        
        self.etiqueta_minuto = Label(self.alarma_cfg, text='Minuto')
        self.etiqueta_minuto.place(x=25, y=75)
        
        self.minuto = Spinbox(self.alarma_cfg, from_=0, to=59, width=2)
        self.minuto.place(x=75, y=75)
        
        self.aceptar = Button(self.alarma_cfg, text='Aceptar', command=self.activar_alarma)
        self.aceptar.place(relx = 0.3, y = 150, anchor = CENTER)
        
        self.cancelar = Button(self.alarma_cfg, text='Cancelar', command=self.alarma_cfg.destroy)
        self.cancelar.place(relx = 0.7, y = 150, anchor = CENTER)
        
        self.alarma_cfg.mainloop()
        
    # Función que muestra que se ha habilitado la alarma   
    def activar_alarma(self):
        h = self.hora.get()
        format_h = self.formato_alarma(h)
        m = self.minuto.get()
        format_m = self.formato_alarma(m)
        self.mostrar_alarma.config(text='{}:{}'.format(format_h, format_m))
        self.etiqueta2.config(bg='#aaaa7f')        
        self.alarma_on.config(bg='green')
        self.alarma_cfg.destroy()
        
    # Función para cambiar formato de alarma
    def formato_alarma(self, valor):
        if valor == '0':
            valor = '00'
        if valor == '1':
            valor = '01'
        elif valor == '2':
            valor = '02'
        elif valor == '3':
            valor = '03'
        elif valor == '4':
            valor = '04'
        elif valor == '5':
            valor = '05'
        elif valor == '6':
            valor = '06'
        elif valor == '7':
            valor = '07'
        elif valor == '8':
            valor = '08'
        elif valor == '9':
            valor = '09'
        
        return valor
    
    # Sonido alarma
    def sonar_alarma(self):
        while True:
            h1 = self.reloj.cget('text')
            h = h1[:5]
            a = self.mostrar_alarma.cget('text')
            if h == a:
                archivoAudio = vlc.MediaPlayer('audio/alarm.mp3')
                archivoAudio.play()
            time.sleep(10)
    
    # Función que para la alrma programada
    def parar_alarma(self):
        self.mostrar_alarma.config(bg='black', text='SIN ALARMA', font='arial 14 bold', fg='#4db80b', padx=5)
        self.etiqueta2.config(bg='red')        
        self.alarma_on.config(bg='#aaaa7f')