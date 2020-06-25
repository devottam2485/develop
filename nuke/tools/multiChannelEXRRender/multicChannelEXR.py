"""
Create exr renders from multiple alpha channel renders

created By: devottam.dutta@technicolor.com
Date: 07-May-2018
"""

import os
import posixpath
import subprocess
import threading

from __ui import multichannel_exr_render_UI
from multiprocessing import Pool
from baler import authoring
from PyQt4 import QtGui
from PyQt4 import QtCore


class multichannel_exr_converter(QtGui.QMainWindow, multichannel_exr_render_UI.Ui_multichannel_exr_render):
    def __init__(self, parent=None):
        """
        Initialize the multichannel_exr_converter Class()
        :param parent:
        """
        super(multichannel_exr_converter, self).__init__()
        self.setupUi(self)
        self.connect_ui()
        print
        "xCC Version 1.2"
        self.setStyleSheet(
            "QMainWindow {background-color: #444444; color: #FFFFFF} QPushButton{background-color: #444444; color: #FFFFFF} QListWidget{background-color: #444444; color: #FFFF00} QLineEdit{background-color: #444444; color: #FFFFFF} QLabel{color: #FFFFFF} QRadioButton{color: #57e6f9} QMessageBox{background-color: #444444; color: #FFFFFF}")

    def connect_ui(self):
        """
        Class object signaling and slotting.
        """
        self.ui_object_switch()
        self.setWindowTitle("XCC")
        self.exr_path_listWidget.setAcceptDrops(True)
        self.local_radioButton.setChecked(True)
        self.browse_pushButton.clicked.connect(self.browse_exr)
        self.renderpath_pushButton.clicked.connect(self.set_render_path)
        self.add_path_pushButton.clicked.connect(self.add_channel_path)
        self.exr_path_lineEdit.textChanged.connect(self.path_validation)
        self.write_lineEdit.textChanged.connect(self.render_path_validation)
        self.reset_pushButton.clicked.connect(self.reset_ui)
        self.remove_pushButton.clicked.connect(self.remove_selected_path)
        self.cancel_pushButton.clicked.connect(self.close_ui)
        self.load_pushButton.clicked.connect(self.load_file)
        self.export_pushButton.clicked.connect(self.export_file)
        self.submit_pushButton.clicked.connect(self.submit_for_render)
        self.nuke_executable = '/X/tools/binlinux/apps/D2Software/Nuke10.0v4/Nuke10.0'
        self.channel_name_list = []

    def ui_object_switch(self, browse=1,
                         line_path=1,
                         first_line=0,
                         channel_line=0,
                         last_line=0,
                         add_path=0,
                         local_radio=0,
                         farm_radio=0,
                         submit_button=0,
                         remove_button=0,
                         reset_button=0,
                         cancel_button=1,
                         write_path=0,
                         renderpath_Button=0):
        """
        UI Object enable/disable switch

        :param browse:
        :param line_path:
        :param first_line:
        :param channel_line:
        :param last_line:
        :param add_path:
        :param local_radio:
        :param farm_radio:
        :param submit_button:
        :param remove_button:
        :param reset_button:
        :param cancel_button:
        :param write_path:
        :param renderpath_Button:
        :return:
        """
        self.browse_pushButton.setEnabled(browse)
        self.exr_path_lineEdit.setEnabled(line_path)
        self.channel_lineEdit.setEnabled(channel_line)
        self.firstframe_lineEdit.setEnabled(first_line)
        self.lastframe_lineEdit.setEnabled(last_line)
        self.add_path_pushButton.setEnabled(add_path)
        self.local_radioButton.setEnabled(local_radio)
        self.farm_radioButton.setEnabled(farm_radio)
        self.submit_pushButton.setEnabled(submit_button)
        self.remove_pushButton.setEnabled(remove_button)
        self.reset_pushButton.setEnabled(reset_button)
        self.cancel_pushButton.setEnabled(cancel_button)
        self.write_lineEdit.setEnabled(write_path)
        self.renderpath_pushButton.setEnabled(renderpath_Button)


def reset_ui(self):
    """
    Reset the UI
    """
    self.exr_path_lineEdit.clear()
    self.exr_path_listWidget.clear()
    self.channel_lineEdit.clear()
    self.firstframe_lineEdit.clear()
    self.lastframe_lineEdit.clear()
    self.write_lineEdit.clear()
    del self.channel_name_list[:]
    self.ui_object_switch()


def close_ui(self):
    """
    Close the UI
    """
    self.close()


def dropEvent(self, event):
    """
    """
    if event.mimeData().hasUrls():
        event.setDropAction(QtCore.Qt.CopyAction)
        event.accept()
        links = []
        for url in event.mimeData().urls():
            links.append(str(url.toLocateFile()))
        self.emit(QtCore.SIGNAL)
    else:
        event.ignore()


def load_file(self):
    """
    """
    load_file_path = str(
        QtGui.QFileDialog.getOpenFileName(self, 'Select text file', '{}'.format(os.path.dirname(__file__)),
                                          "text files (*.txt)"))
    if load_file_path:
        self.load_channel_renders(load_file_path)
    else:
        print("None")


