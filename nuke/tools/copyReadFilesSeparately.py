import shutil
import posixpath
import os

read_node_array = []

def get_selected_write_node():
    """
    get selected write nodes.
    :return: Returns selected write nodes.
    """
    return [each for each in nuke.selectedNodes() if each.Class() == 'Write']


def get_the_loader_recursively(node):
    """
    get all the read nodes.
    :node: write node
    :return: None
    """
    global read_node_array
    for node in node.dependencies():
        if node.Class() == 'Read':
            read_node_array.append(node)
        else:
            get_the_loader_recursively(node)


def copying_the_inputs_separately(folder_path):
    """
    copying the from the sorce to destination
    :folder_path: Destination path where the inputs are moved
    :return: none
    """
    for read_node in read_node_array:
        final_path = posixpath.join(folder_path, read_node.name())
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        get_node_path = nuke.toNode(read_node.name())['file'].value()
        src_dir_name = os.path.dirname(get_node_path)
        for file_item in os.listdir(src_dir_name):    
            src_path = posixpath.join(src_dir_name, file_item)
            dst_path = posixpath.join(final_path, file_item)
            try:
                print "copying {} --> {}".format(src_path, dst_path)
                shutil.copy(src_path, dst_path)
            except Exception as e:
                print(e)

    nuke.message("Inputs moved to separate folders")


def main():
    """
    main function
    :return: None
    """
    p = nuke.Panel('Package Inputs')    
    p.addFilenameSearch('folder path', '../')
    p.addButton('cancel')
    p.addButton('proceed')
    ret = p.show()
    if ret == 1:
        selected_nodes = get_selected_write_node()
        if not selected_nodes:
            nuke.message("Please select a Write node to proceed.")
            return
        for node in selected_nodes:
            get_the_loader_recursively(node)
        copying_the_inputs_separately(p.value('folder path'))


if __name__ == "__main__":
    main()      
