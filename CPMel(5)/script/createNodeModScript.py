#!/usr/bin/python
#-*-coding:gbk -*-
'''
���ģ�����ṩ��createNodeModģ��ľ�̬�������Զ���������
����:maya2018��maya2018��׼python
'''
import pymel.core as pm
node_list_str = 'except:\n'
for i in pm.allNodeTypes(ia = False):
    node_list_str+='    def %s(*args,**kwargs):\n        return createNode(\'%s\',*args,**kwargs)\n'%(i,i)
print node_list_str