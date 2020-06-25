import sgtk
import csv
import os

class ShotFinalCheck(object):
    def __init__(self):
        super(ShotFinalCheck, self).__init__()
        self.final_check_log = '\n<--------------------Shot Final Check Log Starts here-------------------->'
        self._finals_not_production = []
        self._finals_production = []
        self._finals_avid = []
        self._finals_not_avid = []
        self._sg = sgtk.util.shotgun.create_sg_connection()
        self._project = sgtk.platform.current_bundle().context.project
        self._sg_fields = ['code']

    @property
    def get_final_not_production(self):
        """

        :return:
        """
        return self._finals_not_production

    @property
    def get_final_production(self):
        """

        :return:
        """
        return self._finals_production

    @property
    def get_final_avid(self):
        """

        :return:
        """
        return self._finals_avid

    @property
    def get_final_not_avid(self):
        """

        :return:
        """
        return self._finals_not_avid

    def read_version(self, row):
        """

        :param row:
        :return:
        """
        for name, value in row.iteritems():
            field = name.decode('iso-8859-1').encode('ascii', 'ignore').strip()
            if field == "Name":
                # remove the file extension
                return os.path.splitext(value.decode('iso-8859-1').encode('ascii', 'ignore').strip())[0]
            else:
                continue

    def process_file_data(self, file_path):
        """

        :param file_path:
        :return:
        """
        self.final_check_log += '\nReading file {}...'.format(file_path)
        if not file_path.endswith('.txt'):
            self.final_check_log += '\nNot a valid Path for Shot Final Check'
            return
        with open(file_path, "rU") as csvFile:
            csv_reader = csv.DictReader(csvFile, delimiter='\t')
            line = 1
            for row in csv_reader:
                self.final_check_log += '\nExtracting the Version name from Line: {}.'.format(line)
                version_name = self.read_version(row)
                self.final_check_log += '\nVersion name: {}.'.format(version_name)
                if version_name:
                    if version_name in self._finals_avid:
                        continue
                    self._finals_avid.append(version_name.lower())
                else:
                    self.final_check_log += '\nFound no Version name on Line: {}'.format(line)
                    continue
                line += 1

    def process_final_check(self, file_data):
        """

        :param file_data:
        :return:
        """
        if not file_data:
            self.final_check_log += '\nFound No Data for Shot Final Check'
            return
        filters = [['sg_status_list', 'is', 'final'],
                   ["project", "is", self._project],
                   ['entity.Shot.sg_shot_type', 'is', 'VFX']]
        self.final_check_log += '\n\nFilter Used: {}'.format(filters)
        shotgun_query_data = {}
        try:
            shotgun_query_data = self._sg.find('Version', filters, self._sg_fields)
        except Exception as e:
            self.final_check_log += '\n{}'.format(e)
        if not shotgun_query_data:
            self.final_check_log += '\nFound no data for Shot Field {}'.format(self._sg_fields)
            return
        self.final_check_log += '\n{}'.format(shotgun_query_data)
        for shot_item in shotgun_query_data:
            if os.path.splitext(shot_item['code'])[0].strip().lower() not in self._finals_production:
                self._finals_production.append(os.path.splitext(shot_item['code'])[0].strip().lower())
        self.final_check_log += '\n{0} | {1} | {0}\n{2}'.format('-'*10, 'Final Production Shot', self._finals_production)

        for data_item in file_data:
            if data_item in self._finals_production:
                continue
            else:
                self._finals_not_production.append(data_item)
        self.final_check_log += '\n{0} | {1} | {0}\n{2}'.format('-'*10, 'Non-final Production Shot', self._finals_not_production)

        for version_item in self._finals_production:
            if version_item not in self._finals_avid and version_item not in self._finals_not_avid:
                self._finals_not_avid.append(version_item)
