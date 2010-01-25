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
Module containing the "Set Functionality" commands class/widget.
"""

# 3rd party modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SetFunctionalityWidget(QWidget):
    """
    Defines the GUI and behaviour of the "Set Functionality" commands widget.
    """
    TITLE = 'Set Functionality'

    def __init__(self, terminal, parent=None):
        """
        Initialize the interface widgets.
        """
        QWidget.__init__(self, parent)

        # Store the terminal object for later reference
        self.terminal = terminal

        # Create the radio buttons
        self.level0_rad = QRadioButton(self.tr('0 - Turn handset off'))
        self.level1_rad = QRadioButton(self.tr('1 - Full functionality'))
        self.level2_rad = QRadioButton(self.tr('2 - Disable phone transmit RF circuits only'))
        self.level3_rad = QRadioButton(self.tr('3 - Disable phone receive RF circuits only'))
        self.level4_rad = QRadioButton(self.tr('4 - Disable phone receive & transmit RF circuits\n(i.e. Flight mode)'))
        self.level5_rad = QRadioButton(self.tr('5 - GSM only (WCDMA radio off)'))
        self.level6_rad = QRadioButton(self.tr('6 - WCDMA only (GSM radio off)'))
        set_level_btn = QPushButton(self.tr('Set Functionality'))

        # Check the "1 - Full functionality" radio button
        self.level1_rad.setChecked(True)

        # Create the button groupbox & layout
        button_gb = QGroupBox(self.tr('Select Functionality Level:'))
        button_box = QVBoxLayout()
        button_box.addWidget(self.level0_rad)
        button_box.addWidget(self.level1_rad)
        button_box.addWidget(self.level2_rad)
        button_box.addWidget(self.level3_rad)
        button_box.addWidget(self.level4_rad)
        button_box.addWidget(self.level5_rad)
        button_box.addWidget(self.level6_rad)
        button_box.addWidget(set_level_btn)
        button_gb.setLayout(button_box)

        # Create main layout
        container = QHBoxLayout()
        container.addStretch()
        container.addWidget(button_gb)
        container.addStretch()
        self.setLayout(container)

        # Connect widgets
        self.connect(set_level_btn, SIGNAL('clicked()'), self.set_functionality)

    def set_functionality(self):
        if self.level0_rad.isChecked(): self.terminal.send_command('AT+CFUN=0')
        elif self.level1_rad.isChecked(): self.terminal.send_command('AT+CFUN=1')
        elif self.level2_rad.isChecked(): self.terminal.send_command('AT+CFUN=2')
        elif self.level3_rad.isChecked(): self.terminal.send_command('AT+CFUN=3')
        elif self.level4_rad.isChecked(): self.terminal.send_command('AT+CFUN=4')
        elif self.level5_rad.isChecked(): self.terminal.send_command('AT+CFUN=5')
        elif self.level6_rad.isChecked(): self.terminal.send_command('AT+CFUN=6')

if __name__ == '__main__':
    from standalone import run_standalone
    run_standalone(SetFunctionalityWidget)
