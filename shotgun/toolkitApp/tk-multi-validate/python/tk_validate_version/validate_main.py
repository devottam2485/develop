import sgtk
import sys
import re
import os
import posixpath
import logging

from sgtk.platform import Application
from sgtk.platform.qt import QtCore, QtGui
from .ui import validateUI
from validate_drop_area import DropAreaLabel
from shot_final_check import ShotFinalCheck
from version_di_check import ValidateDiCheck
import time

edl = sgtk.platform.import_framework("tk-framework-editorial", "edl")
_valid_ext = ['.edl', '.txt']
_file_data_list = []
_di_final = True
_completed = True

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


class ThreadWorker(QtCore.QObject):
    process_log = QtCore.Signal(str)
    process_debug_log = QtCore.Signal(str)
    process_finished = QtCore.Signal()
    edl_error = QtCore.Signal(str, str)

    @QtCore.Slot()
    def process_data(self):
        """

        :param file_path:
        :return:
        """
        global _completed
        log_str = ''
        log_str1 = '\nPlease Wait...'
        self.process_log.emit(log_str1)
        for path_item in _file_data_list:
            log_str1 += '\nProcessing Started: {}'.format(path_item)
            self.process_log.emit(log_str1)
            if path_item.endswith('.txt'):
                ShotFinalCheckInst = ShotFinalCheck()
                self.process_debug_log.emit(ShotFinalCheckInst.final_check_log)
                ShotFinalCheckInst.process_file_data(path_item)
                self.process_debug_log.emit(ShotFinalCheckInst.final_check_log)
                ShotFinalCheckInst.process_final_check(ShotFinalCheckInst.get_final_avid)
                self.process_debug_log.emit(ShotFinalCheckInst.final_check_log)

                log_str += '\n\n\t\t{0} Shot Final Report {0}'.format('*' * 15)
                self.process_log.emit(log_str)
                log_str += '\n\n\tVersions missing from .txt but "Final" in Shotgun: {}'.format(len(ShotFinalCheckInst.get_final_not_avid))
                self.process_log.emit(log_str)
                log_str += '\n\t{}'.format('\n\t'.join(sorted(ShotFinalCheckInst.get_final_not_avid)))
                self.process_log.emit(log_str)
                log_str += '\n\n\tVersions from .txt which are not "Final" in Shotgun: {}'.format(len(ShotFinalCheckInst.get_final_not_production))
                self.process_log.emit(log_str)
                log_str += '\n\t{}'.format("\n\t".join(sorted(ShotFinalCheckInst.get_final_not_production)))
                self.process_log.emit(log_str)
            elif path_item.endswith('.edl'):
                ValidateDiCheckInst = ValidateDiCheck(di_final=_di_final)
                self.process_debug_log.emit(ValidateDiCheckInst.di_check_log)
                check_status, error_log = ValidateDiCheckInst.process_edl_file_data(path_item)
                self.process_debug_log.emit(ValidateDiCheckInst.di_check_log)
                if check_status:
                    ValidateDiCheckInst.process_shotgun_version_field()
                    self.process_debug_log.emit(ValidateDiCheckInst.di_check_log)
                    ValidateDiCheckInst.process_version_di_edl_check()
                    self.process_debug_log.emit(ValidateDiCheckInst.di_check_log)
                    ValidateDiCheckInst.process_shotgun_di_status_check()
                    self.process_debug_log.emit(ValidateDiCheckInst.di_check_log)

                    log_str += '\n\n\t\t{0} Version Sent DI Report {0}'.format('*' * 15)
                    self.process_log.emit(log_str)
                    if ValidateDiCheckInst.get_edl_version_not_in_shotgun:
                        log_str += '\n\n\tThese Shotgun Versions are in the EDL but not in Shotgun: \n\t{}\n'.format('\n\t'.join(ValidateDiCheckInst.get_edl_version_not_in_shotgun))
                        self.process_log.emit(log_str)
                    if ValidateDiCheckInst.get_edl_shotgun_version_not_di_status:
                        log_str += '\n\n\tThese Shotgun Versions are not set to {}: \n\t{}\n'.format(ValidateDiCheckInst.di_status, '\n\t'.join(ValidateDiCheckInst.get_edl_shotgun_version_not_di_status))
                        self.process_log.emit(log_str)
                    else:
                        log_str += '\n\n\tAll Versions in this EDL are set to {} \n\t{}\n'.format(ValidateDiCheckInst.di_status, '\n\t'.join(ValidateDiCheckInst.get_edl_version_list))
                        self.process_log.emit(log_str)
                    if ValidateDiCheckInst.get_shotgun_version_di_status_not_in_edl:
                        log_str += '\n\n\tThese Shotgun Versions are in Reel {} and set to {} but not in the EDL: \n\t{}\n'.format(ValidateDiCheckInst.get_reel_name, ValidateDiCheckInst.di_status, '\n\t'.join(ValidateDiCheckInst.get_shotgun_version_di_status_not_in_edl))
                        self.process_log.emit(log_str)
                    else:
                        log_str += '\n\n\tAll Versions in Reel {} which are set to {} are in this EDL\n'.format(
                            ValidateDiCheckInst.get_reel_name, ValidateDiCheckInst.di_status)
                        self.process_log.emit(log_str)
                else:
                    log_str += '\nEDL File Parsing Error\n{}'.format(error_log)
                    _completed = False
                    self.process_log.emit(log_str)
                    self.edl_error.emit('Error!', '{}'.format(error_log))

        self.process_finished.emit()


