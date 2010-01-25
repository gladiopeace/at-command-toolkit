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
Top level application file for the AT Command Toolkit application.
"""
__version__ = 'x.x'
APP_NAME = 'AT Command Toolkit'
AUTHOR = 'Craig Dodd'
ORGANIZATION = 'Shelltoad Computing'
COPYRIGHT = 'GNU General Public License v3'

# Try to import required modules
try:
    # Standard library modules
    import sys

    # 3rd party modules
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

    # Local application modules
    from connectdlg import ConnectDlg
    import resources
    from tabs.basicinfo import BasicInfoWidget
    from tabs.callbarring import CallBarringWidget
    from tabs.callcontrol import CallControlWidget
    from tabs.changepasswords import ChangePasswordsWidget
    from tabs.dtmfkeypad import DtmfKeypadWidget
    from tabs.setfunctionality import SetFunctionalityWidget
    from terminal import TerminalWidget

# Display a Tkinter messagebox if a module failed to import (assumes that the
# Tkinter modules are available, which they should be)
except ImportError, e:
    import Tkinter, tkMessageBox
    root = Tkinter.Tk()
    root.withdraw()

    # Get the name of the module that could not be imported and display an
    # error dialog.
    module_name = e.message.split()[-1]
    tkMessageBox.showerror('Error: Module Not Found',
                           'The module "%s" is not installed. This is required for the %s to run.' % (module_name, APP_NAME))
    sys.exit(1)

class MainWindow(QMainWindow):
    """
    This class defines the GUI and behaviour of the main application window.
    """

    def __init__(self, parent=None):
        """
        Create the layout of the form and registers widgets with their associated methods.
        """
        QMainWindow.__init__(self, parent)

        # Setup the window settings
        self.setWindowTitle(self.tr(APP_NAME))
        self.setMinimumSize(550, 400)

        # Create actions
        file_exit_action = QAction(self.tr('E&xit'), self)
        file_exit_action.setToolTip(self.tr('Exit the Application'))
        file_exit_action.setIcon(QIcon(':/images/door_open.png'))
        self.connect(file_exit_action, SIGNAL('triggered()'), self.close)

        set_font_action = QAction(self.tr('Set Terminal Font'), self)
        set_font_action.setToolTip(self.tr('Set the terminal font'))
        set_font_action.setIcon(QIcon('images/font.png'))
        self.connect(set_font_action, SIGNAL('triggered()'), self.set_terminal_font)

        about_action = QAction(self.tr('About'), self)
        about_action.setToolTip(self.tr('About'))
        about_action.setIcon(QIcon(':/images/icon_info.gif'))
        self.connect(about_action, SIGNAL('triggered()'), self.show_about)

        self.connect_com_action = QAction('Connect COM Port', self)
        self.connect_com_action.setToolTip('Connect COM Port')
        self.connect_com_action.setIcon(QIcon(':/images/connect.png'))
        self.connect(self.connect_com_action, SIGNAL('triggered()'), self.connect_com_port)

        self.disconnect_com_action = QAction('Disconnect COM Port', self)
        self.disconnect_com_action.setToolTip('Disconnect COM Port')
        self.disconnect_com_action.setIcon(QIcon(':/images/disconnect.png'))
        self.disconnect_com_action.setDisabled(True)
        self.connect(self.disconnect_com_action, SIGNAL('triggered()'), self.disconnect_com_port)

        # Create & dock the terminal widget
        self.terminal = TerminalWidget()
        self.connect(self.terminal, SIGNAL('connectionError()'), self.disconnect_com_port)

        terminal_dock = QDockWidget(self.tr('Terminal'), self)
        terminal_dock.setFeatures(QDockWidget.NoDockWidgetFeatures |
                                  QDockWidget.DockWidgetFloatable |
                                  QDockWidget.DockWidgetMovable)
        terminal_dock.setWidget(self.terminal)

        self.addDockWidget(Qt.BottomDockWidgetArea, terminal_dock)

        # Create the main window tabs
        self.main_tabs = QTabWidget()
        self.main_tabs.addTab(BasicInfoWidget(self.terminal), self.tr(BasicInfoWidget.TITLE))
        self.main_tabs.addTab(CallBarringWidget(self.terminal), self.tr(CallBarringWidget.TITLE))
        self.main_tabs.addTab(CallControlWidget(self.terminal), self.tr(CallControlWidget.TITLE))
        self.main_tabs.addTab(ChangePasswordsWidget(self.terminal), self.tr(ChangePasswordsWidget.TITLE))
        self.main_tabs.addTab(DtmfKeypadWidget(self.terminal), self.tr(DtmfKeypadWidget.TITLE))
        self.main_tabs.addTab(SetFunctionalityWidget(self.terminal), self.tr(SetFunctionalityWidget.TITLE))
        self.setCentralWidget(self.main_tabs)

        # Connect to the COM port
        self.connect_com_port(exit_on_fail=True)

        # Create the menubar
        file_menu = self.menuBar().addMenu(self.tr('&File'))
        file_menu.addAction(set_font_action)
        file_menu.addAction(file_exit_action)

        com_port_menu = self.menuBar().addMenu('&COM Port')
        com_port_menu.addAction(self.connect_com_action)
        com_port_menu.addAction(self.disconnect_com_action)

        help_menu = self.menuBar().addMenu(self.tr('&Help'))
        help_menu.addAction(about_action)

        # Create a QSettings instance to access stored settings
        self.settings = QSettings()

        # Get the previous terminal font
        previous_font = self.settings.value('TerminalFont')
        if previous_font.type() == QVariant.Font:
            self.current_font = QFont(previous_font)
            self.terminal.set_font(self.current_font)
        else:
            self.current_font = QFont()

    def connect_com_port(self, exit_on_fail=False):
        connect_dialog = ConnectDlg(self)
        if connect_dialog.exec_():

            # Connect to the COM port
            self.terminal.serial_conn = connect_dialog.serial_conn
            self.terminal.connect_com_port()

            # Update the GUI
            self.main_tabs.setEnabled(True)
            self.disconnect_com_action.setEnabled(True)
            self.connect_com_action.setDisabled(True)
        else:
            if exit_on_fail:
                self.close()
    
    def disconnect_com_port(self):

        # Disconnect the terminal
        self.terminal.disconnect_com_port()

        # Update the GUI
        self.main_tabs.setDisabled(True)
        self.disconnect_com_action.setDisabled(True)
        self.connect_com_action.setEnabled(True)

    def set_terminal_font(self):
        """
        Displays a font selection dialog box and sets the font of the terminal widgets.
        Saves the selected font using a QSettings instance stored in "self".
        """

        # Display a font selection dialog box
        font, ok = QFontDialog.getFont(self.current_font)
        if ok:

            # Store the selected font, set the terminal font & save the
            # selected font settings.
            self.current_font = font
            self.terminal.set_font(font)
            self.settings.setValue('TerminalFont', QVariant(font))

    def show_about(self):
        """
        Display the "about" dialog box.
        """
        message = '''<font size="+2">%s</font> v%s
                     <p>GUI for sending AT commands.
                     <p>Written by %s
                     <br>&copy; %s
                     <p>Icons by <a href="http://www.famfamfam.com/">famfamfam</a> and
                     <a href="http://dryicons.com/">dryicons</a>.''' % (APP_NAME,
                                                                        __version__,
                                                                        AUTHOR,
                                                                        COPYRIGHT)

        QMessageBox.about(self, 'About ' + APP_NAME, message)

    #def close(self):
    #    self.settings.setValue("geometry", QVariant(self.saveGeometry()))
    #    self.settings.setValue("state", QVariant(self.saveState()))

    #    QMainWindow.close(self)

    #def closeEvent(self, event):
    #    self.close()

if __name__ == '__main__':

    # Create a QApplication instance
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/images/mobile_phone.png'))
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORGANIZATION)

    # Create an instance of the main window
    form = MainWindow()
    form.show()

    # Start the main event loop
    sys.exit(app.exec_())
