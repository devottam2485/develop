import maya.cmds as mc
import pymel.core as core
import pymel.core.datatypes as dt
import pymel.core.animation as anim
import math

def trackCameraStabilizerXYPos(cameraName, *trackers):
    camShapeList = core.ls(cameraName, dag=True, type="camera")
    trackPos = []
    if len(trackers) == 1:
        trackerName = trackers[0]
        trackPos = core.xform(trackerName, query=True, worldSpace=True, rotatePivot=True)
    if len(trackers) == 2:
        trackerName1 = trackers[0]
        trackPos1 = core.xform(trackerName1, query=True, worldSpace=True, rotatePivot=True)
        trackerName2 = trackers[1]
        trackPos2 = core.xform(trackerName2, query=True, worldSpace=True, rotatePivot=True)
        trackPos.extend(
            [(trackPos1[0] + trackPos2[0]) / 2, (trackPos1[1] + trackPos2[1]) / 2, (trackPos1[2] + trackPos2[2]) / 2])
    cameraWorldInverseMatrix = core.getAttr("{}.worldInverseMatrix".format(cameraName))

    inverseMatrix = dt.Matrix(cameraWorldInverseMatrix[0][0], cameraWorldInverseMatrix[0][1],
                              cameraWorldInverseMatrix[0][2], cameraWorldInverseMatrix[0][3],
                              cameraWorldInverseMatrix[1][0], cameraWorldInverseMatrix[1][1],
                              cameraWorldInverseMatrix[1][2], cameraWorldInverseMatrix[1][3],
                              cameraWorldInverseMatrix[2][0], cameraWorldInverseMatrix[2][1],
                              cameraWorldInverseMatrix[2][2], cameraWorldInverseMatrix[2][3],
                              cameraWorldInverseMatrix[3][0], cameraWorldInverseMatrix[3][1],
                              cameraWorldInverseMatrix[3][2], cameraWorldInverseMatrix[3][3])

    v1 = dt.Matrix(trackPos[0], trackPos[1], trackPos[2], 1.0)
    v2 = v1.__mul__(inverseMatrix)

    screenPos = dt.Vector(v2[0][0], v2[0][1], v2[0][2])

    horizontalFieldView = core.camera(camShapeList[0], query=True, horizontalFieldOfView=True)
    verticalFieldView = core.camera(camShapeList[0], query=True, verticalFieldOfView=True)

    horizontalFilmAperture = core.getAttr("{}.horizontalFilmAperture".format(camShapeList[0]))
    verticalFilmAperture = core.getAttr("{}.verticalFilmAperture".format(camShapeList[0]))

    posX = ((screenPos.x / (-screenPos.z)) / dt.tan(
        math.radians(horizontalFieldView / 2)) * horizontalFilmAperture * .5)
    posY = ((screenPos.y / (-screenPos.z)) / dt.tan(math.radians(verticalFieldView / 2)) * verticalFilmAperture * .5)

    return posX, posY


def trackCameraStabilizerApply(cameraName, *trackers):
    camShapeList = core.ls(cameraName, dag=True, type="camera")
    if core.attributeQuery("offsetX", node=camShapeList[0], exists=True):
        core.deleteAttr(camShapeList[0], attribute="offsetX")
    if core.attributeQuery("offsetY", node=camShapeList[0], exists=True):
        core.deleteAttr(camShapeList[0], attribute="offsetY")
    if core.attributeQuery("stabilizeX", node=camShapeList[0], exists=True):
        core.deleteAttr(camShapeList[0], attribute="stabilizeX")
    if core.attributeQuery("stabilizeY", node=camShapeList[0], exists=True):
        core.deleteAttr(camShapeList[0], attribute="stabilizeY")
    core.addAttr(camShapeList[0], shortName="offsetX", attributeType="float", keyable=True)
    core.addAttr(camShapeList[0], shortName="offsetY", attributeType="float", keyable=True)
    core.addAttr(camShapeList[0], shortName="stabilizeX", attributeType="float", keyable=True)
    core.addAttr(camShapeList[0], shortName="stabilizeY", attributeType="float", keyable=True)

    start_time = int(anim.playbackOptions(animationStartTime=True, query=True))
    end_time = int(anim.playbackOptions(animationEndTime=True, query=True))

    for frame_item in range(start_time, end_time + 1):
        print(frame_item)
        core.currentTime(frame_item)
        screenPosX, screenPosY = trackCameraStabilizerXYPos(cameraName, *trackers)
        print(screenPosX, screenPosY)
        core.setAttr("{}.stabilizeX".format(camShapeList[0]), screenPosX, keyable=True)
        core.setKeyframe(camShapeList[0], attribute="stabilizeX", time=frame_item)
        core.setAttr("{}.stabilizeY".format(camShapeList[0]), screenPosY, keyable=True)
        core.setKeyframe(camShapeList[0], attribute="stabilizeY", time=frame_item)

    core.setAttr("{}.panZoomEnabled".format(camShapeList[0]), 1)

    expression_string = "{0}.horizontalPan = ({0}.stabilizeX + {0}.offsetX);\n{0}.verticalPan = ({0}.stabilizeY + {0}.offsetY);".format(
        camShapeList[0].nodeName())
    core.expression(string=expression_string)


def main():
    selected_obj = core.ls(sl=True)
    selection_count = len(selected_obj)
    if selection_count <= 1:
        print("Please select the camera and tracker to use stabillize tool")
        return
    camera_name = ""

    if core.objectType(selected_obj[0].getShape()) == "camera":
        camera_name = selected_obj[0].name()
    else:
        print("Selection order should be camera, then trackers")
        return

    if selection_count == 2:
        tracker_obj1 = selected_obj[-1].name()
        trackCameraStabilizerApply(camera_name, tracker_obj1)
    elif selection_count == 3:
        tracker_obj1 = selected_obj[-1].name()
        tracker_obj2 = selected_obj[1].name()
        trackCameraStabilizerApply(camera_name, tracker_obj1, tracker_obj2)
    else:
        print("Stabillize tool will not work on more than two objects transform")
