#  timemachine.py
#  
#  Copyright 2017 josef ling <jling@swcp.com>
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
from PyQt4 import QtGui, QtCore, uic
import sys
#import layout_main, layout_edit_clients


Ui_MainWindow, QtBaseClass = uic.loadUiType('layout_main.ui')
Ui_dlgEditClients, QtBaseClass = uic.loadUiType('layout_edit_clients.ui')
Ui_dlgReport, QtBaseClass = uic.loadUiType('layout_report.ui')




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
                return cursor.lastrowid
                
        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            raise e
                
        finally:
            if self.dbcon:
                self.dbcon.close()
                
        
        
        
    def removeClient(self, clientName):

        import sqlite3
    
        self.dbcon = None
        
        try:
            self.dbcon = sqlite3.connect('timemachine.db')
            
            with self.dbcon:
                cursor = self.dbcon.cursor()
                # get clientId with clientName
                cursor.execute("SELECT clientId from clients WHERE clientName = ?" , ( [clientName] ) )
                retVal = cursor.fetchone()
                
                if retVal:
                    clientId = retVal[0]
                
                    # remove client records for worked table
                    cursor.execute("DELETE FROM worked WHERE clientID = ?", ([clientId]) )
                    
                    # remove parent record from clients table
                    cursor.execute("DELETE FROM clients WHERE clientID = ?", ([clientId]) )


        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            raise e
                
        finally:
            if self.dbcon:
                self.dbcon.close()
        

        
        
    def updateTime(self, clientId, secondsWorked):
        """
        save time data???
        """

        import sqlite3, datetime
        
        try:
            
            self.dbcon = sqlite3.connect('timemachine.db')
            
            with self.dbcon:
                
                prevWorked = 0.0
                cursor = self.dbcon.cursor()
                cursor.execute('''SELECT secondsWorked from worked WHERE ClientID = ? and dateWorkedInt = ?''' , ( clientId, datetime.datetime.now().strftime("%Y%m%d") ) )
                prevWorked = cursor.fetchone()
                
                if prevWorked is None:
                    cursor.execute('''INSERT INTO worked (clientId, dateWorkedInt, secondsWorked) VALUES (?,?,?)''', ( clientId, datetime.datetime.now().strftime("%Y%m%d"), secondsWorked ) )
                else:
                    cursor.execute('''UPDATE worked SET secondsWorked = ? WHERE ClientID = ? and dateWorkedInt = ?''', ( (prevWorked[0] + secondsWorked), clientId, datetime.datetime.now().strftime("%Y%m%d") ) )
                    
                    
        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            raise e
        
        finally:
            if self.dbcon:
                self.dbcon.close()
                

    def updateClient(self, clientId, clientName):

        import sqlite3
    
        self.dbcon = None
        
        try:
            self.dbcon = sqlite3.connect('timemachine.db')
            
            with self.dbcon:
                cursor = self.dbcon.cursor()
                cursor.execute("UPDATE clients SET clientName = ? WHERE clientId = ?" , ( [clientName, clientId] ) )


        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            raise e
                
        finally:
            if self.dbcon:
                self.dbcon.close()
                
                                        
        
    def getReport(self, dateStr):

        import sqlite3
    
        self.dbcon = None
        
        try:
            self.dbcon = sqlite3.connect('timemachine.db')
            
            with self.dbcon:
                cursor = self.dbcon.cursor()
                # get clientId with clientName
                #cursor.execute("SELECT clients.clientName, (worked.secondsWorked/3600), sum(worked.secondsWorked) from worked INNER JOIN clients ON worked.clientId = clients.clientId WHERE worked.dateWorkedInt = ?" , ( [dateStr] ) )
                cursor.execute("""SELECT clients.clientName, (worked.secondsWorked/3600), 
                                  (SELECT SUM(worked.secondsWorked/3600) FROM worked WHERE dateWorkedInt = ?) AS totalHours 
                                  FROM clients INNER JOIN worked ON clients.clientId = worked.clientId 
                                  WHERE worked.dateWorkedInt = ?""", ( dateStr, dateStr ) )
                
                retVal = cursor.fetchall()
                return retVal


        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            raise e
                
        finally:
            if self.dbcon:
                self.dbcon.close()
        




    
    
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

        #   save
        if( self.activeClientId != 0 ):
            self.storage.updateTime(self.activeClientId, (datetime.datetime.now() - self.datetimeStart).total_seconds() )
        
        #   update timer values
        if(clientId == 0):
            self.datetimeStart = 0
            self.activeClientId = 0               
        else:
            #if( self.activeClientId != 0 ):
            #    self.storage.updateTime(self.activeClientId, (datetime.datetime.now() - self.datetimeStart).total_seconds() )
            self.datetimeStart = datetime.datetime.now()
            self.activeClientId = clientId            
        
        
        
    def close(self):
        """
        Close down timer and save
        """
        
        import datetime
        
        if( self.activeClientId != 0 ):
            self.storage.updateTime(self.activeClientId, (datetime.datetime.now() - self.datetimeStart).total_seconds() )
        self.datetimeStart = 0
        self.activeClientId = 0        
        
        
        
        
        
