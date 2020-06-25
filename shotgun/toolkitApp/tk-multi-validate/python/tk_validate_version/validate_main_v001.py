import sgtk
import sys
import os
import posixpath
import logging

from sgtk.platform import Application
from sgtk.platform.qt import QtCore, QtGui
from .ui import validateUI
from shot_final_check import ShotFinalCheck


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system.

    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Validate Version", app_instance, ValidateVersion)


class ValidateVersion(QtGui.QWidget, validateUI.Ui_Form):

    def __init__(self, parent=None):
        # QtGui.QWidget.__init__(self)

        logging.info("INFO: Initialized class {}".format(self.__class__))
        super(ValidateVersion, self).__init__()
        self.setupUi(self)
        self._combobox_items = {'select': 0, 'Shot Final Check': 1, 'Di Final Check': 2}
        self._app = sgtk.platform.current_bundle()
        self._ctx = self._app.context
        self.ui_reset()
        # Enable dragging and dropping onto the GUI
        self.setAcceptDrops(True)
        # Signals and Slotting
        self.ui_connect()

    def ui_connect(self):
        """

        :return:
        """
        self.validate_pushButton.clicked.connect(self.process_validation)
        self.reset_pushButton.clicked.connect(self.ui_reset)

    def ui_reset(self):
        """

        :return:
        """
        self.log_items = ''
        self._file_data_list = []
        self.log_textEdit.clear()
        self.validation_type_comboBox.clear()
        self.validation_type_comboBox.addItems(sorted(self._combobox_items.keys(), reverse=True))
        self.validation_type_comboBox.setCurrentIndex(0)
        self.ui_switch(0, 1)
        self.log_textEdit.setText('Results')

    def ui_switch(self, validate, validation_type):
        """

        :param validate:
        :param validation_type:
        :return:
        """
        self.validate_pushButton.setEnabled(validate)
        self.validation_type_comboBox.setEnabled(validation_type)

    # The following three methods set up dragging and dropping for the app
    def dragEnterEvent(self, e):
        """

        :param e:
        :return:
        """
        if self.validation_type_comboBox.isEnabled():
            if e.mimeData().hasUrls():
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        """

        :param e:
        :return:
        """
        if self.validation_type_comboBox.isEnabled():
            if e.mimeData().hasUrls():
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Drop files directly onto the widget
        File locations are stored in fname
        :param e:
        :return:
        """
        if self.validation_type_comboBox.isEnabled() and self._combobox_items[self.validation_type_comboBox.currentText()] != 0:
            if e.mimeData().hasUrls():
                self.ui_switch(1, 0)
                e.setDropAction(QtCore.Qt.CopyAction)
                e.accept()
                self.initialize_validation()
                # Workaround for OSx dragging and dropping
                for url in e.mimeData().urls():
                    if sys.platform.lower() == 'win32':
                        final_path = url.path()[1:]
                    else:
                        final_path = url.path()
                    if os.path.isdir(final_path):
                        self._file_data_list.extend([each_file for each_file in os.listdir(final_path) if os.path.isfile(posixpath.join(final_path, each_file))])
                    else:
                        self._file_data_list.append(final_path)
                    self.log_items += '\n{}'.format(self._file_data_list)
                    self.log_textEdit.setText(self.log_items)
            else:
                e.ignore()
        else:
            e.ignore()

    def initialize_validation(self):
        """

        :return:
        """
        self.log_items += 'Validation Initialized...'
        self.log_textEdit.setText(self.log_items)

    def process_validation(self):
        """

        :return:
        """
        for file_path in self._file_data_list:
            if self._combobox_items[str(self.validation_type_comboBox.currentText())] == 1:
                self.log_items += '\nValidation Started for {}...'.format(self.validation_type_comboBox.currentText())
                self.log_textEdit.setText(self.log_items)
                ShotFinalCheckInst = ShotFinalCheck()
                self.log_items += ShotFinalCheckInst.final_check_log
                self.log_textEdit.setText(self.log_items)
                ShotFinalCheckInst.process_file_data(file_path)
                self.log_items += ShotFinalCheckInst.final_check_log
                self.log_textEdit.setText(self.log_items)
                ShotFinalCheckInst.process_final_check(ShotFinalCheckInst.get_final_avid)
                self.log_items += ShotFinalCheckInst.final_check_log
                self.log_textEdit.setText(self.log_items)
                self.log_items += '\n\n\t\t{0} Generating Final Report {0}'.format('*'*15)
                self.log_textEdit.setText(self.log_items)
                self.log_items += '\n\n\tVersions missing from Avid but finalled in Shotgun: {}'.format(len(ShotFinalCheckInst.get_final_not_avid))
                self.log_textEdit.setText(self.log_items)
                self.log_items += '\n\t'.join(sorted(ShotFinalCheckInst.get_final_not_avid))
                self.log_textEdit.setText(self.log_items)
                self.log_items += '\n\n\tVersions finalled in Avid but not in Shotgun: {}'.format(len(ShotFinalCheckInst.get_final_not_production))
                self.log_textEdit.setText(self.log_items)
                self.log_items += "\n\t".join(sorted(ShotFinalCheckInst.get_final_not_production))
                self.log_textEdit.setText(self.log_items)

            elif self._combobox_items[self.validation_type_comboBox.currentText()] == 2:
                self.log_items += '\nValidation Started for {}...'.format(self.validation_type_comboBox.currentText())
                self.log_textEdit.setText(self.log_items)
                pass
            else:
                self.log_items += '\nInvalid Selection'
                self.log_textEdit.setText(self.log_items)
                return
