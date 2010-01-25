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
Module containing the Terminal class/widget for serial port communication.
"""

# 3rd party modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import serial

class TerminalWidget(QWidget):
    """
    The terminal widget handles sending commands to the serial port.
    It also handles receiving and displaying data from the serial port.

    The purpose behind the class is to abstract all interaction with the
    serial port away from the rest of the application so that commands
    can be constructed by other parts of the application then sent to
    the serial port through this class/widget, without having to deal
    with serial port communication in any way.

    The widget essentially provides a basic terminal interface, but also
    provides the ability for other modules to send commands to the serial
    port via the "send_command" method.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Create the terminal widgets
        self.command_txt = QLineEdit()
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        # Create the command buttons
        self.send_command_btn = QPushButton(QIcon(':/images/bullet_go.png'), '')
        self.clear_log_btn = QPushButton(QIcon(':/images/page_white.png'), '')

        # Create the form layout
        button_box = QHBoxLayout()
        button_box.addWidget(self.command_txt)
        button_box.addWidget(self.send_command_btn)
        button_box.addWidget(self.clear_log_btn)

        container = QVBoxLayout()
        container.addLayout(button_box)
        container.addWidget(self.log)

        self.setLayout(container)

        # Create a timer to read from the serial port
        self.read_timer = QTimer(self)

        # Connect the widgets
        self.connect(self.command_txt, SIGNAL('returnPressed()'), self.send_line_command)
        self.connect(self.send_command_btn, SIGNAL('clicked()'), self.send_line_command)
        self.connect(self.clear_log_btn, SIGNAL('clicked()'), self.log.clear)
        self.connect(self.log, SIGNAL('textChanged()'), self.scroll_log)
        self.connect(self.read_timer, SIGNAL('timeout()'), self.read_serial_data)

    def connect_com_port(self):

        # Start the timer that reads the COM port
        self.read_timer.start(100)

        # Enable the GUI widgets
        self.command_txt.setEnabled(True)
        self.send_command_btn.setEnabled(True)
        self.clear_log_btn.setEnabled(True)
        self.log.setEnabled(True)

    def disconnect_com_port(self):

        # Stop the timer that reads the COM port
        self.read_timer.stop()

        # Close the COM port
        self.serial_conn.close()

        # Disable the GUI widgets
        self.command_txt.setDisabled(True)
        self.send_command_btn.setDisabled(True)
        self.clear_log_btn.setDisabled(True)
        self.log.setDisabled(True)

    def send_command(self, command):
        """
        Send a command to the serial port.

        The command is expected to be an AT command string. Leading and
        trailing white space is stripped from the command string.
        """
        command = str(command).strip()

        try:

            # Add a command marker in the terminal & send the command
            self.log.append('> ')
            self.serial_conn.write(command + '\r\n')

        except serial.SerialException:
            QMessageBox.critical(self,
                                 self.tr('Serial Port Error'),
                                 self.tr('There was a communication error with the serial port.'),
                                 QMessageBox.Ok)

    def set_font(self, font):
        """
        Set the font of the terminal.

        Expects a QFont object as the parameter.
        """
        self.log.setFont(font)
        self.command_txt.setFont(font)

    def send_line_command(self):
        """
        Send a command from the "command_txt" line edit widget.
        """
        
        # Get the command text (cast to string and strip whitespace)
        command = str(self.command_txt.text()).strip()

        # Empty the text box and set focus
        self.command_txt.setText('')
        self.command_txt.setFocus()

        # Send the entered text as a command
        if command:
            self.send_command(command)

    def read_serial_data(self):
        """
        Read any buffered data from the serial port.

        This is invoked at regular intervals by the "read_timer"
        timer that is created in the class initializer.
        """
        try:
            buffer_size = self.serial_conn.inWaiting()
            if buffer_size:
                current_text = str(self.log.toPlainText())
                new_text = self.serial_conn.read(buffer_size)
                new_text = new_text.replace('\r\n', '\n')
                new_text = new_text.replace('\r', '')
                self.log.setText(current_text + new_text)

        except serial.SerialException:

            self.emit(SIGNAL('connectionError()'))
            QMessageBox.critical(self,
                                 self.tr('Serial Port Error'),
                                 self.tr('There was a communication error with the serial port.'),
                                 QMessageBox.Ok)

    def scroll_log(self):
        """
        Moves the terminal log text cursor to the bottom of the text box.

        This is invoked every time the text changes in the terminal log
        so that the most current text is always shown.
        """
        cursor = self.log.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log.setTextCursor(cursor)
