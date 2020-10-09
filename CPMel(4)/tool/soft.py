#!/usr/bin/python
# encoding:gbk
# ���ߣ���¡��
# ���ʱ��:2019.7.29
# ����޸�ʱ��:
'''
���ԣ�
������
������
SoftModificationToWeight ���޸�תȨ�ؼ���Ȩ�ؽڵ㷵��ÿ��ֵΪ����id����Ȩ�أ�
SoftModificationToJointWeight ���޸�ת�ؽ�Ȩ�����루�ؽڣ�ģ�ͣ���Ƥ�ڵ㣩
����ʾ����
ѡ��ģ�����
SoftModificationToWeight()
ѡ��ģ�����
SoftModificationToJointWeight(�ؽ�,ģ��,��Ƥ�ڵ�)
'''
import maya.OpenMaya as om
import pymel.core as pm


def SoftModificationToWeight ( ) :
    richSel = om.MRichSelection ( )
    om.MGlobal.getRichSelection ( richSel )
    richSelList = om.MSelectionList ( )
    richSel.getSelection ( richSelList )
    component = om.MObject ( )
    richSelList.getDagPath ( 0 , om.MDagPath ( ) , component )
    componentFn = om.MFnSingleIndexedComponent ( component )
    return [ (componentFn.element ( i ) , componentFn.weight ( i ).influence ( )) for i in
             range ( 0 , componentFn.elementCount ( ) ) ]


def SoftModificationToJointWeight ( Joint , mesh , skin ) :
    idSkin = SoftModificationToWeight ( )
    [ pm.skinPercent ( skin , mesh.vtx [ i [ 0 ] ] , transformValue = (Joint , i [ 1 ]) ) for i in idSkin ]
    return 0
