#!/usr/bin/python
#-*-coding:gbk -*-
import maya.OpenMaya as om
import pymel.core as pm
import CPMel.outputMaya as outputmaya
class CPGetMeshConnect():
    '''
    ���ڻ�ö����������Ϣ
    ����
        _is_c_path(�Ƿ��Ѿ�����·��)
        _vtx_to_e �������Ӧ�ߵ��ֵ䣩
        _e_to_vtx ���߶�Ӧ������ֵ䣩
        _vtx_to_vtx �������Ӧ������ֵ䣩
    ������
        c_vtx_to_e (self)�����������Ӧ�ߵ��ֵ䣩
        c_e_to_vtx (self)�������߶�Ӧ������ֵ䣩
        c_vtx_to_vtx (self)�����������Ӧ������ֵ䣩
        get_vtx_to_e_connect (self)����ö����Ӧ�ߵ��ֵ䣩
        get_e_to_vtx_connect (self)����ñ߶�Ӧ������ֵ䣩
        get_vtx_to_vtx_connect (self)����ö����Ӧ������ֵ䣩
        get_vtx_path ��self,vtx_id�������һ�����������ж���ı���·�����룩#���Ǹ����ص�����#
    '''
    _is_c_path = False
    _vtx_to_e = False
    _e_to_vtx = False
    _vtx_to_vtx = False

    def __init__(self, obj=False):
        if obj:
            sel = om.MSelectionList()
            sel.add(obj)
            self.path = om.MDagPath()
            sel.getDagPath(0, self.path)
            self._is_c_path = TabError
        else:
            om.MGlobal.displayError('No set mesh name')

    def c_vtx_to_e(self):
        if not self._is_c_path:
            om.MGlobal.displayError('No set mesh name')
            return 0
        it_vtx = om.MItMeshVertex(self.path)
        self._vtx_to_e = dict()
        for i in range(it_vtx.count()):
            int_list = om.MIntArray()
            it_vtx.getConnectedEdges(int_list)
            self._vtx_to_e[i] = int_list
            it_vtx.next()

    def c_e_to_vtx(self):
        if not self._is_c_path:
            om.MGlobal.displayError('No set mesh name')
            return 0
        if not self._vtx_to_e:
            self.c_vtx_to_e()
        self._e_to_vtx = dict()
        for i in self._vtx_to_e:
            for t in self._vtx_to_e[i]:
                if not t in self._e_to_vtx:
                    self._e_to_vtx[t] = list()
                self._e_to_vtx[t].append(i)

    def c_vtx_to_vtx(self):
        if not self._is_c_path:
            om.MGlobal.displayError('No set mesh name')
            return 0
        if not self._e_to_vtx:
            self.c_e_to_vtx()
        self._vtx_to_vtx = \
            {i: list(
                {s for t in self._vtx_to_e[i] for s in self._e_to_vtx[t]} - {i}
            )
                for i in self._vtx_to_e}
        # ԭ��
        # for i in self._vtx_to_e:
        #     vtx_to_vtx_set = {s for t in self._vtx_to_e[i] for s in self._e_to_vtx[t]}
        #     self._vtx_to_vtx[i] = list(vtx_to_vtx_set - {i})

    def get_vtx_to_e_connect(self):
        if not self._vtx_to_e:
            self.c_vtx_to_e()
        return self._vtx_to_e

    def get_e_to_vtx_connect(self):
        if not self._e_to_vtx:
            self.c_e_to_vtx()
        return self._e_to_vtx

    def get_vtx_to_vtx_connect(self):
        if not self._vtx_to_vtx:
            self.c_vtx_to_vtx()
        return self._vtx_to_vtx

    def get_vtx_path(self, vtx_id):
        if not self._is_c_path:
            om.MGlobal.displayError('No set mesh name')
            return 0
        if not self._vtx_to_vtx:
            self.c_vtx_to_vtx()
        if not vtx_id in self._vtx_to_vtx:
            om.MGlobal.displayError('point ID no in connect lsit')
            return 0
        # ����·���ֵ�
        vtx_path = dict()
        # ����ǰ��Ҫ�����ĵ��б�����Ϊ����ID��Ӧ�������б�
        crr_id_list = [vtx_id]
        # Ĭ�Ͻ����������Ϊ���еĵ�
        Already_id_list = list()
        # ��ʹ��.������������Ч�ʻ������
        append = Already_id_list.append
        # ����
        size = 0
        # ��������
        size_len_max = len(self._vtx_to_vtx)
        # ѭ��ֻҪ��ǰ��id�б�С��1 ���� �������ڵ��ڼ������޾�ֹͣ
        while len(crr_id_list) > 0 and size < size_len_max:
            test_id_dict = dict()
            [append(i) for i in crr_id_list]
            for i in crr_id_list:
                test_id_dict[i] = [t for t in self._vtx_to_vtx[i] if not t in Already_id_list]
                vtx_path[i] = size
            crr_id_list = [t for i in test_id_dict for t in test_id_dict[i]]
            size += 1
        return vtx_path
#����ƽ��
def reverseSmoothing(obj_list = None):
    for obj in obj_list if not obj_list is None else pm.selected():
        outputmaya.displayPrint('��������ƽ��:%s'%obj.nodeName())
        pm.select(obj.vtx[-1])
        pm.mel.ConvertSelectionToEdges()
        pm.mel.SelectEdgeLoopSp()
        pm.mel.polySelectEdgesEveryN('edgeRing',2)
        pm.mel.SelectEdgeLoopSp()
        pm.mel.SelectEdgeLoopSp()
        pm.mel.SelectEdgeLoopSp()
        pm.mel.polySelectEdgesEveryN('edgeRing',2)
        pm.polyDelEdge(cv=True,ch=False)
        outputmaya.displayPrint('����ƽ�� %s ���'%obj.nodeName())