import sys
sys.path.append("C:/PROJECTS/manymaya")
import manymaya
import maya.cmds as cmds


@manymaya.instance
def create_lite_scene(filepath):
    #Create a new scene file
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
    cmds.scriptEditorInfo(suppressInfo=True, suppressResults=True)
    cmds.file(filepath, open=True, force=True)
    cmds.polyCube(name="my_cuber2")
    cmds.file(save=True, force=True)


if __name__ == "__main__":
    import tempfile
    import shutil
    import os
    import timeit

    def setup():
        tempdir = tempfile.mkdtemp()
        maya_files = [os.path.join(tempdir, 'file{0:0>4d}.mb'.format(i)) for i in range(100)]
        return tempdir, maya_files


    #Time 1 Process
    print "1 Process:"
    tempdir, maya_files = setup()

    create_time = timeit.timeit(
        'manymaya.start(maya_files, create_lite_scene, processes=1, verbose=False)',
        number=10)
    print "\tCreate 100 files: {0}".format(create_time)

    modify_time = timeit.timeit(
        'manymaya.start(maya_files, modify_lite_scene, processes=1, verbose=False)',
        number=10)
    print "\tModify 100 files: {0}".format(modify_time)

    shutil.rmtree(tempdir)


    #Time 2 Process
    print "2 Process:"
    tempdir, maya_files = setup()

    create_time = timeit.timeit(
        'manymaya.start(maya_files, create_lite_scene, processes=2, verbose=False)',
        number=10)
    print "\tCreate 100 files: {0}".format(create_time)

    modify_time = timeit.timeit(
        'manymaya.start(maya_files, modify_lite_scene, processes=2, verbose=False)',
        number=10)
    print "\tModify 100 files: {0}".format(modify_time)

    shutil.rmtree(tempdir)


    #Time 3 Process
    print "3 Process:"
    tempdir, maya_files = setup()

    create_time = timeit.timeit(
        'manymaya.start(maya_files, create_lite_scene, processes=3, verbose=False)',
        number=10)
    print "\tCreate 100 files: {0}".format(create_time)

    modify_time = timeit.timeit(
        'manymaya.start(maya_files, modify_lite_scene, processes=3, verbose=False)',
        number=10)
    print "\tModify 100 files: {0}".format(modify_time)

    shutil.rmtree(tempdir)


    #Time 4 Process
    print "4 Process:"
    tempdir, maya_files = setup()

    create_time = timeit.timeit(
        'manymaya.start(maya_files, create_lite_scene, processes=4, verbose=False)',
        number=10)
    print "\tCreate 100 files: {0}".format(create_time)

    modify_time = timeit.timeit(
        'manymaya.start(maya_files, modify_lite_scene, processes=4, verbose=False)',
        number=10)
    print "\tModify 100 files: {0}".format(modify_time)

    shutil.rmtree(tempdir)