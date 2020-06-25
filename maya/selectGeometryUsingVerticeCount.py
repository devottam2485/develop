import pymel.core as pm

def select_geometry(vertex_count):
    pm.select(deselect=True)
    for item in pm.ls(geometry=True):
        if vertex_count == item.numVertices():
            pm.select(item, add=True)
        else:
            continue

select_geometry(14)
