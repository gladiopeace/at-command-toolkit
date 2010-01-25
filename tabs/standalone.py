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
Module containing code to run tab widgets as standalone applications.

This is useful when developing or debugging as it allows the behaviour of the
widget to be isolated from the rest of the application.

Instead of using the terminal object that writes to the serial port a dummy
terminal object is created that supports the "send_command" method, but writes
commands to stdout so that the AT commands can be inspected.
"""

# Standard library modules
import sys

# 3rd party modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DummyTerminal(object):
    def send_command(self, command):
        """
        AT commands are written to sys.stdout
        """
        sys.stdout.write(command + '\n')


def run_standalone(widget):
    """
    Function to run a tab widget as a standalone application.

    Creates an instance of the widget passed as a parameter with
    a dummy terminal and displays the widget in a main window.
    """
    app = QApplication(sys.argv)
    form = QMainWindow()

    # Create a dummy terminal & widget
    terminal = DummyTerminal()
    widget = widget(terminal)

    # Set up the form & display it
    form.setCentralWidget(widget)
    form.setWindowTitle(widget.TITLE)
    form.show()
    sys.exit(app.exec_())
