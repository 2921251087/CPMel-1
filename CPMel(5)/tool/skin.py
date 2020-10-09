#!/usr/bin/python
# encoding:gbk
# ���ߣ���¡��
# ���ʱ��:2020.1.17
# ����޸�ʱ��:
'''
���Ǹ�����maya��Ƥ��ģ��
'''
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import functools
import pymel.core as pm
import CPMel.core as cmcore
if __name__ == "__main__":
    import CPMel.tool.Universal as universal
else:
    import Universal as universal
#���Ի�Ȩ��
def rigidWeighting(mesh_list = None):
    if mesh_list is None:mesh_list = [i.getShape() for i in pm.selected()]
    for i in mesh_list:
        skinNode = i.history(type='skinCluster')
        if len(skinNode)<1:
            continue
        skinNode = skinNode[0]
        inf = range(len(skinNode.getInfluence()))
        weigth = [s for t in skinNode.getWeights(i) for s in rigidList(t)]
        setWeigths(skinNode, i, inf, weigth)
    return 0
#���Ի��б�ֻ��һ��Ϊ1��ֵ������Ϊ0
def rigidList(in_v):
    test_max = max(in_v)
    i_id = range(len(in_v))
    try:
        max_id = in_v.index(1)
    except:
        max_id = None
        crr_v = None
        for t,id in zip(in_v, i_id):
            if crr_v is None or crr_v<t:
                crr_v = t
                max_id=id
    return [1 if i == max_id else 0 for i in i_id]
#������ƤȨ��(skinNode, geo, weigth, inf = None)(��Ƥ�ڵ�,��Ƥ����,Ȩ��,Ӱ�������������飨ps�����û������Ļ�����Ĭ�ϲ������У�)
# def setWeigths(skinNode, geo, weigth, inf = None): 
#     if inf is None:
#         unWeights = [t for i in skinNode.getWeights(geo) for t in i]
#         inf = range(len(skinNode.getInfluence()))
#     else:
#         unWeights = [
#             t for i in
#             zip(*[
#                 [
#                     t for t in skinNode.getWeights(geo, i)
#                 ] for i in inf
#             ])
#             for t in i
#         ]
#     doIt = functools.partial(skinNode.setWeights, geo, inf, weigth)
#     undoIt = functools.partial(skinNode.setWeights, geo, inf, unWeights)
#     return cmcore.addCommand(doIt, undoIt)

#������ƤȨ��(skinNode, geo, inf, weigth)(��Ƥ�ڵ�,��Ƥ����,Ӱ��������������,Ȩ��)
def setWeigths(skinNode, geo, inf, weigth):
    #���һ������б�
    cmp_list = [universal.intoComponents(i) for i in universal.translateToName(geo)]
    #�������б������
    if len(cmp_list)<1:
        raise EOFError('geoû���κζ���')
    #����һ�����ѡ���б�
    sel_list = om.MSelectionList()
    [sel_list.add(i) for i in cmp_list]
    if int(sel_list.length())>1:
        raise EOFError('%s ����һ��mesh��������������'%geo)
        return 1
    path,comp = sel_list.getComponent(0)
    sel_list.add(skinNode)
    skinNode = sel_list.getDependNode(1)


    fn_skin = oma.MFnSkinCluster(skinNode)

    m_inf = om.MIntArray(inf)
    m_weigth = om.MDoubleArray(weigth)
    #������Ȩ��
    unWeights = fn_skin.getWeights(path,comp,m_inf)

    doIt = functools.partial(fn_skin.setWeights,path,comp,m_inf,m_weigth)
    undoIt = functools.partial(fn_skin.setWeights,path,comp,m_inf,unWeights)
    return cmcore.addCommand(doIt, undoIt)
class SetWeights:
    '''
    ������ƤȨ�ص���
    __init__(self,skinNode, geo)#(��Ƥ�ڵ�,��Ҫ���õı���Ƥ�ڵ�Ӱ��Ķ���)
    setWeigths(self,inf,weigth)#������ƤȨ��
    getWeigths(self,inf)#�����ƤȨ��
    setBlendWeights(self,weigth)#����DQ���Ȩ��
    getBlendWeights(self)#���DQȨ��
    ʾ��
    import CPMel.tool.skin as skin
    reload(skin)
    skinNode,geo,inf,weights=('skinCluster1','pSphere1',[0,1],[t for i in range(382) for t in range(2) ])
    SetWeights = skin.SetWeights(skinNode,geo)
    SetWeights.getWeigths(inf)
    SetWeights.setWeigths(inf,weights)
    '''
    def __init__(self,skinNode, geo):
        #���һ������б�
        cmp_list = [universal.intoComponents(i) for i in universal.translateToName(geo)]
        #�������б������
        if len(cmp_list)<1:
            raise EOFError('geoû���κζ���')
        #����һ�����ѡ���б�
        sel_list = om.MSelectionList()
        [sel_list.add(i) for i in cmp_list]
        if int(sel_list.length())>1:
            raise EOFError('%s ����һ��mesh��������������'%geo)
            return 1
        self.path,self.comp = sel_list.getComponent(0)
        sel_list.add(skinNode)
        skinNode = sel_list.getDependNode(1)

        self.fn_skin = oma.MFnSkinCluster(skinNode)
    def setWeigths(self,inf,weigth):
        m_inf = om.MIntArray(inf)
        #ִ�е�Ȩ��
        m_weigth = om.MDoubleArray(weigth)
        #������Ȩ��
        unWeights = self.fn_skin.getWeights(self.path,self.comp,m_inf)

        doIt = functools.partial(self.fn_skin.setWeights,self.path,self.comp,m_inf,m_weigth)
        undoIt = functools.partial(self.fn_skin.setWeights,self.path,self.comp,m_inf,unWeights)
        return cmcore.addCommand(doIt, undoIt)
    def getWeigths(self,inf):
        m_inf = om.MIntArray(inf)
        return self.fn_skin.getWeights(self.path,self.comp,m_inf)
    def setBlendWeights(self,weigth):
        #ִ�е�Ȩ��
        m_weigth = om.MDoubleArray(weigth)
        #������Ȩ��
        unWeights = self.fn_skin.getBlendWeights(self.path,self.comp)
        doIt = functools.partial(self.fn_skin.setBlendWeights,self.path,self.comp,m_weigth)
        undoIt = functools.partial(self.fn_skin.setBlendWeights,self.path,self.comp,unWeights)
        return cmcore.addCommand(doIt, undoIt)
    def getBlendWeights(self):
        return self.fn_skin.getBlendWeights(self.path,self.comp)