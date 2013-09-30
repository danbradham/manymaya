#ManyMaya
A fast and light-weight wrapper for Autodesk Maya's standalone extension. ManyMaya leverages the multiprocessing module to run maya.standalone instances concurrently.

```python
import manymaya
import maya.cmds as cmds

@manymaya.instance
def delete_attributes(filepath):
    cmds.file(filepath, open=True, force=True)
    for node in cmds.ls(long=True):
        attr = node + '.userattr'
        if cmds.objExists(attr):
            cmds.deleteAttr(attr)
    cmds.file(save=True, force=True)

if __name__ == "__main__":
    #Find some files to work on
    maya_files = manymaya.find('path/to/search')
    manymaya.start(maya_files, make_cube)
```