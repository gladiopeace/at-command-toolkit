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
Module containing the "Call Control" commands class/widget.
"""

# 3rd party modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CallControlWidget(QWidget):
    """
    Defines the GUI and behaviour of the "Call Control" commands widget.
    """
    TITLE = 'Call Control'

    def __init__(self, terminal, parent=None):
        """
        Initialize the interface widgets.
        """
        QWidget.__init__(self, parent)

        # Store the terminal object for later reference
        self.terminal = terminal

        # Create the "make call" widgets and layout
        self.call_string_txt = QLineEdit()
        self.voice_call_rad = QRadioButton(self.tr('Voice'))
        self.voice_call_rad.setChecked(True)
        self.data_call_rad = QRadioButton(self.tr('Data'))
        make_call_btn = QPushButton(self.tr('Make Call'))

        call_box = QGroupBox(self.tr('Make Call:'))
        call_box_layout = QGridLayout()
        call_box_layout.addWidget(self.call_string_txt, 0, 0, 1, 2)
        call_box_layout.addWidget(self.voice_call_rad, 1, 0)
        call_box_layout.addWidget(self.data_call_rad, 1, 1)
        call_box_layout.addWidget(make_call_btn, 2, 0, 1, 2)
        call_box.setLayout(call_box_layout)

        # Create other miscellaneous buttons
        answer_call_btn = QPushButton(self.tr('Answer Incoming Call'))
        end_call_btn = QPushButton(self.tr('Terminate Active Call'))

        # Create the button groupbox & layout
        commands_box = QGroupBox(self.tr('Call Commands:'))
        commands_box_layout = QVBoxLayout()
        commands_box_layout.addWidget(answer_call_btn)
        commands_box_layout.addWidget(end_call_btn)
        commands_box.setLayout(commands_box_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(call_box)
        main_layout.addWidget(commands_box)
        main_layout.addStretch()

        # Create main layout
        container = QHBoxLayout()
        container.addStretch()
        container.addLayout(main_layout)
        container.addStretch()
        self.setLayout(container)

        # Connect widgets
        self.connect(make_call_btn, SIGNAL('clicked()'), self.make_call)
        self.connect(answer_call_btn, SIGNAL('clicked()'), lambda: terminal.send_command('ATA'))
        self.connect(end_call_btn, SIGNAL('clicked()'), lambda: terminal.send_command('ATH'))

    def make_call(self):
        """
        Sends the AT command to initiate a voice or data call.
        """
        dial_string = str(self.call_string_txt.text()).strip()
        if len(dial_string) == 0:
            QMessageBox.critical(self, self.tr('Error'), self.tr('Please enter a string to dial'), QMessageBox.Ok)
            return

        command_string = 'ATD%s;' if self.voice_call_rad.isChecked() else 'ATD%s'
        self.terminal.send_command(command_string % dial_string)

if __name__ == '__main__':
    from standalone import run_standalone
    run_standalone(CallControlWidget)
