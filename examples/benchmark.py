import sys
sys.path.append("C:/PROJECTS/manymaya")
import manymaya
import maya.cmds as cmds


@manymaya.instance
def create_lite_scene(filepath):
    #Create a new scene file
    cmds.scriptEditorInfo(
        suppressInfo=True,
        suppressResults=True,
        suppressErrors=True,
        suppressWarnings=True)
    cmds.file(new=True, force=True)

    #Perform some actions in the new scene
    pcube = cmds.polyCube(name='my_cuber1')
    cmds.xform(pcube, ws=True, t=(0.5, 0, 0))

    #Name the scene file and save
    cmds.file(rename=filepath)
    cmds.file(save=True, force=True)


@manymaya.instance
def modify_lite_scene(filepath):
    #Use the maya.cmds module to manipulate Maya
    cmds.scriptEditorInfo(
        suppressInfo=True,
        suppressResults=True,
        suppressErrors=True,
        suppressWarnings=True)
    cmds.file(filepath, open=True, force=True)
    cmds.polyCube(name="my_cuber2")
    cmds.file(save=True, force=True)


if __name__ == "__main__":
    import tempfile
    import shutil
    import os
    import time

    def setup(num_files):
        tempdir = tempfile.mkdtemp()
        maya_files = [os.path.join(tempdir, 'file{0:0>4d}.mb'.format(i)) for i in range(num_files)]
        return tempdir, maya_files

    def create_modify_benchmark(num_processes, num_files):
        print num_processes, " Process:"
        tempdir, maya_files = setup(num_files)

        start = time.clock()
        manymaya.start(maya_files, create_lite_scene, processes=num_processes, verbose=True)
        print "\tCreate: {0}".format(time.clock() - start)

        start = time.clock()
        manymaya.start(maya_files, modify_lite_scene, processes=num_processes, verbose=True)
        print "\tModify: {0}".format(time.clock() - start)

        shutil.rmtree(tempdir)

    create_modify_benchmark(2, 2000)