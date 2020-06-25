import pymel.core as pm

def transform_object(node_obj, translate_object, rotate_object, scale_object):
    pm.move(node_obj.name(), translate_object)
    pm.rotate(node_obj.name(), rotate_object)
    pm.scale(node_obj.name(), scale_object)

def create_instance_objects(node_obj, total_instance=10):
    all_instance_object = []
    counter = 1
    while (counter <= total_instance):
        inst_obj = pm.instance(node_obj.name())
        all_instance_object.append(inst_obj)
        counter += 1
        
    return all_instance_object


def main(transform_object, *args):
    all_obj = create_instance_objects(transform_object)
    for item in all_obj:
        transform_object(item[0], args[0], args[1], args[2]) 
        
main([10, 10, 30], [10, 10, 10], [2, 2, 2])
