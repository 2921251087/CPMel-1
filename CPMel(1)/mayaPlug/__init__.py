# -*- coding: gbk -*-
import os
import re
import maya.cmds as mc
import maya.api.OpenMaya as om
import GetPath

def main():
    path_list = [i for i in os.listdir('%s\\mayaPlug'%GetPath.PATH) if not re.match('__',i)]
    for i in path_list:
        om.MGlobal.displayInfo('CPMel:���ڼ���%s'%i)
        mc.loadPlugin('%s\\mayaPlug\\%s'%(GetPath.PATH,i))
        om.MGlobal.displayInfo('CPMel:�ɹ�����%s'%i)
    return True
main()