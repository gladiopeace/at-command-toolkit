# Copyright (c) 2010 Shelltoad Computing <info@shelltoad.com>
#
# This file is part of the "AT Command Toolkit" application.
#
# The "AT Command Toolkit" is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

"""
Module containing the serial port connection dialog.
"""

# 3rd party modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import serial

SERIAL_PORT_TIMEOUT = 0.5

class ConnectDlg(QDialog):
    """
    Defines the GUI and behaviour of the serial port connection dialog.
    """
    def __init__(self, parent=None):
        """
        Initialize the serial port connection interface widgets.

        Calls the "populate_options" method at the end of the initializer
        to fill widgets with options.
        """
        QMainWindow.__init__(self, parent)

        # Set the window title
        self.setWindowTitle(self.tr('Connect'))

        # Create "Serial" object
        self.serial_conn = serial.Serial()

        # Create the serial option widgets
        self.port_box = QComboBox()
        self.baudrate_box = QComboBox()
        self.databits_box = QComboBox()
        self.stopbits_box = QComboBox()
        self.parity_box = QComboBox()
        self.rtscts = QCheckBox(self.tr('RTS/CTS'))
        self.xonxoff = QCheckBox(self.tr('Xon/Xoff'))

        # Create buttons
        connect_btn = QPushButton(QIcon(':/images/connect.png'), self.tr('Connect'))
        exit_btn = QPushButton(QIcon(':/images/door_open.png'), self.tr('Exit'))

        # Create "basics" group layout
        refresh_btn = QPushButton(QIcon(':/images/action_refresh.gif'), '')
        self.connect(refresh_btn, SIGNAL('clicked()'), self.populate_port)

        basics_box = QGroupBox(self.tr('Basics:'))
        basics_box_layout = QGridLayout()
        basics_box_layout.addWidget(QLabel(self.tr('Port:')), 0, 0)
        basics_box_layout.addWidget(self.port_box, 0, 1)
        basics_box_layout.addWidget(refresh_btn, 0, 2)
        basics_box_layout.addWidget(QLabel(self.tr('Baudrate:')), 1, 0)
        basics_box_layout.addWidget(self.baudrate_box, 1, 1)
        basics_box.setLayout(basics_box_layout)

        # Create "data format" group layout
        format_box = QGroupBox(self.tr('Data Format:'))
        format_box_layout = QGridLayout()
        format_box_layout.addWidget(QLabel(self.tr('Data Bits:')), 0, 0)
        format_box_layout.addWidget(self.databits_box, 0, 1)
        format_box_layout.addWidget(QLabel(self.tr('Stop Bits:')), 1, 0)
        format_box_layout.addWidget(self.stopbits_box, 1, 1)
        format_box_layout.addWidget(QLabel(self.tr('Parity:')), 2, 0)
        format_box_layout.addWidget(self.parity_box, 2, 1)
        format_box.setLayout(format_box_layout)

        # Create "flow control" group layout
        flowcontrol_box = QGroupBox(self.tr('Flow Control:'))
        flowcontrol_box_layout = QHBoxLayout()
        flowcontrol_box_layout.addWidget(self.rtscts)
        flowcontrol_box_layout.addWidget(self.xonxoff)
        flowcontrol_box.setLayout(flowcontrol_box_layout)

        # Create buttons group layout
        buttons_box = QHBoxLayout()
        buttons_box.addWidget(connect_btn)
        buttons_box.addWidget(exit_btn)

        # Create main layout
        container = QVBoxLayout()
        container.addWidget(basics_box)
        container.addWidget(format_box)
        container.addWidget(flowcontrol_box)
        container.addLayout(buttons_box)
        self.setLayout(container)

        # Connect widgets
        self.connect(connect_btn, SIGNAL('clicked()'), self.try_connect)
        self.connect(exit_btn, SIGNAL('clicked()'), self.reject)

        # Populate the serial options
        self.populate_options()

    def populate_port(self):
        self.port_box.clear()

        # Populate the port number combo box (attempt to connect to all possible ports)
        for i in range(256):
            try:
                s = serial.Serial(i)
            except serial.SerialException:
                pass
            else:
                self.port_box.addItem(s.portstr)
                s.close()

    def populate_options(self):
        """
        Populates the serial port setting widgets (Available ports, baud
        rates, etc) with the choices available from the Serial object.
        """
        self.populate_port()

        # Populate the baudrate combo box
        for index, baudrate in enumerate(self.serial_conn.BAUDRATES):
            self.baudrate_box.addItem(str(baudrate))
            if self.serial_conn.baudrate == baudrate:
                self.baudrate_box.setCurrentIndex(index)

        # Populate the "data bits" combo box
        for index, bytesize in enumerate(self.serial_conn.BYTESIZES):
            self.databits_box.addItem(str(bytesize))
            if self.serial_conn.bytesize == bytesize:
                self.databits_box.setCurrentIndex(index)

        # Populate the "stop bits" combo box
        for index, stopbits in enumerate(self.serial_conn.STOPBITS):
            self.stopbits_box.addItem(str(stopbits))
            if self.serial_conn.stopbits == stopbits:
                self.stopbits_box.setCurrentIndex(index)

        # Populate the "parity" combo box
        for index, parity in enumerate(self.serial_conn.PARITIES):
            self.parity_box.addItem(str(serial.PARITY_NAMES[parity]))
            if self.serial_conn.parity == parity:
                self.parity_box.setCurrentIndex(index)

        # Populate the "flow control" options
        self.rtscts.setChecked(self.serial_conn.rtscts)
        self.xonxoff.setChecked(self.serial_conn.xonxoff)

    def try_connect(self):
        """
        Reads the serial port settings entered by the user on the GUI and
        attempts to connect to the serial port. If successful then the
        connection dialog will be closed, if not then the error message from
        the serial object will be displayed.

        Once the serial port connection has been made and the connection dialog
        has closed the connected serial object can be retrieved by accessing
        the instance attribute "serial_conn".
        """

        # Set the serial object settings
        self.serial_conn.timeout = SERIAL_PORT_TIMEOUT
        self.serial_conn.port = str(self.port_box.currentText())
        self.serial_conn.baudrate = self.serial_conn.BAUDRATES[self.baudrate_box.currentIndex()]
        self.serial_conn.bytesize = self.serial_conn.BYTESIZES[self.databits_box.currentIndex()]
        self.serial_conn.stopbits = self.serial_conn.STOPBITS[self.stopbits_box.currentIndex()]
        self.serial_conn.parity = self.serial_conn.PARITIES[self.parity_box.currentIndex()]
        self.serial_conn.rtscts = self.rtscts.isChecked()
        self.serial_conn.xonxoff = self.xonxoff.isChecked()

        # Try to open the serial connection
        try:
            self.serial_conn.open()
        except serial.SerialException, e:
            QMessageBox.critical(self, self.tr('Serial Port Error'), self.tr(str(e).capitalize()), QMessageBox.Ok)
        else:
            self.accept()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    form = ConnectDlg()
    if form.exec_():
        serial_conn = form.serial_conn
        print serial_conn
    sys.exit(0)
