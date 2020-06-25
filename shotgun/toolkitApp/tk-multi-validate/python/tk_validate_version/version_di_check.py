import sgtk
import os
import logging

edl = sgtk.platform.import_framework("tk-framework-editorial", "edl")

class ValidateDiCheck(object):
    def __init__(self, di_final=True):
        super(ValidateDiCheck, self).__init__()
        self._di_check_logging = logging.getLogger('ValidateDiCheck')
        self.di_check_log = '\n<--------------------Version di edl check log Starts here-------------------->'
        self._reel_name = None
        self._shotgun_version_dict = {}
        self._edl_version_list = []
        self._valid_edl_di_shotgun = []
        self._invalid_edl_di_shotgun = []
        self._edl_not_in_shotgun = []
        self._shotgun_version_di_not_in_edl = []
        self._shotgun_version_list = []
        self._sg = sgtk.util.shotgun.create_sg_connection()
        self._project = sgtk.platform.current_bundle().context.project
        if di_final:
            self.di_status = 'Sent to DI Final'
        else:
            self.di_status = 'Sent to DI Temp'
        self.di_check_log += '\nDI Status: {}'.format(self.di_status)
        self._fields = ['sg_edit_di_status', 'code']

    @property
    def get_edl_version_list(self):
        """

        :return:
        """
        return self._edl_version_list

    @property
    def get_edl_version_not_in_shotgun(self):
        """

        :return:
        """
        return self._edl_not_in_shotgun

    @property
    def get_edl_shotgun_version_not_di_status(self):
        """

        :return:
        """
        return self._invalid_edl_di_shotgun

    @property
    def get_shotgun_version_di_status_not_in_edl(self):
        """

        :return:
        """
        return self._shotgun_version_di_not_in_edl

    @property
    def get_reel_name(self):
        """

        :return:
        """
        return self._reel_name

    @property
    def get_shotgun_version_list(self):
        """

        :return:
        """
        return self._shotgun_version_list

    def process_shotgun_version_field(self):
        """

        :return:
        """
        # ['sg_status_list', 'is', 'final'],
        self.di_check_log += "\nShotgun API call for Querying Version..."
        self._di_check_logging.info("\nShotgun API call for Querying Version...")
        reel_dict = {}
        if self._reel_name:
            reel_dict = self._sg.find_one('Reel', [['project', 'is', self._project], ['code', 'is', self._reel_name]], ['code'])
            self.di_check_log += '\nReel Dict: {}'.format(reel_dict)
        if reel_dict:
            sg_filter = [['project', 'is', self._project],
                         ['entity.Shot.sg_shot_type', 'is', 'VFX'],
                         ['entity.Shot.reel', 'is', reel_dict]]
        else:
            sg_filter = [['project', 'is', self._project],
                         ['entity.Shot.sg_shot_type', 'is', 'VFX']]
        self.di_check_log += "\nShotgun Filter Used: {}".format(sg_filter)
        try:
            self._shotgun_version_list = self._sg.find('Version', sg_filter, self._fields)
            self.di_check_log += "\nVersion List Count: {}".format(len([i['code'] for i in self._shotgun_version_list]))
            self._shotgun_version_dict.update({ver_item['code'].lower(): ver_item for ver_item in self._shotgun_version_list})
            self.di_check_log += "\nVersion Dict: {}".format(self._shotgun_version_dict)
        except Exception as e:
            self.di_check_log += "\nError: {}".format(e)
            return

    def process_version_di_edl_check(self):
        """

        :param version_name:
        :return:
        """
        self.di_check_log += "\nProcessing the Version DI EDL check"
        self.di_check_log += "\nedit_di_status == {}".format(self.di_status)
        for each_edl_version in self._edl_version_list:
            if each_edl_version.lower() in self._shotgun_version_dict:
                self.di_check_log += "\nChecking the edl version {} in shotgun: True".format(each_edl_version)
                if self._shotgun_version_dict[each_edl_version.lower()].get('sg_edit_di_status', 'Key Error') == self.di_status:
                    self.di_check_log += "\nChecking the edl version {} in shotgun and DI Status is {}: True".format(
                        each_edl_version, self.di_status)
                    self._valid_edl_di_shotgun.append(each_edl_version)
                else:
                    self.di_check_log += "\nChecking the edl version {} in shotgun and DI Status is {}: False".format(
                        each_edl_version, self.di_status)
                    if each_edl_version in self._invalid_edl_di_shotgun:
                        continue
                    self._invalid_edl_di_shotgun.append(each_edl_version)
            else:
                self.di_check_log += "\nChecking the edl version {} in shotgun: False".format(each_edl_version)
                if each_edl_version in self._edl_not_in_shotgun:
                    continue
                self._edl_not_in_shotgun.append(each_edl_version)
        self.di_check_log += "\nThese Versions are in the EDL but not in Shotgun: \n{}".format(self._edl_not_in_shotgun)
        self.di_check_log += "\nThese Versions are not {}: \n{}".format(self.di_status, self._invalid_edl_di_shotgun)

    def process_shotgun_di_status_check(self):
        """

        :return:
        """
        self.di_check_log += "\nProcessing the SAME reel Version NOT in the EDL, and set to {}.".format(self.di_status)
        shotgun_version_set = set(self._shotgun_version_dict)
        edl_version_set = set(self._edl_version_list)
        shotgun_version_not_in_edl = list(shotgun_version_set - edl_version_set)
        self.di_check_log += "\nShotgun Version not in EDL: \n{}".format(shotgun_version_not_in_edl)
        self._shotgun_version_di_not_in_edl.extend([version_item for version_item in shotgun_version_not_in_edl if self._shotgun_version_dict[version_item]['sg_edit_di_status'] == self.di_status])
        self.di_check_log += "\nThese Versions are in Reel {} and set to {} but not in the EDL: \n{}".format(self._reel_name, self.di_status, self._shotgun_version_di_not_in_edl)

    def edit_parser(self, edit, logger):
        """

        :param edit:
        :param logger:
        :return:
        """
        edl.process_edit(edit, self._di_check_logging)
        if edit.comments:
            if isinstance(edit.comments, list):
                new_comment, edit._clip_name = edit.comments[0].split(':')
                if edit._clip_name:
                    clipname, ext = os.path.splitext(edit._clip_name)
                edit.get_version_name = lambda: clipname.strip().lower()

    def process_edl_file_data(self, edl_file_path):
        """

        :param edl_file_path:
        :return:
        """
        self.di_check_log += "\nProcessing edl File: %s" % edl_file_path
        self._di_check_logging.info("\nProcessing edl File: %s" % edl_file_path)
        try:
            edl_obj = edl.EditList(file_path=edl_file_path, visitor=self.edit_parser)
        except Exception as e:
            self.di_check_log += "\n{}".format(e)
            return False, e
        self.di_check_log += "\nExtracting the Reel Number from the File Name..."
        reel_split_name = os.path.splitext(os.path.basename(edl_file_path))[0].split('_')
        self.di_check_log += "\nReel Split Name: {}".format(reel_split_name)
        self._reel_name = reel_split_name[0][1:]
        self.di_check_log += "\nReel Number: {}".format(self._reel_name)
        for edl_item in edl_obj.edits:
            edl_version_name = edl_item.get_version_name()
            self.di_check_log += "\nVersion Name: {}".format(edl_version_name)
            if edl_version_name in self._edl_version_list:
                continue
            self._edl_version_list.append(edl_version_name.lower())
        return True, 'success'
