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
Module containing the "Call Barring" commands class/widget.
"""

# 3rd party modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CallBarringWidget(QWidget):
    """
    Defines the GUI and behaviour of the "Call Barring" commands widget.
    """
    TITLE = 'Call Barring'

    def __init__(self, terminal, parent=None):
        """
        Initialize the interface widgets.
        """
        QWidget.__init__(self, parent)

        # Store the terminal object for later reference
        self.terminal = terminal

        # Create "Facility" widgets & group box
        self.facility_ao = QRadioButton(self.tr('AO (BAOC)'))
        self.facility_ao.setChecked(True)
        self.facility_oi = QRadioButton(self.tr('OI (BOIC)'))
        self.facility_ox = QRadioButton(self.tr('OX (BOIC-exHC)'))
        self.facility_ai = QRadioButton(self.tr('AI (BAIC)'))
        self.facility_ir = QRadioButton(self.tr('IR (BIC-Roam)'))
        self.facility_ac = QRadioButton(self.tr('AC (All Incoming)'))
        self.facility_ag = QRadioButton(self.tr('AG (All Outgoing)'))
        self.facility_ab = QRadioButton(self.tr('AB (All Barring)'))

        facility_box = QGroupBox(self.tr('Facility:'))
        facility_box_layout = QVBoxLayout()
        facility_box_layout.addWidget(self.facility_ao)
        facility_box_layout.addWidget(self.facility_oi)
        facility_box_layout.addWidget(self.facility_ox)
        facility_box_layout.addWidget(self.facility_ai)
        facility_box_layout.addWidget(self.facility_ir)
        facility_box_layout.addWidget(self.facility_ac)
        facility_box_layout.addWidget(self.facility_ag)
        facility_box_layout.addWidget(self.facility_ab)
        facility_box.setLayout(facility_box_layout)

        # Create "Class" widgets & group box
        class_toggle = QCheckBox(self.tr('(Toggle All Classes)'))
        self.class_voice = QCheckBox(self.tr('1 (Voice)'))
        self.class_data = QCheckBox(self.tr('2 (Data)'))
        self.class_fax = QCheckBox(self.tr('4 (Fax)'))
        self.class_sms = QCheckBox(self.tr('8 (SMS)'))
        self.class_sync = QCheckBox(self.tr('16 (Data Circuit Sync)'))
        self.class_async = QCheckBox(self.tr('32 (Data Circuit ASync)'))
        self.class_packet_access = QCheckBox(self.tr('64 (Dedicated Packet Access)'))
        self.class_pad_access = QCheckBox(self.tr('128 (Dedicated Pad Access)'))

        class_box = QGroupBox(self.tr('Classes:'))
        class_box_layout = QVBoxLayout()
        class_box_layout.addWidget(class_toggle)
        class_box_layout.addWidget(self.class_voice)
        class_box_layout.addWidget(self.class_data)
        class_box_layout.addWidget(self.class_fax)
        class_box_layout.addWidget(self.class_sms)
        class_box_layout.addWidget(self.class_sync)
        class_box_layout.addWidget(self.class_async)
        class_box_layout.addWidget(self.class_packet_access)
        class_box_layout.addWidget(self.class_pad_access)
        class_box.setLayout(class_box_layout)

        # Create buttons & network password widget
        self.cb_enable_btn = QPushButton(self.tr('Enable'))
        self.cb_disable_btn = QPushButton(self.tr('Disable'))
        self.cb_interrogate_btn = QPushButton(self.tr('Interrogate'))
        self.network_pw = QLineEdit()
        self.network_pw.setMaximumWidth(40)
        network_pw_box = QHBoxLayout()
        network_pw_box.addWidget(QLabel(self.tr('Network Password:')))
        network_pw_box.addWidget(self.network_pw)

        # Create right hand side layout
        actions_layout = QVBoxLayout()
        actions_layout.addWidget(self.cb_enable_btn)
        actions_layout.addWidget(self.cb_disable_btn)
        actions_layout.addWidget(self.cb_interrogate_btn)
        actions_layout.addLayout(network_pw_box)
        actions_layout.addStretch()

        # Create main layout
        container = QHBoxLayout()
        container.addWidget(facility_box)
        container.addWidget(class_box)
        container.addLayout(actions_layout)
        self.setLayout(container)

        # Connect widgets
        self.connect(self.facility_ao, SIGNAL('toggled(bool)'), self.check_facility)
        self.connect(self.facility_oi, SIGNAL('toggled(bool)'), self.check_facility)
        self.connect(self.facility_ox, SIGNAL('toggled(bool)'), self.check_facility)
        self.connect(self.facility_ai, SIGNAL('toggled(bool)'), self.check_facility)
        self.connect(self.facility_ir, SIGNAL('toggled(bool)'), self.check_facility)
        self.connect(self.facility_ac, SIGNAL('toggled(bool)'), self.check_facility)
        self.connect(self.facility_ag, SIGNAL('toggled(bool)'), self.check_facility)
        self.connect(self.facility_ab, SIGNAL('toggled(bool)'), self.check_facility)
        self.connect(class_toggle, SIGNAL('stateChanged(int)'), self.toggle_classes)
        self.connect(self.cb_enable_btn, SIGNAL('clicked()'), self.enable_command)
        self.connect(self.cb_disable_btn, SIGNAL('clicked()'), self.disable_command)
        self.connect(self.cb_interrogate_btn, SIGNAL('clicked()'), self.interrogate_facility)

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
        if self.facility_ao.isChecked(): return 'AO'
        if self.facility_oi.isChecked(): return 'OI'
        if self.facility_ox.isChecked(): return 'OX'
        if self.facility_ai.isChecked(): return 'AI'
        if self.facility_ir.isChecked(): return 'IR'
        if self.facility_ac.isChecked(): return 'AC'
        if self.facility_ag.isChecked(): return 'AG'
        if self.facility_ab.isChecked(): return 'AB'

    def get_classes(self):
        """
        Determine which classes are selected on the GUI and return
        the corresponding class integer to be used in AT commands.
        """
        i = 0
        if self.class_voice.isChecked(): i += 1
        if self.class_data.isChecked(): i += 2
        if self.class_fax.isChecked(): i += 4
        if self.class_sms.isChecked(): i += 8
        if self.class_sync.isChecked(): i += 16
        if self.class_async.isChecked(): i += 32
        if self.class_packet_access.isChecked(): i += 64
        if self.class_pad_access.isChecked(): i += 128
        return i

    def toggle_classes(self, state):
        """
        Toggle the "class" check boxes on and off according to
        the "Toggle All Classes" check box state.

        This is invoked whenever the "Toggle All Classes" state is changed.
        """
        value = True if state == 2 else False

        self.class_voice.setChecked(value)
        self.class_data.setChecked(value)
        self.class_fax.setChecked(value)
        self.class_sms.setChecked(value)
        self.class_sync.setChecked(value)
        self.class_async.setChecked(value)
        self.class_packet_access.setChecked(value)
        self.class_pad_access.setChecked(value)

    def enable_command(self):
        self.barring_command(True)

    def disable_command(self):
        self.barring_command(False)

    def barring_command(self, enable):

        # Get the necessary options
        facility = self.get_facility()
        action = 1 if enable else 0
        network_pw = str(self.network_pw.text())
        classes = self.get_classes()

        # Validate the network password
        try:
            self.validate_network_pw(network_pw)
        except ValueError, e:
            QMessageBox.critical(self, self.tr('Error'), self.tr(e.message), QMessageBox.Ok)
            self.network_pw.setFocus()
            self.network_pw.selectAll()
            return

        if classes:
            command = 'AT+CLCK="%s", %d, "%s", %d' % (facility, action, network_pw, classes)
        else:
            command = 'AT+CLCK="%s", %d, "%s"' % (facility, action, network_pw)

        # Run the AT command in the terminal
        self.terminal.send_command(command)

    def interrogate_facility(self):
        """
        Send the AT command to interrogate the currently selected facility.
        The result will be displayed in the terminal window.
        """
        self.terminal.send_command('AT+CLCK="%s", 2' % self.get_facility())

    def check_facility(self):
        """
        Check which facility has been selected and disable any commands
        that are not available to the chosen facility.

        This method is triggered whenever a facility radio box is selected.
        """

        # Enable the "enable" and "interrogate" buttons
        self.cb_enable_btn.setEnabled(True)
        self.cb_interrogate_btn.setEnabled(True)

        # Define a list of facilities that can only be disabled
        disable_only = ('AC', 'AG', 'AB')

        # Get the currently selected facility code & disable any necessary widgets
        if self.get_facility() in disable_only:
            self.cb_enable_btn.setDisabled(True)
            self.cb_interrogate_btn.setDisabled(True)

if __name__ == '__main__':
    from standalone import run_standalone
    run_standalone(CallBarringWidget)
