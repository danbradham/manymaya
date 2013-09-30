import manymaya
import maya.cmds as cmds


@manymaya.instance
def make_cube(filepath):
    cmds.file(filepath, open=True, force=True)
    cmds.polyCube(name="my_cube")
    cmds.file(save=True, force=True)

if __name__ == "__main__":
    #Get some files to work on.
    maya_files = manymaya.find('path/to/search')
    manymaya.start(maya_files, make_cube)