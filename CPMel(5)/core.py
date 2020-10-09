#!/usr/bin/python
#-*-coding:gbk -*-
'''
���������ģ�����ṩ��һЩ��Ҫ�Ĺ���
addCommand #������������ӵ����������#
Command #������#
'''
import importMayaPlug
import maya.cmds as mc
import abc

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

class Command ( object ) :
    '''
    ������
    isCommand #�����Ƿ񱻴���Ĭ��False
    __init__(self,*args,**key) #���г�ʼ������Ӧ���ڴ˴���
    _redoIt(self) #�����Ĳ���
    _undoIt��self�� #�����Ĳ���
    ʾ����
        class TestCommand(Command):
            isCommand = True
            def __init__(self, print_a_str, print_b_str):
                print "doIt"
                self.print_a_str = print_a_str
                self.print_b_str = print_b_str
                self._carryOut()
            def _redoIt ( self ) :
                print self.print_a_str
            def _undoIt ( self ) :
                print self.print_b_str
    '''
    isCommand = False
    def _carryOut( self ) :
        addCommand ( self._redoIt , self._undoIt )
    def _redoIt ( self ) :
        pass
    def _undoIt ( self ) :
        pass
#�������ע�������
def getCommand():
    class_list = list()
    crr_class_list = [Command]
    test_list = list()
    while len(crr_class_list)>0:
        for i in crr_class_list:
            test_list = i.__subclasses__()
            [class_list.append(i) for i in test_list]
        crr_class_list = test_list
    return [i for i in class_list if i.isCommand]