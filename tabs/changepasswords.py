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
Module containing the "Change Passwords" commands class/widget.
"""

# 3rd party modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ChangePasswordsWidget(QWidget):
    """
    Defines the GUI and behaviour of the "Change Passwords" commands widget.
    """
    TITLE = 'Change Passwords'

    def __init__(self, terminal, parent=None):
        """
        Initialize the interface widgets.
        """
        QWidget.__init__(self, parent)

        # Store the terminal object for later reference
        self.terminal = terminal

        # Create "Facility" widgets & group box
        self.facility_ps = QRadioButton(self.tr('PS (Lock phone to SIM card)'))
        self.facility_ps.setChecked(True)
        self.facility_sc = QRadioButton(self.tr('SC (Lock SIM card)'))
        self.facility_p2 = QRadioButton(self.tr('P2 (SIM PIN2)'))
        self.facility_ao = QRadioButton(self.tr('AO (BOAC)'))
        self.facility_oi = QRadioButton(self.tr('OI (BOIC)'))
        self.facility_ai = QRadioButton(self.tr('AI (BAIC)'))
        self.facility_ir = QRadioButton(self.tr('IR (BIC-Roam)'))
        self.facility_ox = QRadioButton(self.tr('OX (BOIC-exHC)'))
        self.facility_ab = QRadioButton(self.tr('AB (All Barring)'))
        self.facility_ag = QRadioButton(self.tr('AG (All Outgoing Barring)'))
        self.facility_ac = QRadioButton(self.tr('AC (All Incoming Barring)'))

        facility_box = QGroupBox(self.tr('Facility:'))
        facility_box_layout = QVBoxLayout()
        facility_box_layout.addWidget(self.facility_ps)
        facility_box_layout.addWidget(self.facility_sc)
        facility_box_layout.addWidget(self.facility_p2)
        facility_box_layout.addWidget(self.facility_ao)
        facility_box_layout.addWidget(self.facility_oi)
        facility_box_layout.addWidget(self.facility_ai)
        facility_box_layout.addWidget(self.facility_ir)
        facility_box_layout.addWidget(self.facility_ox)
        facility_box_layout.addWidget(self.facility_ab)
        facility_box_layout.addWidget(self.facility_ag)
        facility_box_layout.addWidget(self.facility_ac)
        facility_box.setLayout(facility_box_layout)

        # Create controls widgets & group box
        self.old_pw_txt = QLineEdit()
        self.new_pw_txt = QLineEdit()
        change_pw_btn = QPushButton(self.tr('Change Password'))
        test_cmd_btn = QPushButton(self.tr('Run Test Command (AT+CPWD=?)'))

        control_box = QVBoxLayout()
        control_box.addWidget(QLabel(self.tr('Old Password:')))
        control_box.addWidget(self.old_pw_txt)
        control_box.addWidget(QLabel(self.tr('New Password:')))
        control_box.addWidget(self.new_pw_txt)
        control_box.addWidget(change_pw_btn)
        control_box.addWidget(test_cmd_btn)
        control_box.addStretch()

        # Create main layout
        container = QHBoxLayout()
        container.addWidget(facility_box)
        container.addLayout(control_box)
        container.addStretch()
        self.setLayout(container)

        # Connect widgets
        self.connect(change_pw_btn, SIGNAL('clicked()'), self.change_pw)
        self.connect(test_cmd_btn, SIGNAL('clicked()'), lambda: terminal.send_command('AT+CPWD=?'))

    def validate_network_pw(self, network_pw):
        """
        Check that a given network password is valid. The network
        password must be exactly 4 digits.
        """
        network_pw = str(network_pw)

        # Check that the network password is not empty
        if len(network_pw) == 0:
            raise ValueError('Please enter a network password.')

        # Check that the network password is only digits
        if not network_pw.isdigit():
            raise ValueError('The network password can only contain digits.')

    def get_facility(self):
        """
        Determine which facility is selected on the GUI and return
        the corresponding code to be used in AT commands.
        """
        if self.facility_ps.isChecked(): return 'PS'
        if self.facility_sc.isChecked(): return 'SC'
        if self.facility_p2.isChecked(): return 'P2'
        if self.facility_ao.isChecked(): return 'AO'
        if self.facility_oi.isChecked(): return 'OI'
        if self.facility_ai.isChecked(): return 'AI'
        if self.facility_ir.isChecked(): return 'IR'
        if self.facility_ox.isChecked(): return 'OX'
        if self.facility_ab.isChecked(): return 'AB'
        if self.facility_ag.isChecked(): return 'AG'
        if self.facility_ac.isChecked(): return 'AC'

    def change_pw(self):
        """
        Send the AT command to change the password for the the currently selected facility.
        """

        # Get the necessary options
        facility = self.get_facility()
        old_network_pw = str(self.old_pw_txt.text())
        new_network_pw = str(self.new_pw_txt.text())

        # Validate the old network password
        try:
            self.validate_network_pw(old_network_pw)
        except ValueError, e:
            QMessageBox.critical(self, self.tr('Error'), self.tr(e.message), QMessageBox.Ok)
            self.old_pw_txt.setFocus()
            self.old_pw_txt.selectAll()
            return

        # Validate the new network password
        try:
            self.validate_network_pw(new_network_pw)
        except ValueError, e:
            QMessageBox.critical(self, self.tr('Error'), self.tr(e.message), QMessageBox.Ok)
            self.new_pw_txt.setFocus()
            self.new_pw_txt.selectAll()
            return

        # Create the change password command string
        command = 'AT+CPWD="%s", "%s", "%s"' % (facility, old_network_pw, new_network_pw)

        # Run the AT command in the terminal
        self.terminal.send_command(command)

if __name__ == '__main__':
    from standalone import run_standalone
    run_standalone(ChangePasswordsWidget)
