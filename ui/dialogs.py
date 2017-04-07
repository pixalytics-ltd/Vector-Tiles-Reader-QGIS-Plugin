from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QColor, QAction, QIcon, QMenu, QToolButton, QFileDialog, QMessageBox
from dlg_file_connection import Ui_DlgFileConnection
from dlg_server_connections import Ui_DlgServerConnections
from dlg_edit_server_connection import Ui_DlgEditServerConnection
import os


class FileConnectionDialog(QtGui.QDialog, Ui_DlgFileConnection):

    on_open = pyqtSignal(str)

    def __init__(self, home_directory):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.path = None
        self.home_directory = home_directory
        self.btnBrowse.clicked.connect(self._open_browser)
        self.txtPath.textChanged.connect(self._on_path_changed)
        self.rbFile.toggled.connect(self._update_open_button_state)
        self.rbDirectory.toggled.connect(self._update_open_button_state)
        self.btnOpen.clicked.connect(self._handle_open_click)

    def load_directory_checked(self):
        return self.rbDirectory.isChecked()

    def is_apply_styles_enabled(self):
        return self.chkApplyStyles.isChecked()

    def is_merge_tiles_enabled(self):
        return self.chkMergeTiles.isChecked()

    def _open_browser(self):
        open_path = self.path
        if not open_path:
            open_path = self.home_directory

        if self.rbFile.isChecked():
            open_file_name = QFileDialog.getOpenFileName(None, "Select Mapbox Tiles", open_path, "Mapbox Tiles (*.mbtiles)")
        else:
            open_file_name = QFileDialog.getExistingDirectory(None, "Select Mapbox Tiles Directory", open_path)

        if open_file_name:
            self.path = open_file_name
            self.txtPath.setText(open_file_name)

    def _on_path_changed(self):
        self.path = self.txtPath.text()
        self._update_open_button_state()

    def _update_open_button_state(self):
        is_valid_dir = self.rbDirectory.isChecked() and os.path.isdir(self.path)
        is_valid_file = self.rbFile.isChecked() and os.path.isfile(self.path) and os.path.splitext(self.path)[1] == ".mbtiles"
        is_enabled = is_valid_dir or is_valid_file
        self.btnOpen.setEnabled(is_enabled)

    def _handle_open_click(self):
        self.close()
        self.on_open.emit(self.path)

    def show(self):
        self.exec_()


class ServerConnectionDialog(QtGui.QDialog, Ui_DlgServerConnections):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)


class EditServerConnection(QtGui.QDialog, Ui_DlgEditServerConnection):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)