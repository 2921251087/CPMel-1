#!/usr/bin/python
#-*-coding:gbk -*-
import pymel.core as pm
import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import functools
import CPMel.core as cmc

#���Ǹ��Դ󲿷ֱ����������ݵ�����Ȩ�غ���(�������ڵ�,Ȩ���б�#һ�������Ӧһ��floatֵ#,���=None)
#����������������Ĭ�����ñ�����Ӱ������ж���
#������ֻҪ��һ�������Ӱ�춼��Ĭ��������������������ҪΪ������������������һ��Ȩ��,����maya�������޷��޸�#
def setDeformerWeigth(DeformerNode,weights,geo=None):
    #DeformerNode = 'softMod1'
    #geo = None
    #weights = [0 for i in pm.selected(fl = True)]

    if not pm.objExists(DeformerNode):
        om.MGlobal.displayError('��������ı��νڵ㲢������')
        return False
    if not isinstance(DeformerNode,basestring):
    	DeformerNode = DeformerNode.nodeName()
    if not geo is None:
        if not pm.objExists(geo):
            om.MGlobal.displayError('��������Ķ��󲢲�����')
            return False
        if not isinstance(geo,basestring):
            geo = ['%s'%i for i in pm.ls(geo)]
        else:
            geo = [geo]
    sel = om.MSelectionList()
    obj = om.MObject()
    path = om.MDagPath()
    comp = om.MObject()
    try:
        sel.add(DeformerNode)
    except:
        om.MGlobal.displayError('�޷��ҵ����νڵ�')
        return False
    sel.getDependNode(0,obj)
    
    try:
        weightGeo = oma.MFnWeightGeometryFilter(obj)
    except:
        om.MGlobal.displayError('����ı��νڵ㲻����ȷ�Ķ���(��,�����...)')
        return False
    float_array = om.MFloatArray()
    append = float_array.append
    try:
        [append(i) for i in weights]
    except:
        om.MGlobal.displayError('����Ȩ���б����')
        return False
    sel = om.MSelectionList()
    if not geo is None:
        try:
            [sel.add(i) for i in geo]
        except:
            om.MGlobal.displayError('�޷��ҵ����ζ���')
            return False

        sel.getDagPath(0,path,comp)
    
        try:
            undoIt_float_array = om.MFloatArray()
            weightGeo.getWeights(path,comp,undoIt_float_array)
            doIt_def = functools.partial(weightGeo.setWeight,path,comp,float_array)
            undoIt_def = functools.partial(weightGeo.setWeight,path,comp,undoIt_float_array)
            cmc.addCommand(doIt_def,undoIt_def)
        except:
            om.MGlobal.displayError('����Ȩ�ط�������')
            return False
    else:
        comp_dict = {'mesh':'vtx','nurbsCurve':'cv','nurbsSurface':'cv','lattice':'pt'}
        for i in range(weightGeo.numOutputConnections()):
            weightGeo.getPathAtIndex(i,path)
            itGeo = om.MItGeometry(weightGeo.outputShapeAtIndex(i))
            length = itGeo.exactCount()
            shape = path.fullPathName()
            shape_type = mc.objectType(shape)
            comp_type = comp_dict[shape_type]
            for t in range(length):
                sel.add('%s.%s[%d]'%(shape,comp_type,itGeo.index()) )
                itGeo.next()
        if sel.length() == 1:
            sel.getDagPath(0,path,comp)
            try:
                undoIt_float_array = om.MFloatArray()
                weightGeo.getWeights(path,comp,undoIt_float_array)
                doIt_def = functools.partial(weightGeo.setWeight,path,0,comp,float_array)
                undoIt_def = functools.partial(weightGeo.setWeight,path,0,comp,undoIt_float_array)
                cmc.addCommand(doIt_def,undoIt_def)
            except:
                om.MGlobal.displayError('����Ȩ�ط�������')
                return False
        crr_id = 0
        for i in range(sel.length()):
            sel.getDagPath(i,path,comp)
            obj_comp_size = om.MFnComponent(comp).elementCount()
            try:
                undoIt_float_array = om.MFloatArray()
                weightGeo.getWeights(path,comp,undoIt_float_array)
                
                doIt_float_array = float_array[crr_id:crr_id+obj_comp_size]
                
                doIt_def = functools.partial(weightGeo.setWeight,path,i,comp,doIt_float_array)
                undoIt_def = functools.partial(weightGeo.setWeight,path,i,comp,undoIt_float_array)
                cmc.addCommand(doIt_def,undoIt_def)
                
                #weightGeo.setWeight(path,i,obj,float_array[crr_id:crr_id+obj_comp_size])
            except:
                om.MGlobal.displayError('����Ȩ�ط�������')
                return False
            crr_id += obj_comp_size
    return True