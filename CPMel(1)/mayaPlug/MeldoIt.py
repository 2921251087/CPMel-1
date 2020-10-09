# -*- coding: gbk -*-
import maya.api.OpenMaya as om
import sys
import ctypes
import copy

def maya_useNewAPI():
    pass


class CPMeldoIt(om.MPxCommand):
    doIt_label = "d"
    undoIt_label = "ud"
    doIt_label_long = "doIt"
    undoIt_label_long = "undoIt"
    # is_copy = True

    doIt_def = False
    undoIt_def = False

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return CPMeldoIt()

    def doIt(self, args):
        arg_data = om.MArgDatabase(syntaxCreator(), args)
        if arg_data.isFlagSet(self.doIt_label_long) and arg_data.isFlagSet(self.undoIt_label_long):
            doIt_id = long(arg_data.flagArgumentString(self.doIt_label_long, 0))
            undoIt_id = long(arg_data.flagArgumentString(self.undoIt_label_long, 0))
            self.doIt_def = ctypes.cast(doIt_id, ctypes.py_object).value
            self.undoIt_def = ctypes.cast(undoIt_id, ctypes.py_object).value
            self.redoIt()
        else:
            om.MGlobal.displayError('No doItComm and undoItComm')
            return

    def redoIt(self):
        if self.doIt_def and self.undoIt_def:
            self.doIt_def()
        else:
            om.MGlobal.displayError('No doItComm and undoItComm')

    def undoIt(self):
        if self.doIt_def and self.undoIt_def:
            self.undoIt_def()
        else:
            om.MGlobal.displayError('No doItComm and undoItComm')

    def isUndoable(self):
        return True


def syntaxCreator():
    syntax = om.MSyntax()
    syntax.addFlag(CPMeldoIt.doIt_label, CPMeldoIt.doIt_label_long, syntax.kString)
    syntax.addFlag(CPMeldoIt.undoIt_label, CPMeldoIt.undoIt_label_long, syntax.kString)
    return syntax


def initializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject, "Phantom of the Cang", "0.1")
    try:
        mplugin.registerCommand('CPMeldoIt', CPMeldoIt.cmdCreator, syntaxCreator)
    except:
        sys.stderr.write("Failed to register command:CPMeldoIt")
        raise


def uninitializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand('CPMeldoIt')
    except:
        sys.stderr.write("Failed to unregister command:CPMeldoIt")
        raise
