#!/usr/bin/python
#-*-coding:gbk -*-
import mayaPlug
import maya.cmds as mc
#������������ӵ����������
def addCommand(doIt, undoIt):
    if callable(doIt) and callable(undoIt):
        try:
            mc.CPMeldoIt(d=id(doIt), ud=id(undoIt))
            return 0
        except:
            return 1
    else:
        return 1
#��δʵ������ע����
class Command(object):
    pass