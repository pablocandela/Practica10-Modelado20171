import sys
from PyQt4 import QtGui, QtCore, uic
from random import randint 
import uuid  
from xmlrpc.server import SimpleXMLRPCServer

class Vivora():
    
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]
        red, green,blue = randint(0,255), randint(0,255), randint(0,255)
        self.color = {"r": red, "g" : green, "b": blue}
        self.casillas = [] 
        self.camino = []
        self.camino = []
        self.tamaño = len(self.casillas)
        self.direccion = "Abajo" 
              
        
    def diccionario(self):
        diccionario = dict()
        diccionario = {'id': self.id,'camino': self.camino, 'color': self.color}
        return diccionario


class Servidor(QtGui.QMainWindow):

    def __init__(self):
        super(Servidor, self).__init__() 
        uic.loadUi('servidor.ui', self) 
        self.terminar.hide() 
        self.iniciar = False 
        self.pausar = False
        self.timer = 0 
        timer_s = None
        timer_camino = None
        self.vivoras = [] 
        self.agrandar_cuadros() 
        self.llenar_tabla()
        self.pushButton.clicked.connect(self.inicializa)
        self.tableWidget.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.spinBox_2.valueChanged.connect(self.actualiza_tabla) 
        self.spinBox_3.valueChanged.connect(self.actualiza_tabla)
        self.spinBox.valueChanged.connect(self.actualizar_timer)
        self.iniciar_pausar.clicked.connect(self.comenzar_juego) 
        self.terminar.clicked.connect(self.terminar_juego)
        self.show() 
          
    def aux(self):
	    self.servidor.handle_request()
    
    def nuevo_camino(self):
	    for vivora in self.vivoras:
		    vivora.camino = []
		    for celda in vivora.casillas:
			    vivora.camino.append((celda[0],celda[1]))
			
    def inicializa(self):
        puerto = self.h.value()
        direccion = self.lineEdit.text()
        print(puerto)
        self.servidor = SimpleXMLRPCServer((direccion, 0)) 
        puerto2 = self.servidor.server_address[1]
        print(puerto2)
        self.h.setValue(puerto2)
        self.pushButton.setText(str(puerto2))
        self.h.setReadOnly(True) 
        self.lineEdit.setReadOnly(True) 
        self.pushButton.setEnabled(False)
        self.servidor.register_function(self.ping)
        self.servidor.register_function(self.yo_juego)
        self.servidor.register_function(self.cambia_direccion)
        self.servidor.register_function(self.estado_del_juego)
        self.servidor.timeout = 0  
        self.timer_s = QtCore.QTimer(self)
        self.timer_s.timeout.connect(self.aux) 
        self.timer_s.start(self.servidor.timeout) 
    
    def hacer_server(self):
        self.pushButton.setText("hola")
        
    def lista_de_jugadores(self):
        lista = []
        for vivora in self.vivoras:
            lista.append(vivora.dicionario())
        return lista
	
    def ping(self):
        return "¡Pong!"
		
    def yo_juego(self):
        nueva_vivora = self.nueva_vivora()
        diccionario = {"id": serpiente_nueva.id, "color": serpiente_nueva.color}
        return diccionario
      
    def cambia_direccion(self):
        for s in self.vivoras:
            if s.id == identificador:
                if numero == 0:
                    if s.direccion is not "Abajo": 
                        s.direccion = "Arriba"
                if numero == 1:
                    if s.direccion is not "Izquierda":
                        s.direccion = "Derecha"
                if numero == 2: 
                    if s.direccion is not "Arriba":
                        s.direccion = "Abajo"
                if numero == 3: 
                    if s.direccion is not "Derecha":
                        s.direccion = "Izquierda"
        return True 
		
    def estado_del_juego(self):
        diccionario = dict()
        diccionario = {
            'espera': self.servidor.timeout, 
            'tamX': self.tableWidget.columnCount(),
            'tamY': self.tableWidget.rowCount(),
            'viboras': self.lista_de_jugadores() 
        }
        return diccionario
	
    def crear_vivora(self):
        vivora_nueva = Vivora()
        creada = False
        while not creada:
            creada = True
            uno = randint(1, self.tableWidget.rowCount()/2)
            dos = uno + 1
            tres = dos +1 
            ancho = randint(1, self.tableWidget.columnCount()-1)
            achecar_1, achecar_2, achecar_3 = [uno, ancho], [dos, ancho], [tres, ancho]
            for s in self.vivoras:
                if achecar_1 in s.casillas or achecar_2 in s.casillas or achecar_3 in s.casillas:
                    creada = False
                    break
            vivora_nueva.casillas = [achecar_1, achecar_2, achecar_3]
            self.vivoras.append(vivora_nueva)
            return vivora_nueva
    
    def actualiza_timer2(self):
        self.servidor.timeout = self.time.value() 
        self.timer_s.setInterval(self.time.value())
		
    
    def comenzar_juego(self):
        if not self.iniciar:
            self.terminar.show()
            self.crear_vivora()  
            self.iniciar_pausar.setText("Pausar Juego") 
            self.dibujar_vivoras()
            self.timer = QtCore.QTimer(self) 
            self.timer.timeout.connect(self.mover_vivoras)
            self.timer.start(100)
            self.tableWidget.installEventFilter(self) 
            self.timer_camino = QtCore.QTimer(self)
            self.timer_camino.timeout.connect(self.nuevo_camino)
            self.timer_camino.start(100)
            self.tableWidget.installEventFilter(self)
            self.iniciar = True 
        elif self.iniciar and self.pausar == False: 
            self.timer.stop() 
            self.pausar = True 
            self.iniciar_pausar.setText("Reanudar el Juego") 
        elif self.pausar: 
            self.timer.start() 
            self.pausar = False 
            self.iniciar_pausar.setText("Pausar Juego") 

    def terminar_juego(self):
        self.vivoras = [] 
        self.timer.stop()
        self.iniciar = False 
        self.terminar.hide()
        self.iniciar_pausar.setText("Iniciar Juego")  
        self.llenar_tabla() 

    def actualizar_timer(self):
        valor = self.spinBox.value()
        self.timer.setInterval(valor)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and
            source is self.tableWidget): 
                key = event.key() 
                if (key == QtCore.Qt.Key_Up and source is self.tableWidget):
                    for vivora in self.vivoras:
                        if vivora.direccion is not "Abajo":
                            vivora.direccion = "Arriba"
                elif (key == QtCore.Qt.Key_Down and source is self.tableWidget):
                    for vivora in self.vivoras:
                        if vivora.direccion is not "Arriba": vivora.direccion = "Abajo"
                elif (key == QtCore.Qt.Key_Right and source is self.tableWidget):
                    for vivora in self.vivoras:
                        if vivora.direccion is not "Izquierda": vivora.direccion = "Derecha"
                elif (key == QtCore.Qt.Key_Left and source is self.tableWidget):
                    for vivora in self.vivoras:
                        if vivora.direccion is not "Derecha": vivora.direccion = "Izquierda"
        return QtGui.QMainWindow.eventFilter(self, source, event) 

    def dibujar_vivoras(self):
        for vivora in self.vivoras:
            for parte_vivora in vivora.casillas:
                self.tableWidget.item(parte_vivora[0], parte_vivora[1]).setBackground(QtGui.QColor(vivora.color['r'], vivora.color['g'], vivora.color['b']))
    
    def se_comio(self, vivora):    
        for parte_de_vivora in vivora.casillas[0:len(vivora.casillas)-2]:           
            if vivora.casillas[-1][0] == parte_de_vivora[0] and vivora.casillas[-1][1] == parte_de_vivora[1]: return True
        return False

    def choca_con_otra_vivora(self,revisar):
        for vivora in self.vivoras:
            if vivora.id != revisar.id:
                for parte_cuerpo in vivora.casillas[:]: 
                    if revisar.casillas[-1][0] == parte_cuerpo[0] and revisar.casillas[-1][1] == parte_cuerpo[1]:
                        self.serpientes_juego.remove(serpiente_a_checar) 
		
    
    def mover_vivoras(self):
        for vivora in self.vivoras: 
            if self.se_comio(vivora) or self.choca_con_otra_vivora(vivora): 
                self.vivoras.remove(vivora) 
                self.llenar_tabla() 
                vivora_1 = self.crear_vivora() 
                self.vivoras = [vivora_1]
            self.tableWidget.item(vivora.casillas[0][0],vivora.casillas[0][1]).setBackground(QtGui.QColor(82,130,135))
            x = 0 
            for tupla in vivora.casillas[0: len(vivora.casillas)-1]:
                x += 1
                tupla[0] = vivora.casillas[x][0]
                tupla[1] = vivora.casillas[x][1]
            if vivora.direccion == "Abajo":
                if vivora.casillas[-1][0] + 1 - self.tableWidget.rowCount() < 0: vivora.casillas[-1][0] += 1
                else:
                    vivora.casillas[-1][0] = 0
            if vivora.direccion == "Derecha":
                if vivora.casillas[-1][1] + 1 - self.tableWidget.columnCount() < 0: vivora.casillas[-1][1] += 1
                else:
                    vivora.casillas[-1][1] = 0
            if vivora.direccion == "Arriba":
                if vivora.casillas[-1][0] != 0: vivora.casillas[-1][0] -= 1
                else:
                    vivora.casillas[-1][0] = self.tableWidget.rowCount()-1
            if vivora.direccion == "Izquierda":
                if vivora.casillas[-1][1] != 0: vivora.casillas[-1][1] -= 1
                else:
                    vivora.casillas[-1][1] = self.tableWidget.columnCount()-1
        self.dibujar_vivoras() 

    def llenar_tabla(self):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i,j, QtGui.QTableWidgetItem())
                self.tableWidget.item(i,j).setBackground(QtGui.QColor(80,134,134))

    def agrandar_cuadros(self):
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

    def actualiza_tabla(self):
        filas = self.spinBox_2.value()
        columnas = self.spinBox_3.value()
        self.tableWidget.setRowCount(filas) 
        self.tableWidget.setColumnCount(columnas)
        self.llenar_tabla()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv) 
    ventana = Servidor() 
    sys.exit(app.exec_()) 
