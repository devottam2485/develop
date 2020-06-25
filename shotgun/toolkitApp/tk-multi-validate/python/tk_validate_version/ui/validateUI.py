# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\git_repo\tk-multi-validate\resources\validate.ui'
#
# Created: Fri Oct 11 02:20:03 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(698, 846)
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.setFont(font)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtGui.QFrame(Form)
        self.frame.setEnabled(True)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.drop_area_label = DropAreaLabel(self.frame)
        self.drop_area_label.setObjectName("drop_area_label")
        self.gridLayout_2.addWidget(self.drop_area_label, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.shot_final_checkBox = QtGui.QCheckBox(self.frame)
        self.shot_final_checkBox.setObjectName("shot_final_checkBox")
        self.verticalLayout_2.addWidget(self.shot_final_checkBox)
        self.line_2 = QtGui.QFrame(self.frame)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setMidLineWidth(0)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.send_di_checkBox = QtGui.QCheckBox(self.frame)
        self.send_di_checkBox.setObjectName("send_di_checkBox")
        self.verticalLayout_2.addWidget(self.send_di_checkBox)
        self.di_final_radioButton = QtGui.QRadioButton(self.frame)
        self.di_final_radioButton.setObjectName("di_final_radioButton")
        self.verticalLayout_2.addWidget(self.di_final_radioButton)
        self.di_temp_radioButton = QtGui.QRadioButton(self.frame)
        self.di_temp_radioButton.setObjectName("di_temp_radioButton")
        self.verticalLayout_2.addWidget(self.di_temp_radioButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.validate_pushButton = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.validate_pushButton.sizePolicy().hasHeightForWidth())
        self.validate_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.validate_pushButton.setFont(font)
        self.validate_pushButton.setObjectName("validate_pushButton")
        self.horizontalLayout_2.addWidget(self.validate_pushButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 3, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.debug_log_checkBox = QtGui.QCheckBox(Form)
        self.debug_log_checkBox.setObjectName("debug_log_checkBox")
        self.horizontalLayout_3.addWidget(self.debug_log_checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.log_textEdit = QtGui.QTextEdit(Form)
        self.log_textEdit.setObjectName("log_textEdit")
        self.verticalLayout.addWidget(self.log_textEdit)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.close_pushButton = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_pushButton.sizePolicy().hasHeightForWidth())
        self.close_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.close_pushButton.setFont(font)
        self.close_pushButton.setObjectName("close_pushButton")
        self.horizontalLayout.addWidget(self.close_pushButton)
        self.reset_pushButton = QtGui.QPushButton(Form)
        self.reset_pushButton.setObjectName("reset_pushButton")
        self.horizontalLayout.addWidget(self.reset_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 4, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.drop_area_label.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-style:italic;\">Drop EDL and TXT files here</span></p><p align=\"center\"><img src=\":/media/txt-icon.png\"/><img src=\":/media/edl_file.png\"/></p><p><span style=\" font-weight:600; font-style:italic;\"><br/></span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_final_checkBox.setText(QtGui.QApplication.translate("Form", "Shot Final Check", None, QtGui.QApplication.UnicodeUTF8))
        self.send_di_checkBox.setText(QtGui.QApplication.translate("Form", "Version Send DI Check", None, QtGui.QApplication.UnicodeUTF8))
        self.di_final_radioButton.setText(QtGui.QApplication.translate("Form", "DI Final (default)", None, QtGui.QApplication.UnicodeUTF8))
        self.di_temp_radioButton.setText(QtGui.QApplication.translate("Form", "DI Temp", None, QtGui.QApplication.UnicodeUTF8))
        self.validate_pushButton.setText(QtGui.QApplication.translate("Form", "validate", None, QtGui.QApplication.UnicodeUTF8))
        self.debug_log_checkBox.setText(QtGui.QApplication.translate("Form", "Debug Log", None, QtGui.QApplication.UnicodeUTF8))
        self.log_textEdit.setHtml(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Results</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.close_pushButton.setText(QtGui.QApplication.translate("Form", "close", None, QtGui.QApplication.UnicodeUTF8))
        self.reset_pushButton.setText(QtGui.QApplication.translate("Form", "reset", None, QtGui.QApplication.UnicodeUTF8))

from ..validate_drop_area import DropAreaLabel
import resources_rc


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

