#!/bin/tcsh
pyuic5 -o ./layout/main.py ./layout/main.ui
pyuic5 -o ./layout/edit_clients.py ./layout/edit_clients.ui
pyuic5 -o ./layout/report.py ./layout/report.ui

pyrcc5 -o timemachine_rc.py timemachine.qrc
