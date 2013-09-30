import manymaya
import maya.cmds as cmds


@manymaya.instance
def fatcube_scene(filepath):
    #Create a new scene file
    cmds.file(new=True, force=True)

    #Perform some actions in the new scene
    pcube = cmds.polyCube(name='fatCube')
    cmds.xform(pcube, ws=True, t=(0.5, 0, 0))

    #Name the scene file and save
    cmds.file(rename=filepath)
    cmds.file(save=True, force=True)


if __name__ == "__main__":
    import os

    #Get some files to work on.
    maya_files = [
        os.path.abspath('tmp/path/to/file1.mb'),
        os.path.abspath('tmp/path/to/file2.mb'),
        os.path.abspath('tmp/path/to/file3.mb'),
        os.path.abspath('tmp/path/to/file4.mb')]
    manymaya.start(maya_files, fatcube_scene, verbose=False)