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
Module containing the "Basic Info" commands class/widget.
"""

# 3rd party modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class BasicInfoWidget(QWidget):
    """
    Defines the GUI and behaviour of the "Basic Info" commands widget.
    """
    TITLE = 'Basic Info'

    def __init__(self, terminal, parent=None):
        """
        Initialize the interface widgets.
        """
        QWidget.__init__(self, parent)

        # Create the buttons
        imei_btn = QPushButton(self.tr('IMEI'))
        imsi_btn = QPushButton(self.tr('IMSI'))
        manufacturer_btn = QPushButton(self.tr('Manufacturer'))
        model_btn = QPushButton(self.tr('Model'))
        software_btn = QPushButton(self.tr('Software Revision'))
        modem_btn = QPushButton(self.tr('Modem Capabilities'))
        commands_btn = QPushButton(self.tr('Available AT Commands'))

        # Create the button groupbox & layout
        display_btns = QGroupBox(self.tr('Display Information:'))
        button_box = QVBoxLayout()
        button_box.addWidget(imei_btn)
        button_box.addWidget(imsi_btn)
        button_box.addWidget(manufacturer_btn)
        button_box.addWidget(model_btn)
        button_box.addWidget(software_btn)
        button_box.addWidget(modem_btn)
        button_box.addWidget(commands_btn)
        display_btns.setLayout(button_box)

        # Create main layout
        container = QHBoxLayout()
        container.addStretch()
        container.addWidget(display_btns)
        container.addStretch()
        self.setLayout(container)

        # Connect widgets
        self.connect(imei_btn, SIGNAL('clicked()'), lambda: terminal.send_command('AT+CGSN'))
        self.connect(imsi_btn, SIGNAL('clicked()'), lambda: terminal.send_command('AT+CIMI'))
        self.connect(manufacturer_btn, SIGNAL('clicked()'), lambda: terminal.send_command('AT+GMI'))
        self.connect(model_btn, SIGNAL('clicked()'), lambda: terminal.send_command('AT+GMM'))
        self.connect(software_btn, SIGNAL('clicked()'), lambda: terminal.send_command('AT+GMR'))
        self.connect(modem_btn, SIGNAL('clicked()'), lambda: terminal.send_command('AT+GCAP'))
        self.connect(commands_btn, SIGNAL('clicked()'), lambda: terminal.send_command('AT+CLAC'))

if __name__ == '__main__':
    from standalone import run_standalone
    run_standalone(BasicInfoWidget)
