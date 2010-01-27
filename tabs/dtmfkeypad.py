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
Module containing the "DTMF Keypad" commands class/widget.
"""

# 3rd party modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DtmfKeypadWidget(QWidget):
    """
    Defines the GUI and behaviour of the "DTMF Keypad" commands widget.
    """
    TITLE = 'DTMF Keypad'

    def __init__(self, terminal, parent=None):
        """
        Initialize the interface widgets.
        """
        QWidget.__init__(self, parent)

        # Store the terminal object for later reference
        self.terminal = terminal

        # Create "dial pad" buttons
        btn_0 = QPushButton(self.tr('0'))
        btn_1 = QPushButton(self.tr('1'))
        btn_2 = QPushButton(self.tr('2'))
        btn_3 = QPushButton(self.tr('3'))
        btn_4 = QPushButton(self.tr('4'))
        btn_5 = QPushButton(self.tr('5'))
        btn_6 = QPushButton(self.tr('6'))
        btn_7 = QPushButton(self.tr('7'))
        btn_8 = QPushButton(self.tr('8'))
        btn_9 = QPushButton(self.tr('9'))
        btn_a = QPushButton(self.tr('A'))
        btn_b = QPushButton(self.tr('B'))
        btn_c = QPushButton(self.tr('C'))
        btn_d = QPushButton(self.tr('D'))
        btn_str = QPushButton(self.tr('*'))
        btn_hsh = QPushButton(self.tr('#'))

        # Set the width & font of the buttons
        btn_list = (btn_0, btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7,
                    btn_8, btn_9, btn_a, btn_b, btn_c, btn_d, btn_str, btn_hsh)

        for button in btn_list:
            button.setFixedWidth(40)
            button.setFont(QFont('', 18))

        # Create the "dial pad" group box & layout
        keypad_grpbox = QGroupBox(self.tr('Keypad:'))
        keypad_layout = QGridLayout()
        keypad_layout.addWidget(btn_1, 0, 0)
        keypad_layout.addWidget(btn_2, 0, 1)
        keypad_layout.addWidget(btn_3, 0, 2)
        keypad_layout.addWidget(btn_a, 0, 3)
        keypad_layout.addWidget(btn_4, 1, 0)
        keypad_layout.addWidget(btn_5, 1, 1)
        keypad_layout.addWidget(btn_6, 1, 2)
        keypad_layout.addWidget(btn_b, 1, 3)
        keypad_layout.addWidget(btn_7, 2, 0)
        keypad_layout.addWidget(btn_8, 2, 1)
        keypad_layout.addWidget(btn_9, 2, 2)
        keypad_layout.addWidget(btn_c, 2, 3)
        keypad_layout.addWidget(btn_str, 3, 0)
        keypad_layout.addWidget(btn_0, 3, 1)
        keypad_layout.addWidget(btn_hsh, 3, 2)
        keypad_layout.addWidget(btn_d, 3, 3)
        keypad_grpbox.setLayout(keypad_layout)

        self.command_string = QLineEdit()
        send_string_btn = QPushButton(QIcon(':/images/bullet_go.png'), '')
        send_string_grpbox = QGroupBox(self.tr('Send String of Tones:'))
        send_string_layout = QVBoxLayout()
        send_string_layout.addWidget(QLabel(self.tr('Send a series of DTMF tones.')))
        send_string_layout.addWidget(QLabel(self.tr('Comma separate values. i.e. "1,2,A,3" (without quotes)')))
        send_string_sublayout = QHBoxLayout()
        send_string_sublayout.addWidget(self.command_string)
        send_string_sublayout.addWidget(send_string_btn)
        send_string_layout.addLayout(send_string_sublayout)
        send_string_grpbox.setLayout(send_string_layout)

        sub_container = QVBoxLayout()
        sub_container.addStretch()
        sub_container.addWidget(keypad_grpbox)
        sub_container.addWidget(send_string_grpbox)
        sub_container.addStretch()

        # Create main layout
        container = QHBoxLayout()
        container.addStretch()
        container.addLayout(sub_container)
        container.addStretch()
        self.setLayout(container)

        # Connect widgets
        self.connect(btn_0, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="0"'))
        self.connect(btn_1, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="1"'))
        self.connect(btn_2, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="2"'))
        self.connect(btn_3, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="3"'))
        self.connect(btn_4, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="4"'))
        self.connect(btn_5, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="5"'))
        self.connect(btn_6, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="6"'))
        self.connect(btn_7, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="7"'))
        self.connect(btn_8, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="8"'))
        self.connect(btn_9, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="9"'))
        self.connect(btn_a, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="A"'))
        self.connect(btn_b, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="B"'))
        self.connect(btn_c, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="C"'))
        self.connect(btn_d, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="D"'))
        self.connect(btn_str, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="*"'))
        self.connect(btn_hsh, SIGNAL('clicked()'), lambda: terminal.send_command('AT+VTS="#"'))
        self.connect(send_string_btn, SIGNAL('clicked()'), self.send_string)

    def validate_dtmf_string(self, dtmf_string):
        """
        Checks for any errors in the string to be used in the DTMF AT command.

        If an error is found the error message will be returned, as a string.
        If no errors occur then "None" is returned.
        """

        # Check for any invalid characters
        allowed_chars = '0123456789*#ABCD,'

        for char in dtmf_string:
            char_original = char.strip()
            char_upper = char_original.upper()
            if char_upper and char_upper not in allowed_chars:
                return 'Character "%s" is invalid.' % char_original

        # Strip spaces and commas from both ends of the string
        dtmf_string = dtmf_string.strip(' ,')

        # Check each "item" is valid
        items = dtmf_string.split(',')

        for item in items:
            item = item.strip()
            if len(item) != 1:
                return 'The specified tone string is invalid, please check.'

    def send_string(self):
        dial_string = str(self.command_string.text()).strip(' ,')

        error_msg = self.validate_dtmf_string(dial_string)
        if error_msg:
            QMessageBox.critical(self, self.tr('Error'), self.tr(error_msg), QMessageBox.Ok)
            self.command_string.setFocus()
            self.command_string.selectAll()
            return

        items = [i.strip().upper() for i in dial_string.split(',')]
        self.terminal.send_command('AT+VTS="%s"' % ','.join(items))

if __name__ == '__main__':
    from standalone import run_standalone
    run_standalone(DtmfKeypadWidget)