class ValidateVersion(QtGui.QWidget, validateUI.Ui_Form):

    list_path = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(ValidateVersion, self).__init__()
        self._logging = logging.getLogger('Validate')
        self._logging.info("INFO: Initialized class {}".format(self.__class__))
        self.setupUi(self)

        # Getting the Thread Class
        self.thread = QtCore.QThread()
        # Making Thread object
        self.thread_obj = ThreadWorker()

        self._app = sgtk.platform.current_bundle()
        self._ctx = self._app.context
        self.ui_reset()
        # Signals and Slotting
        self.ui_connect()

    def ui_connect(self):
        """

        :return:
        """
        self.thread_obj.process_log.connect(self.set_log_text)
        self.thread_obj.process_debug_log.connect(self.set_debug_log_text)
        self.thread_obj.edl_error.connect(self.show_message_info)
        self.thread_obj.moveToThread(self.thread)
        self.thread_obj.process_finished.connect(self.complete_validation)
        self.thread.started.connect(self.thread_obj.process_data)
        self.drop_area_label.something_dropped.connect(self.initialize_validation)
        self.drop_area_label.set_restrict_to_ext(_valid_ext)
        self.validate_pushButton.clicked.connect(self.process_validation)
        self.shot_final_checkBox.clicked.connect(self.checkbox_state_change)
        self.send_di_checkBox.clicked.connect(self.checkbox_state_change)
        self.reset_pushButton.clicked.connect(self.ui_reset)
        self.close_pushButton.clicked.connect(self.close_ui)
        self.label_font = QtGui.QFont()

    def close_ui(self):
        """

        :return:
        """
        result = self.show_message_info('Warning!', 'are you sure?', error_type='warning')
        if result == 16384:
            self.close()

    def ui_reset(self):
        """

        :return:
        """
        self.log_items = ''
        global _file_data_list
        global _di_final
        global _completed
        _completed = True
        _di_final = True
        _file_data_list = []
        self._edl = []
        self.log_textEdit.clear()
        self.shot_final_checkBox.setChecked(False)
        self.send_di_checkBox.setChecked(False)
        self.di_final_radioButton.setEnabled(False)
        self.di_final_radioButton.setChecked(True)
        self.di_temp_radioButton.setEnabled(False)
        self.di_temp_radioButton.setChecked(False)
        self.ui_switch(0, 1, 1)
        self.log_textEdit.setText('Results')

    def ui_switch(self, validate, send_di, shot_final):
        """

        :param validate:
        :param validation_type:
        :return:
        """
        self.validate_pushButton.setEnabled(validate)
        self.send_di_checkBox.setEnabled(send_di)
        self.shot_final_checkBox.setEnabled(shot_final)

    def show_message_info(self, title, message, error_type='critical'):
        """

        :param title:
        :param message:
        :param type:
        :return:
        """
        msg = QtGui.QMessageBox()
        if error_type == 'warning':
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText(message)
            msg.setWindowTitle(title)
            msg.setStandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        elif error_type == 'information':
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText(message)
            msg.setWindowTitle(title)
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
        elif error_type == 'critical':
            msg.setIcon(QtGui.QMessageBox.Critical)
            msg.setText(message)
            msg.setWindowTitle(title)
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
        retval = msg.exec_()
        return retval

    def checkbox_state_change(self):
        if self.shot_final_checkBox.isChecked() or self.send_di_checkBox.isChecked():
            if _file_data_list:
                self.ui_switch(1, 1, 1)
            else:
                self.ui_switch(0, 1, 1)
        else:
            self.ui_switch(0, 1, 1)

    def selection_change(self, file_name):
        """

        :param file_name:
        :return:
        """
        global _di_final
        if file_name.endswith('.txt'):
            self.shot_final_checkBox.setChecked(True)
        elif file_name.endswith('.edl'):
            self.send_di_checkBox.setChecked(True)
            if 'temp' in file_name.lower():
                self.di_temp_radioButton.setChecked(True)
                _di_final = False
            if 'final' in file_name.lower():
                self.di_final_radioButton.setChecked(True)
                _di_final = True
            else:
                pass
        else:
            pass

    @QtCore.Slot(str)
    def set_log_text(self, txt):
        """

        :param txt:
        :return:
        """
        if not self.debug_log_checkBox.isChecked():
            self.log_textEdit.setText(txt)

    @QtCore.Slot(str)
    def set_debug_log_text(self, txt):
        """

        :param txt:
        :return:
        """
        if self.debug_log_checkBox.isChecked():
            self.log_textEdit.setText(txt)

    @QtCore.Slot(list)
    def initialize_validation(self, paths):
        """

        :return:
        """
        global _file_data_list
        if _file_data_list:
            QtGui.QMessageBox.warning(
                self,
                "Can't process drop",
                "Validation is already in progress!\nPlease reset the app for new calculations.",
            )
            return
        num_paths = len(paths)
        if num_paths > 1:
            QtGui.QMessageBox.warning(
                self,
                "Can't process drop",
                "Please drop maximum of 1 file at a time (EDL or TXT).",
            )
            return
        self.log_items = '\nValidation Ready to Start...'
        self.log_textEdit.setText(self.log_items)
        path = paths[0].encode("utf-8")
        _, ext = os.path.splitext(path)
        _file_data_list.append(path)
        self.selection_change(path)
        self.ui_switch(1, 0, 0)

        if num_paths == 2:
            path = paths[1].encode("utf-8")
            _, ext_2 = os.path.splitext(path)
            if ext_2.lower() == ext.lower():
                self._logger.error(
                    "An EDL file and a movie should be dropped, not two %s files." % (
                        ext[1:],
                    ))
                return
            _file_data_list.append(path)
            self.selection_change(path)
            self.ui_switch(1, 0, 0)
        for path_item in _file_data_list:
            self.log_items += "\n->{}".format(path_item)
            self.log_textEdit.setText(self.log_items)

    def process_validation(self):
        """

        :return:
        """
        self.thread.start()
        self.ui_switch(0, 0, 0)

    def complete_validation(self):
        """

        :return:
        """
        self.thread.quit()
        if _completed:
            self.show_message_info(title='Done', message='Successfully Completed', error_type='information')

