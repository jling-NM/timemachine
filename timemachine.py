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
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import layout.main, layout.edit_clients, layout.report
from inspect import getsourcefile
import os.path

### if you want to load for ui files but i haven't figured out how to package and call
### those when you aren't in local directory
#Ui_MainWindow, QtBaseClass = uic.loadUiType('layout_main.ui')
#Ui_dlgEditClients, QtBaseClass = uic.loadUiType('layout_edit_clients.ui')
#Ui_dlgReport, QtBaseClass = uic.loadUiType('layout_report.ui')


class NotesTextEdit(QtWidgets.QPlainTextEdit):
    """
    Subclass text field to use focus events
    """
    lostFocus = QtCore.pyqtSignal('QString')
    
    def focusOutEvent(self, event):
        self.lostFocus.emit(self.toPlainText())
        super(NotesTextEdit, self).focusOutEvent(event)
       
    
class Storage:
    """
    Data interface
    """

    class DbConCursor(object):

        """
        Context manager for database connection cursor
        """
        def __init__(self):

            # get the path of the script that launched the application
            self.app_path = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))

            import sqlite3
            try:
                self.dbcon = sqlite3.connect(os.path.join(self.app_path, 'timemachine.db'))
            except sqlite3.Error as e:
                raise e

        def __enter__(self):
            return self.dbcon.cursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.dbcon:
                self.dbcon.commit()
                self.dbcon.close()



    def __init__(self):
        self.create()



    def create(self):
        """
        Create db
        """
        with self.DbConCursor() as dbc:
            dbc.execute('''CREATE TABLE IF NOT EXISTS 
                              clients(clientId INTEGER NOT NULL PRIMARY KEY, clientName)''')
            dbc.execute('''CREATE TABLE IF NOT EXISTS 
                              worked(clientId integer NOT NULL, dateWorkedInt text, secondsWorked float, 
                              FOREIGN KEY (clientId) REFERENCES clients(clientId) )''')
            dbc.execute('''CREATE TABLE IF NOT EXISTS 
                              notes(dateNote text, note)''')


    def get_clients(self):
        """
        :return: dictionary of client names; client ids
        """
        import sqlite3

        try:
            with self.DbConCursor() as dbc:
                dbc.row_factory = sqlite3.Row
                dbc.execute('SELECT * from clients')
                clients = dbc.fetchall()
                return clients
        except Exception as e:
            print("Storage error: {}".format(e))


    def add_client(self, client_name):
        """
        Add client
        :param client_name: 
        :return: new client_id
        """
        with self.DbConCursor() as dbc:
            dbc.execute("INSERT INTO clients (clientName) VALUES (?)", ([client_name]))
            new_client_id = dbc.lastrowid

        return new_client_id


    def remove_client(self, client_name):
        """
        Remove client
        :param client_name: 
        :return: nothing
        """
        with self.DbConCursor() as dbc:
            # get clientId with clientName
            dbc.execute("SELECT clientId from clients WHERE clientName = ?", ([client_name]))
            ret_val = dbc.fetchone()

            if ret_val:
                client_id = ret_val[0]
                # remove client records for worked table
                dbc.execute("DELETE FROM worked WHERE clientID = ?", ([client_id]))
                # remove parent record from clients table
                dbc.execute("DELETE FROM clients WHERE clientID = ?", ([client_id]))


    def update_time(self, client_id, seconds_worked):
        """
        Update time worked for client
        :param client_id: 
        :param seconds_worked: 
        :return: nothing
        """
        import datetime
        with self.DbConCursor() as dbc:
            dbc.execute('''SELECT secondsWorked from worked 
                              WHERE ClientID = ? and dateWorkedInt = ?''',
                           (client_id, datetime.datetime.now().strftime("%Y%m%d")))
            prev_worked = dbc.fetchone()

            if prev_worked is None:
                dbc.execute('''INSERT INTO worked (clientId, dateWorkedInt, secondsWorked) 
                               VALUES (?,?,?)''',
                               (client_id, datetime.datetime.now().strftime("%Y%m%d"), seconds_worked))
            else:
                dbc.execute('''UPDATE worked SET secondsWorked = ? WHERE ClientID = ? and dateWorkedInt = ?''', (
                    (prev_worked[0] + seconds_worked), client_id, datetime.datetime.now().strftime("%Y%m%d")))


    def update_client(self, client_id, client_name):
        """
        Update client name
        :param client_id: 
        :param client_name: 
        :return: void
        """
        with self.DbConCursor() as dbc:
            dbc.execute("UPDATE clients SET clientName = ? WHERE clientId = ?", ([client_name, client_id]))


    def get_note(self, date_str):
        """
        Retrieve any notes for the date
        """
        notes_txt = ''
        
        with self.DbConCursor() as dbc:
            dbc.execute("SELECT note FROM notes WHERE dateNote == ?", ([date_str]))
            ret_val = dbc.fetchone()
            if ret_val:
                notes_txt = ret_val[0]
            
        return notes_txt
        
        
    def update_note(self, notes_txt):
        """
        Update day notes
        :param notes_txt: 
        :return: void
        """
        import datetime
        current_date_str = datetime.datetime.now().strftime("%Y%m%d")

        with self.DbConCursor() as dbc:
            dbc.execute("SELECT dateNote FROM notes WHERE dateNote == ?", ([current_date_str]))
            note_exists = dbc.fetchone()
            
            if note_exists:
                if len(notes_txt):
                    dbc.execute("UPDATE notes SET note = ? WHERE dateNote = ?", (notes_txt, current_date_str))
                else:
                    dbc.execute("DELETE FROM notes WHERE dateNote = ?", ([current_date_str]))                    
            else:
                dbc.execute("INSERT INTO notes (dateNote, note) VALUES (?,?)", (current_date_str, notes_txt))

    
    
    
    def get_report(self, date_str):
        """
        Get worked data for date string
        :param date_str: 
        :return: list of records
        """
        with self.DbConCursor() as dbc:
            # get clientId with clientName
            dbc.execute("""SELECT clients.clientName, (worked.secondsWorked/3600), 
                              (SELECT SUM(worked.secondsWorked/3600) FROM worked WHERE dateWorkedInt = ?) AS totalHours 
                              FROM clients INNER JOIN worked ON clients.clientId = worked.clientId 
                              WHERE worked.dateWorkedInt = ?""", (date_str, date_str))

            ret_val = dbc.fetchall()
            return ret_val


