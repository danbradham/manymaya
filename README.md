#ManyMaya
A fast and light-weight wrapper for Autodesk Maya's standalone extension. ManyMaya leverages the multiprocessing module to run maya.standalone instances concurrently.


##An example
Delete attributes from all maya files in a directory.

```python
import manymaya
import maya.cmds as cmds

#Decorate the function you'd like to run in each file.
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
    #Start instances and run delete_attributes on each file.
    manymaya.start(maya_files, delete_attributes)
```


###API
As you can see ManyMaya is very easy to use. Simply decorate a function that takes a single argument, *filepath*, then call manymaya.start with a list of filepaths and the decorated function as arguments.

####manymaya.instance
A decorator that wraps your function inside a maya.standalone instance. Every function you decorate with instance, must have a filepath argument.

####manymaya.start(file_list, fn, processes=4, verbose=False)
Creates a multiprocessing Queue and runs several worker processes to pull from it.

  - *file_list*: List of files to process.
  - *fn*: Target function.
  - *processes*: Number of processes to run concurrently. (optional)
  - *verbose*: Print verbose output. (optional)

####manymaya.find(inside, exts=['ma', 'mb'], subdirs=True):
Search a specified directory for Maya compatible files.
Returns a list of filepaths for use with manymaya.start().

  - *inside*: Path to search.
  - *exts*: Extensions of files to include in returned list. (optional)
  - *subdirs*: Search inside subdirs. (optional)

####manymaya.log(message, level="INFO"):
Fluff...Exists only to shorten logging calls.

-  message: Message to log.
-  level: Level at which to log message. (optional)


##Installation

    git clone https://danbradham@github.com/danbradham/manymaya.git
    cd manymaya
    python setup.py install

###Running ManyMaya Scripts
The best way to run a script utilizing ManyMaya is to execute it with mayapy, located in your Maya's bin path. You may want to add Maya's bin folder to your environment path to ease the use of calling mayapy.

    mayapy path/to/my/script.py


##To Do
  - Improve logging.
  - Make output more verbose.
