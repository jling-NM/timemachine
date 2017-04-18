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
import layout, layout_edit_clients





class Storage():
    """
    This will be the data interface
    """
    
    def __init__(self):
    
        import sqlite3
    
        self.dbcon = None
        
        try:
            self.dbcon = sqlite3.connect('timemachine.db')
            
            with self.dbcon:
                cursor = self.dbcon.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS clients(clientId INTEGER NOT NULL PRIMARY KEY, clientName)''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS worked(clientId integer NOT NULL, dateWorkedInt text, secondsWorked float, FOREIGN KEY (clientId) REFERENCES clients(clientId) )''')

                
        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            raise e
                
        finally:
            if self.dbcon:
                self.dbcon.close()
                
                

        
        
    def getClients(self):
        #   return dictionary of client names; client ids
        
        import sqlite3
        self.dbcon = None
        self.clients = None
        
        try:
            self.dbcon = sqlite3.connect('timemachine.db')
            
            with self.dbcon:
                cursor = self.dbcon.cursor()
                self.dbcon.row_factory = sqlite3.Row
                cursor.execute('''SELECT * from clients''')
                self.clients = cursor.fetchall()
                
        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            raise e
                
        finally:
            if self.dbcon:
                self.dbcon.close()
                        
        return self.clients
        
        
        
    def addClient(self, name):
        #   add
        #   return id?
        import sqlite3
    
        self.dbcon = None
        
        try:
            self.dbcon = sqlite3.connect('timemachine.db')
            
            with self.dbcon:
                cursor = self.dbcon.cursor()
                cursor.execute("INSERT INTO clients (clientName) VALUES (?)", ([name]) )
                
        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            raise e
                
        finally:
            if self.dbcon:
                self.dbcon.close()
                
        
        
        
    def removeClient(self):
        pass
        
        
        
    def updateTime(self, clientId, secondsWorked):
        """
        save time data???
        """
        print("Update time for client:{} with {} minutes".format(clientId, secondsWorked/60))
        
        import sqlite3, datetime
        
        try:
            
            self.dbcon = sqlite3.connect('timemachine.db')
            
            with self.dbcon:
                
                prevWorked = 0.0
                #db.row_factory = sqlite3.Row
                cursor = self.dbcon.cursor()
                cursor.execute('''SELECT secondsWorked from worked WHERE ClientID = ? and dateWorkedInt = ?''' , ( clientId, datetime.datetime.now().strftime("%Y%m%d") ) )
                prevWorked = cursor.fetchone()
                
                if prevWorked is None:
                    cursor.execute('''INSERT INTO worked (clientId, dateWorkedInt, secondsWorked) VALUES (?,?,?)''', ( clientId, datetime.datetime.now().strftime("%Y%m%d"), secondsWorked ) )
                else:
                    print(prevWorked[0] + secondsWorked)
                    cursor.execute('''UPDATE worked SET secondsWorked = ? WHERE ClientID = ? and dateWorkedInt = ?''', ( (prevWorked[0] + secondsWorked), clientId, datetime.datetime.now().strftime("%Y%m%d") ) )
                    
                    
        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            raise e
        
        

    
    
class ClientTimer():
    
    """
    This handles timing
    """
    
    def __init__(self, storage):
        
        self.storage = storage
        self.activeClientId = 0   # who we are timing
        self.datetimeStart  = 0.0 # when we started

        
        
    def update(self, clientId):
        
        """
        Update Timer
        
        if clientId is 0 the timer should go off on active client
            b) storage.write(activeClientId, minutes(now - start time))
            c) start time = 0
        else 
            if activeClientId = 0
                first client and need to start timer
                a) start time = now
                b) activeClientId = clientId
                c) storage.write
                
            else need to switch clients
                a) storage.write(activeClientId, minutes(now - start time)
                b) start time = now
                c) activeClientId = clientId

        """
        import datetime
        
        if(clientId == 0):
            if( self.activeClientId != 0 ):
                self.storage.updateTime(self.activeClientId, (datetime.datetime.now() - self.datetimeStart).total_seconds() )
            self.datetimeStart = 0
            self.activeClientId = 0               
        else:
            if( self.activeClientId == 0 ):
                # some crash protection storage started???
                #self.storage.updateTime(self.activeClientId, 7.0)
                print("start timing for client {}".format(clientId))
            else:
                self.storage.updateTime(self.activeClientId, (datetime.datetime.now() - self.datetimeStart).total_seconds() )
        
            self.datetimeStart = datetime.datetime.now()
            self.activeClientId = clientId            
        
        
        
        
class DlgEditClients(QtGui.QDialog, layout_edit_clients.Ui_dlgEditClients):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.storage = None
        
        
    @QtCore.pyqtSlot()
    def addItem(self):
        if( len(self.inputNewClient.text()) ):
            self.clientListWidget.addItem(self.inputNewClient.text())
            self.storage.addClient(self.inputNewClient.text())


    @QtCore.pyqtSlot()
    def removeItems(self):
        for item in self.clientListWidget.selectedItems():
            self.clientListWidget.takeItem(self.clientListWidget.row(item))
            #self.storage.removeClient(self.inputNewClient.text())
                        
    def setStorage(self, storage):
        self.storage = storage
        
        
        

class TimeMachineApp(QtGui.QMainWindow, layout.Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(TimeMachineApp, self).__init__(parent)
        self.setupUi(self)
        
        #self.actionExit.triggered.connect(QtGui.qApp.quit)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL('triggered()'), QtGui.qApp.quit)
        #self.actionEdit_Clients.triggered.connect(self.editClients)
        QtCore.QObject.connect(self.actionEdit_Clients, QtCore.SIGNAL('triggered()'), self.editClients)
        
        try:
            #   init storage
            self.storage = Storage()
            
            #   add client buttons
            self.setupClientButtons(self.storage)
            
            #   init timer        
            self.clientTimer = ClientTimer(self.storage)
            
            #   done
            self.statusBar().showMessage('Ready')
          
        except Exception as e:
            print(e)
            sys.exit(1)
            
            
      
    @QtCore.pyqtSlot(int)
    def clientButtonGroupToggled(self, clientId):
        print("client toggled:{}".format(clientId) )
        self.clientTimer.update(clientId)



      
    def setupClientButtons(self, storage):
        """
        Client buttons must be dynamic
        This is a function that clears the client buttons if needed
        then adds client buttons to the form
        """

        
        #####   add client buttons from storage list #####

        #   init logical container for client buttons; not sure if this is worth the trouble except for id feature
        self.clientButtonGroup = QtGui.QButtonGroup(self)

        #   add buttons to layout and logical contaner
        clientButtonArray = []
        #   add off button at zero so that clientId and index can be the same
        #   and because Off button has some different parameters
        clientButtonArray.append( QtGui.QPushButton(self.verticalLayoutWidget) )
        clientButtonArray[0].setText("Off")
        clientButtonArray[0].setCheckable(True)
        clientButtonArray[0].setChecked(True)
        self.verticalLayout.addWidget(clientButtonArray[0])   
        self.clientButtonGroup.addButton(clientButtonArray[0], 0)
                
        for clientId, clientName in storage.getClients():
            #print("{}:{}".format(clientId, clientName))
            clientButtonArray.append( QtGui.QPushButton(self.verticalLayoutWidget) )
            clientButtonArray[clientId].setText( clientName )
            clientButtonArray[clientId].setCheckable(True)
            self.verticalLayout.addWidget(clientButtonArray[clientId])
            self.clientButtonGroup.addButton(clientButtonArray[clientId], clientId)
            

        #   make logical container toggle
        self.clientButtonGroup.setExclusive(True)
        QtCore.QObject.connect(self.clientButtonGroup, QtCore.SIGNAL('buttonPressed(int)'), self.clientButtonGroupToggled)
             


        
    @QtCore.pyqtSlot()
    def editClients(self):
 
        dlgEditClients = DlgEditClients();
        dlgEditClients.setStorage(self.storage)
        for clientId, clientName in self.storage.getClients():
            dlgEditClients.clientListWidget.addItem(clientName)
        
        
        dlgEditClients.btnInsert.clicked.connect(dlgEditClients.addItem)
        dlgEditClients.btnRemove.clicked.connect(dlgEditClients.removeItems)
        
        dlgEditClients.exec_()





        
        
    
def main():
    app = QtGui.QApplication(sys.argv)
    form = TimeMachineApp()
    form.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