class ClientTimer:
    """
    Timer for hours worked
    """
    def __init__(self, storage):

        self.storage = storage
        self.activeClientId = 0  # who we are timing
        self.datetimeStart = 0.0  # when we started

    def update(self, client_id):
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
        if self.activeClientId != 0:
            self.storage.update_time(self.activeClientId,
                                     (datetime.datetime.now() - self.datetimeStart).total_seconds())

        # update timer values
        if client_id == 0:
            self.datetimeStart = 0
            self.activeClientId = 0
        else:
            self.datetimeStart = datetime.datetime.now()
            self.activeClientId = client_id

    def close(self):
        """
        Close down timer and save
        """

        import datetime

        if self.activeClientId != 0:
            self.storage.update_time(self.activeClientId,
                                     (datetime.datetime.now() - self.datetimeStart).total_seconds())
        self.datetimeStart = 0
        self.activeClientId = 0


class DlgEditClients(QtWidgets.QDialog, layout.edit_clients.Ui_dlgEditClients):
    """
    Dialog for editing clients
    """
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.storage = parent.storage

        for clientId, clientName in self.storage.get_clients():
            item = QtWidgets.QListWidgetItem(clientName)
            item.setData(QtCore.Qt.UserRole, clientId)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            self.clientListWidget.addItem(item)

        self.btnInsert.clicked.connect(self.add_item)
        self.btnRemove.clicked.connect(self.remove_items)
        self.clientListWidget.itemDoubleClicked[QtWidgets.QListWidgetItem].connect(self.edit_item)
        self.clientListWidget.itemChanged[QtWidgets.QListWidgetItem].connect(self.save_changed_item)

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def save_changed_item(self, current_item):
        """
        Save inline edit of client name
        :param current_item: 
        :return: 
        """
        client_id = current_item.data(QtCore.Qt.UserRole)
        new_client_name = current_item.text()

        self.storage.update_client(client_id, new_client_name)
        self.parentWidget().update_client_button(client_id, new_client_name)

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def edit_item(self, item):
        """
        Bring up inline editor in listwidget
        :param item: 
        :return: 
        """
        self.clientListWidget.editItem(item)

    @QtCore.pyqtSlot()
    def add_item(self):
        """
        Add new client
        :return: 
        """
        if len(self.inputNewClient.text()):
            self.clientListWidget.addItem(self.inputNewClient.text())
            new_client_id = self.storage.add_client(self.inputNewClient.text())
            self.parentWidget().add_client_button(new_client_id, self.inputNewClient.text())

    @QtCore.pyqtSlot()
    def remove_items(self):
        """
        Remove selected clients
        :return: 
        """
        for item in self.clientListWidget.selectedItems():
            self.clientListWidget.takeItem(self.clientListWidget.row(item))
            self.storage.remove_client(item.text())
            self.parentWidget().remove_client_button(item.text())



