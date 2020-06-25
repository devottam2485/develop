
class SelectedNodeFilterUpdate(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'Update Filter')
        self.filterName = nuke.Enumeration_Knob('filter', 'filter', ['Select', 'filter', 'source_filter'])
        self.filterValue = nuke.Enumeration_Knob('filterValue', 'filter value', [])
        self.filterValue.clearFlag(nuke.STARTLINE)

        for k in (self.filterName, self.filterValue):
            self.addKnob(k)

    def knobChanged(self, knob):
        """
        Change event for any nuke knob
        :param knob: knob object name
        :return:
        """
        if knob.name() == 'filter':
           self.knob_name = self.filterName.value()
           self.valid_nodes = self.get_valid_nodes(self.knob_name)
           if not self.valid_nodes:
               nuke.message('The knob name does not exists on the selected Nodes')
               return
           filter_array_value = self.get_filter_values(self.knob_name, self.valid_nodes)
           if not filter_array_value:
               nuke.message('The knob name does not exists on the selected Nodes')
           self.filterValue.setValues(filter_array_value)
        if knob.name() == 'filterValue':
            self.knob_value = self.filterValue.value()
            self.update_filter_value(self.knob_name, self.knob_value, self.valid_nodes)
            nuke.message('Nodes Updated Successfully')
            return

    def get_valid_nodes(self, knob_name):
        """

        :param knob_name: knob object name on node
        :return: all the valid nodes
        """
        return [node for node in nuke.selectedNodes() if knob_name in nuke.toNode(node.name()).knobs().keys()]

    def get_filter_values(self, knob_name, valid_nodes):
        """

        :param knob_name: knob object name on node
        :param valid_nodes: selected nodes which has the knob name
        :return: nuke nodes
        """
        list_of_filter_values = []
        for node in valid_nodes:
            for item in nuke.toNode(node.name())[knob_name].values():
                if '\t' in item:
                    list_of_filter_values.append(filter(None, item.split('\t'))[0])
                else:
                    list_of_filter_values.append(item)

        return list(set(list_of_filter_values))

    def update_filter_value(self, knob_name, knob_value, valid_nodes):
        """

        :param knob_name: knob object name on node
        :param knob_value: knob value of type filter
        :param valid_nodes: selected nodes which has the knob name
        :return: nuke nodes
        """
        for node in valid_nodes:
            try:
                nuke.toNode(node.name())[knob_name].setValue(knob_value)
            except Exception as e:
                print(e)


def main():
    p = SelectedNodeFilterUpdate()
    p.showModalDialog()


if __name__ == "__main__":
    main()