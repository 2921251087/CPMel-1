#!/usr/bin/python
# encoding:gbk
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

#����PyQt���ڶ���������Ϊmaya���Ӵ���
def setMayaWindow(win):
    mui = wrapInstance(long(omui.MQtUtil.mainWindow()),QWidget)
    win.setParent(mui)
    win.setWindowFlags(Qt.Window)