class DlgReport(QtWidgets.QDialog, layout.report.Ui_dlgReport):
    """
    Dialog for viewing work report
    """
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.storage = parent.storage
        # set handler when date is clicked
        self.calendarWidget.clicked[QtCore.QDate].connect(self.generate_report)
        # on init, select current date and display that as default
        self.generate_report(QtCore.QDate.currentDate())


    @QtCore.pyqtSlot("QDate")
    def generate_report(self, date):
        """
        Display work for date
        :param date: 
        :return: 
        """
        # QtWidgets.QMessageBox.information(self,"QCalendarWidget Date Selected",date.toString("yyyyMMdd"))
        work_report = self.storage.get_report(date.toString("yyyyMMdd"))

        if len(work_report):
            self.lblReport.setText("")
            for clientName, hoursWorked, totalHours in work_report:
                self.lblReport.setText(self.lblReport.text() + "{} : {:04.2f} hours\n".format(clientName, hoursWorked))

            self.lblReport.setText(
                self.lblReport.text() + "======================\nTotal : {:04.2f}\n".format(totalHours))

        else:
            self.lblReport.setText("No work data for " + date.toString())


        # Any notes?
        notes = self.storage.get_note(date.toString("yyyyMMdd"))
        if len(notes):
            self.lblReport.setText(self.lblReport.text() + "\n====================== Notes:\n{}".format(notes))


