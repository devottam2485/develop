from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1377, 384)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.vrayattr_tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.vrayattr_tableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.vrayattr_tableWidget.setObjectName(_fromUtf8("vrayattr_tableWidget"))
        self.vrayattr_tableWidget.setColumnCount(2)
        self.vrayattr_tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.vrayattr_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.vrayattr_tableWidget.setHorizontalHeaderItem(1, item)
        self.horizontalLayout.addWidget(self.vrayattr_tableWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.subdiv_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.subdiv_checkBox.setObjectName(_fromUtf8("subdiv_checkBox"))
        self.verticalLayout.addWidget(self.subdiv_checkBox)
        self.subquality_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.subquality_checkBox.setObjectName(_fromUtf8("subquality_checkBox"))


self.verticalLayout.addWidget(self.subquality_checkBox)
        self.displacement_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.displacement_checkBox.setObjectName(_fromUtf8("displacement_checkBox"))
        self.verticalLayout.addWidget(self.displacement_checkBox)
        self.opensubdiv_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.opensubdiv_checkBox.setObjectName(_fromUtf8("opensubdiv_checkBox"))
        self.verticalLayout.addWidget(self.opensubdiv_checkBox)
        self.roundedges_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.roundedges_checkBox.setObjectName(_fromUtf8("roundedges_checkBox"))
        self.verticalLayout.addWidget(self.roundedges_checkBox)
        self.userattr_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.userattr_checkBox.setObjectName(_fromUtf8("userattr_checkBox"))
        self.verticalLayout.addWidget(self.userattr_checkBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.objectid_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.objectid_checkBox.setObjectName(_fromUtf8("objectid_checkBox"))
        self.horizontalLayout_2.addWidget(self.objectid_checkBox)
        self.object_id_lineEdit = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.object_id_lineEdit.sizePolicy().hasHeightForWidth())
        self.object_id_lineEdit.setSizePolicy(sizePolicy)
        self.object_id_lineEdit.setInputMask(_fromUtf8(""))
        self.object_id_lineEdit.setText(_fromUtf8(""))
        self.object_id_lineEdit.setObjectName(_fromUtf8("object_id_lineEdit"))
        self.horizontalLayout_2.addWidget(self.object_id_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.fogfadeout_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.fogfadeout_checkBox.setObjectName(_fromUtf8("fogfadeout_checkBox"))
        self.verticalLayout.addWidget(self.fogfadeout_checkBox)
        self.localrayserver_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.localrayserver_checkBox.setObjectName(_fromUtf8("localrayserver_checkBox"))
        self.verticalLayout.addWidget(self.localrayserver_checkBox)
        self.attr_pushButton = QtGui.QPushButton(self.centralwidget)
        self.attr_pushButton.setObjectName(_fromUtf8("attr_pushButton"))


self.verticalLayout.addWidget(self.attr_pushButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.reload_pushButton = QtGui.QPushButton(self.centralwidget)
        self.reload_pushButton.setObjectName(_fromUtf8("reload_pushButton"))
        self.verticalLayout.addWidget(self.reload_pushButton)
        self.close_pushButton = QtGui.QPushButton(self.centralwidget)
        self.close_pushButton.setObjectName(_fromUtf8("close_pushButton"))
        self.verticalLayout.addWidget(self.close_pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "X Vray Attributes", None))
        item = self.vrayattr_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column", None))
        item = self.vrayattr_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column", None))
        self.subdiv_checkBox.setText(_translate("MainWindow", "Subdivision", None))
        self.subquality_checkBox.setText(_translate("MainWindow", "Subquality", None))
        self.displacement_checkBox.setText(_translate("MainWindow", "Displacement", None))
        self.opensubdiv_checkBox.setText(_translate("MainWindow", "OpenSubdiv", None))
        self.roundedges_checkBox.setText(_translate("MainWindow", "Round Edges", None))
        self.userattr_checkBox.setText(_translate("MainWindow", "User Attributes", None))
        self.objectid_checkBox.setText(_translate("MainWindow", "Object ID", None))
        self.fogfadeout_checkBox.setText(_translate("MainWindow", "Fog fade out radius", None))
        self.localrayserver_checkBox.setText(_translate("MainWindow", "Local ray server", None))
        self.attr_pushButton.setText(_translate("MainWindow", "Attribute Spread Sheet", None))
        self.reload_pushButton.setText(_translate("MainWindow", "reload ", None))
        self.close_pushButton.setText(_translate("MainWindow", "close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())