import sys
import os
import posixpath
import nuke

list_of_paths = eval(sys.argv[1])

write_node_path = sys.argv[2]

print("list_of_paths", list_of_paths)


def create_multichannel_exr():
    """
    Creating Read nodes with channel merge nodes and Contact sheet which finally write all the custom alpha channel.
    """
    constant_node = nuke.nodes.Constant()
    # constant_node = nuke.nodes.Remove(operation="remove", channels="all")
    switch_node = constant_node
    read_list = []
    input_width = int()
    input_height = int()
    input_pixel_aspect_ratio = int()
    for item in list_of_paths:
        item_split_list = item.split()
        if len(item_split_list) != 3:
            print
            "\nPlease check the {} path!\n".format(item)
            return
        read_node = nuke.nodes.Read()
        read_node.knob("file").setValue(item_split_list[0])
        read_node.knob("first").setValue(int(item_split_list[1].split('-')[0]))
        read_node.knob("last").setValue(int(item_split_list[1].split('-')[-1]))
        # read_list.append(read_node)

        input_width = read_node.metadata()['input/width']
        input_height = read_node.metadata()['input/height']
        input_pixel_aspect_ratio = read_node.metadata()['exr/pixelAspectRatio']

        nuke.Layer("%s" % item_split_list[-1], ['%s.alpha' % item_split_list[-1]])
        channel_merge_node = nuke.nodes.ChannelMerge()
        channel_merge_node.setInput(0, switch_node)
        channel_merge_node.setInput(1, read_node)
        channel_merge_node.knob("output").setValue("%s.alpha" % item_split_list[-1])
        # switch_node.setInput(0, read_list[0])
        switch_node = channel_merge_node

    contact_sheet = nuke.nodes.LayerContactSheet()
    contact_sheet.knob('width').setValue(int(input_width))
    contact_sheet.knob('height').setValue(int(input_height))
    contact_sheet.knob("center").setValue(True)
    contact_sheet.setInput(0, switch_node)

    channel_merge_node_contact = nuke.nodes.ChannelMerge()
    channel_merge_node_contact.knob("output").setValue('rgb.red')
    channel_merge_node_contact.setInput(0, switch_node)
    channel_merge_node_contact.setInput(1, contact_sheet)

    reformat_node = nuke.nodes.Reformat()
    reformat_node.knob("type").setValue("to box")
    reformat_node.knob("box_fixed").setValue(1)
    reformat_node.knob('box_width').setValue(int(input_width))
    reformat_node.knob('box_height').setValue(int(input_height))
    reformat_node.knob('resize').setValue('none')
    reformat_node.knob('box_pixel_aspect').setValue(int(input_pixel_aspect_ratio))
    reformat_node.setInput(0, channel_merge_node_contact)

    write_node = nuke.nodes.Write()
    write_node.setInput(0, reformat_node)
    write_node.knob("file").setValue(write_node_path)
    write_node.knob("channels").setValue('all')
    write_node.knob("file_type").setValue("exr")

    roto_format = " {} {} for_roto".format(input_width, input_height)
    nuke.addFormat(roto_format)

    nuke.root()['format'].setValue('for_roto')

    nuke.scriptSaveAs(posixpath.join(os.path.dirname(write_node_path), 'multichannel_nuke_render.nk'), 1)
    # nuke.execute('Write1', read_node.knob("first").value(), read_node.knob("last").value())


if __name__ == "__main__":
    """
    Calling the main function
    """
    create_multichannel_exr()