def load_channel_renders(self, file_source=posixpath.join(__file__, 'channel_path_list_text.txt')):
    """
    """

    channel_path_list = []
    if os.path.exists(file_source):
        file_inst = open(file_source, 'r')
        channel_path_list.extend(file_inst.readlines())
        file_inst.close()
    else:
        self.message_box("Path not found")
        return

    self.exr_path_listWidget.clear()
    self.exr_path_listWidget.addItems([path_item.strip() for path_item in channel_path_list])
    self.channel_name_list.extend([(path_item.strip()).split()[-1] for path_item in channel_path_list])
    self.firstframe_lineEdit.setText(channel_path_list[0].split()[-2].split('-')[0])
    self.lastframe_lineEdit.setText(channel_path_list[0].split()[-2].split('-')[-1])
    self.ui_object_switch(1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1)


def export_file(self):
    """
    """
    export_file_path = str(
        QtGui.QFileDialog.getSaveFileName(self, 'export text path', '{}'.format(os.path.dirname(__file__)),
                                          "txt files (*.txt)"))
    if export_file_path:
        self.export_channel_renders(export_file_path)
    else:
        prin("None")


def export_channel_renders(self, export_path=posixpath.join(__file__, 'channel_path_list_text.txt')):
    """
    """
    file_export_inst = open(export_path, 'w')
    for path_item in self.list_path_items():
        file_export_inst.writelines(path_item.strip() + '\n')
    file_export_inst.close()


def browse_exr(self):
    """

    :return:
    """
    browse_path = str(self.exr_path_lineEdit.text())
    if browse_path:
        get_exr_file = str(
            QtGui.QFileDialog.getOpenFileName(self, 'Select a file', '{}'.format(browse_path), "exr files (*.exr)"))
    else:
        get_exr_file = str(QtGui.QFileDialog.getOpenFileName(self, 'Select a file', '/X', "exr files (*.exr)"))

    try:
        self.exr_path_lineEdit.setText(get_exr_file)
    except:
        print("")


def set_render_path(self):
    """

    :return:
    """
    save_path = str(self.write_lineEdit.text())
    if save_path:
        save_exr_file = str(
            QtGui.QFileDialog.getSaveFileName(self, 'Save Render Path', '{}'.format(save_path), "exr files (*.exr)"))
    else:
        save_exr_file = str(QtGui.QFileDialog.getSaveFileName(self, 'Save Render Path', '/X', "exr files (*.exr)"))
    try:
        if save_exr_file.endswith('.exr'):
            exr_split_path = save_exr_file.split('.')
            exr_split_path.insert(-1, '%04d')
            save_exr_file = '.'.join(exr_split_path)
        else:
            save_exr_file = '.'.join([save_exr_file, '%04d', 'exr'])
        self.write_lineEdit.setText(save_exr_file)
    except:
        print("Unable to set path")


def get_custom_range(self, start, end, batch=5):
    """
    """
    temp = 0
    for num in xrange(start, end + 1, batch):
        if temp == num:
            if num + batch >= end:
                yield "{}-{}".format(num + 1, end)
            else:
                yield "{}-{}".format(num + 1, num + batch)
            temp += batch
            if temp >= end:
                break
        else:
            yield "{}-{}".format(num, num + batch)
            temp = num + batch


def list_path_items(self, diff=0):
    """
    Returns the total number of items from the list widget
    :param diff:
    :return: items
    """
    return [str(self.exr_path_listWidget.item(path_item).text()) for path_item in
            range(0, self.exr_path_listWidget.count() - diff)]


def add_channel_path(self):
    """
    Adding the different Roto alpha channel paths into the List widget
    :return:
    """
    chn_path = str(self.exr_path_lineEdit.text())
    first_frame = str(self.firstframe_lineEdit.text())
    last_frame = str(self.lastframe_lineEdit.text())
    channel_name = str(self.channel_lineEdit.text())
    if channel_name in self.channel_name_list:
        self.message_box("Channel Name already Exists...", "Exists Error!")
        return
    else:
        self.channel_name_list.append(channel_name)

    chn_path = str(self.exr_path_lineEdit.text())
    if chn_path:
        if chn_path.endswith('.exr'):
            split_file_path = chn_path.split('.')
            frame_padding = "%0{}d".format(len(split_file_path[-2]))
            split_file_path[-2] = frame_padding
            if not channel_name:
                self.message_box("Invalid Channel Name...", "Invalid!")
                return
            chn_path = ".".join(split_file_path) + " {}-{} {}".format(first_frame, last_frame, channel_name)
        else:
            self.message_box("Not a valid file...", "Invalid!")
            print("Not a valid file")
    else:
        self.message_box("Path not found", "Path Error!")
        return

    if chn_path in self.list_path_items():
        self.message_box("Path Already Exists...", "Exists Error!")
        print("Path Already Exists")
        return

    self.exr_path_listWidget.addItem(chn_path)
    self.ui_object_switch(1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1)


