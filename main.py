#  main.py
#  
#  Copyright 2017 josef <josef@CODER>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from PyQt4 import QtGui, QtCore
import sys
import layout


class Storage():
    """
    This will be the data interface
    """
    def __init__(self):
        pass
        
    def getClients(self):
        #   return dictionary of client names; client ids
        clients = { 'Client 1':1, 'Client 2':2 }
        return clients
        
        
    def addClient(self, name):
        #   add
        #   return id?
        pass
        
    def removeClient(self):
        pass
        
    
    
    

class TimeMachineApp(QtGui.QMainWindow, layout.Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(TimeMachineApp, self).__init__(parent)
        self.setupUi(self)
        
        #self.actionExit.triggered.connect(QtGui.qApp.quit)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL('triggered()'), QtGui.qApp.quit)
        #self.actionEdit_Clients.triggered.connect(self.editClients)
        QtCore.QObject.connect(self.actionEdit_Clients, QtCore.SIGNAL('triggered()'), editClients)
        
        
        #   read storage
        storage = Storage()
        
        #   add client buttons from storage list
        


        #   init logical container for client buttons; not sure if this is worth the trouble except for id feature
        self.clientButtonGroup = QtGui.QButtonGroup()

        #   add buttons to layout and logical contaner
        print(storage.getClients())
        
        for clientId, clientName in storage.getClients().items():
            print("{}:{}".format(clientId, clientName))
                self.btnClient1 = QtGui.QPushButton("Client 1", self.verticalLayoutWidget)
                self.btnClient1.setCheckable(True)
                self.verticalLayout.addWidget(self.btnClient1)
                self.clientButtonGroup.addButton(self.btnClient1, 1)
            
            
        self.btnClient1 = QtGui.QPushButton("Client 1", self.verticalLayoutWidget)
        self.btnClient1.setCheckable(True)
        self.verticalLayout.addWidget(self.btnClient1)
        self.clientButtonGroup.addButton(self.btnClient1, 1)
        
        self.btnClient2 = QtGui.QPushButton("Client 2", self.verticalLayoutWidget)
        self.btnClient2.setCheckable(True)
        self.verticalLayout.addWidget(self.btnClient2)
        self.clientButtonGroup.addButton(self.btnClient2, 2)
        #   done adding buttons from storage
        
        
        #   add off button
        self.btnClientOff = QtGui.QPushButton("Off", self.verticalLayoutWidget)
        self.btnClientOff.setCheckable(True)
        self.btnClientOff.setChecked(True)
        self.verticalLayout.addWidget(self.btnClientOff)   
        self.clientButtonGroup.addButton(self.btnClientOff, 0)
        
        #   make logical container toggle
        self.clientButtonGroup.setExclusive(True)
        QtCore.QObject.connect(self.clientButtonGroup, QtCore.SIGNAL('buttonPressed(int)'), clientButtonGroupToggled)
     
                
        
        #   done
        self.statusBar().showMessage('Ready')
      
      
      
      
        
@QtCore.pyqtSlot()
def editClients():
    print("editclients")
    

@QtCore.pyqtSlot()
def clientButtonGroupToggled(clientId):
    print("client toggled:{}".format(clientId) )
    
    
    
def main():
    app = QtGui.QApplication(sys.argv)
    form = TimeMachineApp()
    form.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