class TimeMachineApp(QtWidgets.QMainWindow, layout.main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(TimeMachineApp, self).__init__(parent)
        self.setupUi(self)
        self.actionExit.triggered.connect(QtWidgets.qApp.quit)
        self.actionEdit_Clients.triggered.connect(self.edit_clients)
        self.actionReport.triggered.connect(self.report)


        # init storage
        self.storage = Storage()

        # runtime layout
        self.runtime_layout()

        # init timer
        self.clientTimer = ClientTimer(self.storage)
        
        # session persistence
        self.settings = QtCore.QSettings()
        
        # done
        self.statusBar().showMessage('Ready')




    @QtCore.pyqtSlot(int)
    def client_button_group_toggled(self, client_id):
        """
        Respond to client button change
        """
        self.clientTimer.update(client_id)
        if client_id != 0:
            self.statusBar().showMessage('Timer Started')
        else:
            self.statusBar().showMessage('Timer Stopped')

 
       
    def runtime_layout(self):
        """
        Client buttons must be dynamic
        This is a function that clears the client buttons if needed
        then adds client buttons to the form
        """

        # ####   add client buttons from storage list #####

        #   init logical container for client buttons; not sure if this is worth the trouble except for id feature
        self.clientButtonGroup = QtWidgets.QButtonGroup(self)
        
        self.add_client_button(0, 'Off')
        # add client buttons for each client
        for clientId, clientName in self.storage.get_clients():
            self.add_client_button(clientId, clientName)
        
        # make logical container toggle
        self.clientButtonGroup.setExclusive(True)
        self.clientButtonGroup.buttonPressed[int].connect(self.client_button_group_toggled)
        
        # notes editor
        self.notesVerticalLayout.addWidget(QtWidgets.QLabel("Day Notes:"))
        notesTextEdit = NotesTextEdit()
        notesTextEdit.lostFocus.connect(self.save_notes)
        # insert notes from storage
        notes = self.storage.get_note(QtCore.QDate.currentDate().toString("yyyyMMdd"))
        if notes:
            notesTextEdit.setPlainText(notes)
        self.notesVerticalLayout.addWidget(notesTextEdit)


        
        
    def add_client_button(self, client_id, client_name):
        """
        Adds new client button to button group layout
        :param client_id: 
        :param client_name: 
        :return: 
        """
        btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        btn.setText(client_name)
        btn.setCheckable(True)
        if client_id == 0:
            btn.setChecked(True)

        self.clientBtnVerticalLayout.addWidget(btn)
        self.clientButtonGroup.addButton(btn, client_id)


    def update_client_button(self, client_id, client_name):
        """
        Update client button text
        :param client_id: 
        :param client_name: 
        :return: 
        """
        btn = self.clientButtonGroup.button(client_id)
        btn.setText(client_name)


    def remove_client_button(self, client_name):
        """
        Remove client button to button group layout
        :param client_name: 
        :return: 
        """
        for i in reversed(range(self.clientBtnVerticalLayout.count())):
            widget_to_remove = self.clientBtnVerticalLayout.itemAt(i).widget()
            if widget_to_remove.text() == client_name:
                # remove it from the layout list
                self.clientBtnVerticalLayout.removeWidget(widget_to_remove)
                # remove it from the gui
                widget_to_remove.setParent(None)




    @QtCore.pyqtSlot('QString')
    def save_notes(self, notes_txt):
        """
        Save notes to storage
        """
        self.storage.update_note(notes_txt)
        
                        
    @QtCore.pyqtSlot()
    def edit_clients(self):
        """
        Launch client list editor
        :return: 
        """
        DlgEditClients(self).exec_()

    @QtCore.pyqtSlot()
    def report(self):
        """
        Launch time report
        :return: 
        """
        DlgReport(self).exec_()

    @QtCore.pyqtSlot(QtWidgets.QMainWindow, QtGui.QCloseEvent)
    def closeEvent(self, event):
        """
        override close event
        :param event: 
        :return: 
        """
        self.close()

    @QtCore.pyqtSlot()
    def close(self):
        """
        QApplication.aboutToQuit() doesn't send event and i haven't figured out how to
        so i resort to chaining closeEvent() -> close() like this for now.
        i could connect to clientTimer.clost() but i left it this way in case i wanted 
        to do something else like confirm user close...        
        :return: 
        """
        self.clientTimer.close()


    def show_first_time(self):
        """
        The first time we identify db has no clients
        """
        if self.settings.value('first_time_run', True, type=bool):
            
            # no clients in db
            if not len(self.storage.get_clients()):
                
                msg_button_reply = QtWidgets.QMessageBox.question(
                                    self, 
                                    'Time Machine', 
                                    'Time Machine has no clients yet.\nAdd Clients now?', 
                                    QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes, 
                                    QtWidgets.QMessageBox.Yes )
                                    
                if msg_button_reply == QtWidgets.QMessageBox.Yes:
                    self.edit_clients()
            
           
        # update settings; no longer the first time
        self.settings.setValue('first_time_run', False)
        # this writes to native storage
        del self.settings
                
                
def main():

    app = QtWidgets.QApplication(sys.argv)
    # app style
    app.setStyle("plastique")
    # app setting in general but specifically so that call to QSettings() uses meaningful path for settings
    app.setOrganizationName("jling_projects")
    app.setApplicationName("Time Machine")
    
    appWin = TimeMachineApp()
    # connect main window close and app close events
    app.aboutToQuit.connect(appWin.close)
    
    try:
        appWin.show()
        appWin.show_first_time()
        # disable resizing or stretching of main window
        appWin.setFixedSize(appWin.size());
        
    except Exception as e:
        QtWidgets.QMessageBox.information("QCalendarWidget Date Selected", e)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