class DlgEditClients(QtGui.QDialog, Ui_dlgEditClients):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.storage = parent.storage
        
        for clientId, clientName in self.storage.getClients():
            item = QtGui.QListWidgetItem(clientName)
            item.setData(QtCore.Qt.UserRole, clientId)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            self.clientListWidget.addItem(item)
        
        
        self.btnInsert.clicked.connect(self.addItem)
        self.btnRemove.clicked.connect(self.removeItems)       
        self.clientListWidget.itemDoubleClicked[QtGui.QListWidgetItem].connect(self.editItem)
        self.clientListWidget.itemChanged[QtGui.QListWidgetItem].connect(self.saveChangedItem)



    @QtCore.pyqtSlot(QtGui.QListWidgetItem)
    def saveChangedItem(self, currentItem):
        clientId = currentItem.data(QtCore.Qt.UserRole)
        newClientName = currentItem.text()

        self.storage.updateClient( clientId, newClientName )
        self.parentWidget().updateClientButton(clientId, newClientName)

        
        
    @QtCore.pyqtSlot(QtGui.QListWidgetItem)
    def editItem(self, item):
        self.clientListWidget.editItem(item)

        
                
    @QtCore.pyqtSlot()
    def addItem(self):
        if( len(self.inputNewClient.text()) ):
            self.clientListWidget.addItem(self.inputNewClient.text())
            newClientId = self.storage.addClient(self.inputNewClient.text())
            self.parentWidget().addClientButton(newClientId, self.inputNewClient.text())



    @QtCore.pyqtSlot()
    def removeItems(self):
        for item in self.clientListWidget.selectedItems():
            self.clientListWidget.takeItem(self.clientListWidget.row(item))
            self.storage.removeClient(item.text())
            self.parentWidget().removeClientButton(item.text())
                        

        

        
        
class DlgReport(QtGui.QDialog, Ui_dlgReport):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.storage = parent.storage
        self.calendarWidget.clicked[QtCore.QDate].connect(self.generateReport)
        

    @QtCore.pyqtSlot("QDate")
    def generateReport(self, date):
        #QtGui.QMessageBox.information(self,"QCalendarWidget Date Selected",date.toString("yyyyMMdd"))
        workReport = self.storage.getReport(date.toString("yyyyMMdd"))
        
        if len(workReport):
            self.lblReport.setText("")
            #totalHours = 0
            for clientName, hoursWorked, totalHours in workReport:
                self.lblReport.setText(self.lblReport.text() + "{} : {:04.2f} hours\n".format(clientName, hoursWorked))
                
            self.lblReport.setText(self.lblReport.text() + "======================\nTotal : {:04.2f}\n".format(totalHours))
            
        else:
            self.lblReport.setText("No work data for "+date.toString())
              

            

class TimeMachineApp(QtGui.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(TimeMachineApp, self).__init__(parent)
        self.setupUi(self)
        
        #self.actionExit.triggered.connect(QtGui.qApp.quit)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL('triggered()'), QtGui.qApp.quit)
        #self.actionEdit_Clients.triggered.connect(self.editClients)
        QtCore.QObject.connect(self.actionEdit_Clients, QtCore.SIGNAL('triggered()'), self.editClients)
        QtCore.QObject.connect(self.actionReport, QtCore.SIGNAL('triggered()'), self.report)
        
        
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
        """
        Respond to client change
        """
        self.clientTimer.update(clientId)
        if clientId != 0:
            self.statusBar().showMessage('Timer Started')
        else:
            self.statusBar().showMessage('Timer Stopped')


      
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
            clientButtonArray.append( QtGui.QPushButton(self.verticalLayoutWidget) )
            clientButtonArray[clientId].setText( clientName )
            clientButtonArray[clientId].setCheckable(True)
            self.verticalLayout.addWidget(clientButtonArray[clientId])
            self.clientButtonGroup.addButton(clientButtonArray[clientId], clientId)
            

        #   make logical container toggle
        self.clientButtonGroup.setExclusive(True)
        QtCore.QObject.connect(self.clientButtonGroup, QtCore.SIGNAL('buttonPressed(int)'), self.clientButtonGroupToggled)
             



    def addClientButton(self, clientId, clientName):
        """
        Adds new client button to button group layout
        """
        btn = QtGui.QPushButton(self.verticalLayoutWidget)
        btn.setText( clientName )
        btn.setCheckable(True)        
        self.verticalLayout.addWidget(btn)
        self.clientButtonGroup.addButton(btn, clientId)        
        


    def updateClientButton(self, clientId, clientName):
        """
        Update client button text
        """
        btn = self.clientButtonGroup.button(clientId)
        btn.setText(clientName)
        
                
        
    def removeClientButton(self, clientName):
        """
        Remove client button to button group layout
        """        
        for i in reversed(range(self.verticalLayout.count())): 
            widgetToRemove = self.verticalLayout.itemAt( i ).widget()
            if( widgetToRemove.text() == clientName ):
                # remove it from the layout list
                self.verticalLayout.removeWidget( widgetToRemove )
                # remove it from the gui
                widgetToRemove.setParent( None )

        
        
        
    @QtCore.pyqtSlot()
    def editClients(self):
        """
        Launch client list editor
        """
        dlgEditClients = DlgEditClients(self).exec_()



    @QtCore.pyqtSlot()
    def report(self):
        """
        Launch time report
        """
        dlgReport = DlgReport(self).exec_()
        
        
        
    @QtCore.pyqtSlot(QtGui.QMainWindow, QtGui.QCloseEvent)
    def closeEvent(self, event):
        """
        override close event which expects event object
        """
        self.close() 
        
        
    @QtCore.pyqtSlot(QtGui.QMainWindow)
    def close(self):
        """
        QApplication.aboutToQuit() doesn't send event and i haven't figured out how to
        so i resort to chaining closeEvent() -> close() like this for now.
        i could connect to clientTimer.clost() but i left it this way in case i wanted 
        to do something else like confirm user close...
        """
        self.clientTimer.close()   
        
        
        
    
def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    form = TimeMachineApp()
    
    app.aboutToQuit.connect(form.close)
    #QtCore.QObject.connect(app, QtCore.SIGNAL('aboutToQuit(QtGui.QCloseEvent)'), form.closeEvent)
    #app.aboutToQuit.connect[QtGui.QCloseEvent].connect(form.closeEvent)
    
    form.show()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()