def render_path_validation(self):
    """

    :param self:
    :return:
    """
    write_path = str(self.write_lineEdit.text())
    if os.path.exists(os.path.dirname(write_path)) and write_path.endswith('.exr'):

        self.write_lineEdit.setStyleSheet("color: rgb(0, 255, 0);")
        self.ui_object_switch(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    else:
        self.write_lineEdit.setStyleSheet("color: rgb(100, 0, 0);")
        self.ui_object_switch(1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1)


def path_validation(self):
    """

    :param self:
    :return:
    """
    frame_list = []
    get_path = str(self.exr_path_lineEdit.text())
    if os.path.exists(get_path):
        self.exr_path_lineEdit.setStyleSheet("color: rgb(0, 255, 0);")
        try:
            frame_list.extend([file_item.split('.')[-2] for file_item in os.listdir(os.path.dirname(get_path)) if
                               len(file_item.split('.')) == 3 and file_item.split('.')[-2].isdigit()])
        except:
            frame_list.append(0)
        if self.list_path_items():
            self.ui_object_switch(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        else:
            self.ui_object_switch(1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0)
    else:
        self.exr_path_lineEdit.setStyleSheet("color: rgb(255, 0, 0);")
        if self.list_path_items():
            self.ui_object_switch(1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1)
        else:
            self.ui_object_switch(1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)
    try:
        self.firstframe_lineEdit.setText(min(frame_list))
        self.lastframe_lineEdit.setText(max(frame_list))
    except:
        self.firstframe_lineEdit.setText('None')
        self.lastframe_lineEdit.setText('None')


def remove_selected_path(self):
    """

    :param self:
    :return:
    """
    sel_items = self.exr_path_listWidget.selectedItems()
    if not sel_items:
        print("Selection Error!")
        return
    for item in sel_items:
        self.exr_path_listWidget.takeItem(self.exr_path_listWidget.row(item))
        self.channel_name_list.remove(str(item.text()).split()[-1])


def submit_for_render(self):
    """

    :param self:
    :return:
    """
    nuke_py_converter = "{}/exr_multichannel_render.py".format(os.path.dirname(__file__))
    frame_first = int(self.firstframe_lineEdit.text())
    frame_last = int(self.lastframe_lineEdit.text())
    command_list = []
    try:
        create_nuke_command = '{} -t {} "{}" {}'.format(self.nuke_executable, nuke_py_converter, self.list_path_items(),
                                                        str(self.write_lineEdit.text()))
        subprocess.call(create_nuke_command, shell=True)
        if self.local_radioButton.isChecked():
            print("on local")
            print(self.list_path_items())
            for frame_range in self.get_custom_range(frame_first, frame_last):
                custom_frame_nuke_render_command = "{} -F {} -xi {}".format(self.nuke_executable, frame_range,
                                                                            posixpath.join(os.path.dirname(
                                                                                str(self.write_lineEdit.text())),
                                                                                           'multichannel_nuke_render.nk'))
                command_list.append(custom_frame_nuke_render_command)
                print("\ncommand_list", command_list)
            app_thread(command_list).start()
        elif self.farm_radioButton.isChecked():
            print("on farm")
            nuke_file = posixpath.join(os.path.dirname(str(self.write_lineEdit.text())), 'multichannel_nuke_render.nk')
            show_name = os.getenv('SHOW', None)
            shot_name = os.getenv('SHOT', None)
            job_name = os.path.basename(str(self.write_lineEdit.text())).split('.')[0]

            if show_name == None:
                show_name = 'testing'
            if shot_name == None:
                shot_name = '_default'
            print(show_name, shot_name, job_name)

            get_job = authoring.init_job(job_name, show=show_name,
                                         shot=shot_name)  # , licenses='foundry_LICENSE=4101@10.108.4.115')
            get_job.envkey = ['xenv foundry_LICENSE=4101@10.108.4.115']
            for range_item in self.get_custom_range(1016, 1255):
                nuke_task = get_job.newTask(title='Frame range {}'.format(range_item))
                nuke_task.newCommand(argv=[self.nuke_executable, '-F', range_item, '-xi', nuke_file])
                get_job.addChild(nuke_task)
            nuke_submit_id = get_job.spool()
            self.message_box("Submitted Job id: {}".format(nuke_submit_id), 'Done!')
        else:
            print("Invalid Selection")
    except:
        print("Submission Error!")


def message_box(self, message, title):
    """

    :param self:
    :param message:
    :param title:
    :return:
    """
    msg = QtGui.QMessageBox(self)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec_()


class app_thread(threading.Thread):
    def __init__(self, command_path):
        """
        """
        threading.Thread.__init__(self)
        self.command_path = command_path
        self.total_process = 4

    def run(self):
        """
        """
        process_inst = Pool(processes=self.total_process)
        process_inst.map(os.system, self.command_path)


def main():
    """

    :return:
    """
    import sys
    app = QtGui.QApplication(sys.argv)
    buildapp = multichannel_exr_converter()
    buildapp.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

