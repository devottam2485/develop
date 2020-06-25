import os
import sys

maya_python_path = ['/X/tools/python/3rd_party/linux_python2.7', '/X/tools/binlinux/aw/maya2016.5/lib/python2.7/site-packages']

sys.path.extend([path_item for path_item in maya_python_path if path_item not in sys.path])

import maya.cmds as mc
import pymel.core as pm

from PySide import QtGui
from PySide import QtCore
from __ui import xVrayAttrSwitchUi

class x_Vray_attr(QtGui.QMainWindow, xVrayAttrSwitchUi.Ui_MainWindow):
    def __init__(self):
        """

        """
        super(x_Vray_attr, self).__init__()
        self.setupUi(self)
        self.resize(1200, 374)
        self.connect_ui()

    def connect_ui(self):
        """

        :return:
        """
        self.generate_shapes_table()
        self.attr_pushButton.clicked.connect(self.open_attribute_spread_sheet)
        self.reload_pushButton.clicked.connect(self.reset_ui_switch)
        self.close_pushButton.clicked.connect(self.close_ui)
        self.subdiv_checkBox.clicked.connect(self.get_selected_table_data)
        self.subquality_checkBox.clicked.connect(self.get_selected_table_data)
        self.displacement_checkBox.clicked.connect(self.get_selected_table_data)
        self.opensubdiv_checkBox.clicked.connect(self.get_selected_table_data)
        self.roundedges_checkBox.clicked.connect(self.get_selected_table_data)
        self.userattr_checkBox.clicked.connect(self.get_selected_table_data)
        self.objectid_checkBox.clicked.connect(self.get_selected_table_data)
        self.fogfadeout_checkBox.clicked.connect(self.get_selected_table_data)
        self.localrayserver_checkBox.clicked.connect(self.get_selected_table_data)
        self.object_id_lineEdit.textChanged.connect(self.set_vray_object_id)
        self.object_id_lineEdit.setText('0')


    def reset_ui_switch(self):
        """

        :return:
        """
        self.subdiv_checkBox.setChecked(False)
        self.subquality_checkBox.setChecked(False)
        self.displacement_checkBox.setChecked(False)
        self.opensubdiv_checkBox.setChecked(False)
        self.roundedges_checkBox.setChecked(False)
        self.userattr_checkBox.setChecked(False)
        self.objectid_checkBox.setChecked(False)
        self.fogfadeout_checkBox.setChecked(False)
        self.localrayserver_checkBox.setChecked(False)
        self.object_id_lineEdit.clear()
        self.object_id_lineEdit.setText('0')
        self.generate_shapes_table()


    def open_attribute_spread_sheet(self):
        """

        :return:
        """
        import maya.mel as mel

        mel.eval('SpreadSheetEditor;')
        mel.eval('SpreadSheetWindow;')

    def close_ui(self):
        self.close()

    def get_selected_shapes(self):
        """

        :return:
        """
        return [shape_item.name() for shape_item in pm.ls(selection=True, shapes=True)]

    def load_shapes_scene(self):
        """

        :return:
        """
        all_descendents = pm.listRelatives(allDescendents=True, shapes=True)
        for descendent_item in all_descendents:
            if descendent_item.nodeType() == 'mesh':
                pm.select(descendent_item, add=True)
            else:
                continue
    def vray_attributes_exists(self, shape_obj):
            """

            :param shape_obj:
            :return:
            """
            return (pm.attributeQuery('vraySeparator_vray_subdivision', node=shape_obj, exists=True),
                    pm.attributeQuery('vraySeparator_vray_subquality', node=shape_obj, exists=True),
                    pm.attributeQuery('vraySeparator_vray_displacement', node=shape_obj, exists=True),
                    pm.attributeQuery('vraySeparator_vray_opensubdiv', node=shape_obj, exists=True),
                    pm.attributeQuery('vraySeparator_vray_roundedges', node=shape_obj, exists=True),
                    pm.attributeQuery('vraySeparator_vray_user_attributes', node=shape_obj, exists=True),
                    pm.attributeQuery('vraySeparator_vray_objectID', node=shape_obj, exists=True),
                    pm.attributeQuery('vraySeparator_vray_fogFadeOut', node=shape_obj, exists=True),
                    pm.attributeQuery('vraySeparator_vray_localrayserver', node=shape_obj, exists=True))

    def vray_attributes_get(self, shape_Obj):
        """

        :param shape_Obj:
        :return:
        """
        try:
            return mc.getAttr("{}.vrayObjectID".format(shape_Obj))
        except:
            return 0

    def generate_shapes_table(self):
        """

        :return:
        """
        self.vrayattr_tableWidget.setColumnCount(10)
        self.vrayattr_tableWidget.setHorizontalHeaderLabels(("Subdivision", "Subdivision and Displacement Quality",
                                                             "Displacement Control", "OpenSubdiv", "Round Edges",
                                                             "User Attributes", "Object ID", "Object_ID_Value", "Fog Fade out Radius",
                                                             "Local Ray Server"))
        self.vrayattr_tableWidget.resizeColumnsToContents()
        self.load_shapes_scene()
        selected_shapes = self.get_selected_shapes()
        green_color = QtGui.QColor(0, 255, 0)
        if selected_shapes:
            self.vrayattr_tableWidget.setRowCount(len(selected_shapes))
            for index_val in range(0, len(selected_shapes)):
                self.vrayattr_tableWidget.setVerticalHeaderItem(index_val,
                                                                QtGui.QTableWidgetItem(selected_shapes[index_val]))

                sub_div_val = QtGui.QTableWidgetItem(str(self.vray_attributes_exists(selected_shapes[index_val])[0]))
                if sub_div_val.text() == 'True':
                    sub_div_val.setForeground(green_color)
                self.vrayattr_tableWidget.setItem(index_val, 0, sub_div_val)

                sub_qual_val = QtGui.QTableWidgetItem(str(self.vray_attributes_exists(selected_shapes[index_val])[1]))
                if sub_qual_val.text() == 'True':
                    sub_qual_val.setForeground(green_color)
                self.vrayattr_tableWidget.setItem(index_val, 1, sub_qual_val)

                dplcement_val = QtGui.QTableWidgetItem(str(self.vray_attributes_exists(selected_shapes[index_val])[2]))
                if dplcement_val.text() == 'True':
                    dplcement_val.setForeground(green_color)
                self.vrayattr_tableWidget.setItem(index_val, 2, dplcement_val)

                opnsubdiv_val = QtGui.QTableWidgetItem(str(self.vray_attributes_exists(selected_shapes[index_val])[3]))
                if opnsubdiv_val.text() == 'True':
                    opnsubdiv_val.setForeground(green_color)
                self.vrayattr_tableWidget.setItem(index_val, 3, opnsubdiv_val)
                rndedge_val = QtGui.QTableWidgetItem(str(self.vray_attributes_exists(selected_shapes[index_val])[4]))
                if rndedge_val.text() == 'True':
                    rndedge_val.setForeground(green_color)
                self.vrayattr_tableWidget.setItem(index_val, 4, rndedge_val)

                usrattr_val = QtGui.QTableWidgetItem(str(self.vray_attributes_exists(selected_shapes[index_val])[5]))
                if usrattr_val.text() == 'True':
                    usrattr_val.setForeground(green_color)
                self.vrayattr_tableWidget.setItem(index_val, 5, usrattr_val)

                objid_val = QtGui.QTableWidgetItem(str(self.vray_attributes_exists(selected_shapes[index_val])[6]))
                if objid_val.text() == 'True':
                    objid_val.setForeground(green_color)
                self.vrayattr_tableWidget.setItem(index_val, 6, objid_val)

                get_objid_val = QtGui.QTableWidgetItem(str(self.vray_attributes_get(selected_shapes[index_val])))
                self.vrayattr_tableWidget.setItem(index_val, 7, get_objid_val)

                fg_fd_val = QtGui.QTableWidgetItem(str(self.vray_attributes_exists(selected_shapes[index_val])[7]))
                if fg_fd_val.text() == 'True':
                    fg_fd_val.setForeground(green_color)
                self.vrayattr_tableWidget.setItem(index_val, 8, fg_fd_val)

                loc_val = QtGui.QTableWidgetItem(str(self.vray_attributes_exists(selected_shapes[index_val])[8]))
                if loc_val.text() == 'True':
                    loc_val.setForeground(green_color)
                self.vrayattr_tableWidget.setItem(index_val, 9, loc_val)
        else:
            print "No shape/mesh object found"

        self.vrayattr_tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)


    def set_vray_object_id(self):
            """

            :return:
            """
            id_val = str(self.object_id_lineEdit.text())
            if len(id_val) == 3:
                self.object_id_lineEdit.clear()
                self.object_id_lineEdit.setText(id_val[:-1])
                return
            if len(id_val) == 2:
                if ord(id_val[-1]) not in range(48, 58):
                    self.object_id_lineEdit.clear()
                    self.object_id_lineEdit.setText('0')
                    return
                if int(id_val[0]) > 1:
                    self.object_id_lineEdit.setText(id_val[0])
                else:
                    if int(id_val[-1]) > 5:
                        self.object_id_lineEdit.setText(id_val[:-1])
            else:
                if not ord(id_val) in range(48, 58):
                    self.object_id_lineEdit.clear()
                    self.object_id_lineEdit.setText('0')
                    return
            selected_cell_items = self.vrayattr_tableWidget.selectedItems()
            if not selected_cell_items:
                print "Found no selection"
                return
            for sel_cell_item in selected_cell_items:
                shape_item = self.vrayattr_tableWidget.verticalHeaderItem(sel_cell_item.row()).text()
                try:
                    mc.setAttr("{}.vrayObjectID".format(shape_item), int(self.object_id_lineEdit.text()))
                except:
                    raise AttributeError
    self.generate_shapes_table()
    def get_selected_table_data(self):
            """

            :return:
            """
            selected_cell_items = self.vrayattr_tableWidget.selectedItems()
            if not selected_cell_items:
                print "Found no selection"
                return
            for sel_cell_item in selected_cell_items:
                shape_item = self.vrayattr_tableWidget.verticalHeaderItem(sel_cell_item.row()).text()
                vray_attr_item = self.vrayattr_tableWidget.horizontalHeaderItem(sel_cell_item.column()).text()
                self.toggle_vray_attr_shapes(shape_item, vray_attr_item)

            self.generate_shapes_table()

    def toggle_vray_attr_shapes(self, shape_name, attribute_name):
        """

        :param shape_name:
        :param attribute_name:
        :return:
        """
        if attribute_name == 'Subdivision':
            if self.subdiv_checkBox.isChecked():
                mc.vray("addAttributesFromGroup", shape_name, "vray_subdivision", 1)
            else:
                mc.vray("addAttributesFromGroup", shape_name, "vray_subdivision", 0)

        elif attribute_name == 'Subdivision and Displacement Quality':
            if self.subquality_checkBox.isChecked():
                mc.vray("addAttributesFromGroup", shape_name, "vray_subquality", 1)
            else:
                mc.vray("addAttributesFromGroup", shape_name, "vray_subquality", 0)

        elif attribute_name == 'Displacement Control':
            if self.displacement_checkBox.isChecked():
                mc.vray("addAttributesFromGroup", shape_name, "vray_displacement", 1)
            else:
                mc.vray("addAttributesFromGroup", shape_name, "vray_displacement", 0)

        elif attribute_name == 'OpenSubdiv':
            if self.opensubdiv_checkBox.isChecked():
                mc.vray("addAttributesFromGroup", shape_name, "vray_opensubdiv", 1)
            else:
                mc.vray("addAttributesFromGroup", shape_name, "vray_opensubdiv", 0)
        elif attribute_name == 'Round Edges':
            if self.roundedges_checkBox.isChecked():
                mc.vray("addAttributesFromGroup", shape_name, "vray_roundedges", 1)
            else:
                mc.vray("addAttributesFromGroup", shape_name, "vray_roundedges", 0)

        elif attribute_name == 'User Attributes':
            if self.userattr_checkBox.isChecked():
                mc.vray("addAttributesFromGroup", shape_name, "vray_user_attributes", 1)
            else:
                mc.vray("addAttributesFromGroup", shape_name, "vray_user_attributes", 0)

        elif attribute_name == 'Object ID':
            if self.objectid_checkBox.isChecked():
                mc.vray("addAttributesFromGroup", shape_name, "vray_objectID", 1)
            else:
                mc.vray("addAttributesFromGroup", shape_name, "vray_objectID", 0)
                self.object_id_lineEdit.setText('0')

        elif attribute_name == 'Fog Fade out Radius':
            if self.fogfadeout_checkBox.isChecked():
                mc.vray("addAttributesFromGroup", shape_name, "vray_fogFadeOut", 1)
            else:
                mc.vray("addAttributesFromGroup", shape_name, "vray_fogFadeOut", 0)

        elif attribute_name == 'Local Ray Server':
            if self.localrayserver_checkBox.isChecked():
                mc.vray("addAttributesFromGroup", shape_name, "vray_localrayserver", 1)
            else:
                mc.vray("addAttributesFromGroup", shape_name, "vray_localrayserver", 0)

        else:
            "Not a valid Attribute"


def main():
    """

    :return:
    """
    app = QtGui.QApplication(sys.argv)
    buildapp = x_Vray_attr()
    buildapp.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

