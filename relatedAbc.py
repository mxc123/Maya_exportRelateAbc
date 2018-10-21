#!usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author:MCC
@file: exportAbc
@time: 2018/09/18 10:03
"""
import sys
try:
    from PySide2 import QtWidgets as QtGui
    from PySide2 import QtCore
except ImportError:
    from PySide import QtGui
    from PySide import QtCore

class WindowsData(object):
    def __init__(self,windows):
        self._windows = windows
        import maya.cmds as cmds
        import maya.mel as mel

        self._cmds = cmds
        self._mel = mel

    def getMayaFileType(self,path):

        type = ''
        fileTyp = path.split(".")[-1]
        if fileTyp == "ma":
            type = "mayaAscii"
        elif fileTyp == "mb":
            type = "mayaBinary"
        elif fileTyp == "abc":
            type = "Alembic"

        return type

    def importMayaFile(self,path):
        typ = self.getMayaFileType(path)
        if typ:
            self._cmds.file(path,f=1, options="v=0;",ignoreVersion=1,typ=typ,o=1)
        #self._cmds.AbcImport(path, mode=1)

    def connectAbc(self,path):
        cmd = 'AbcImport -mode import -connect "/" "%s";' % path
        self._mel.eval(cmd)




    def chooseModel(self):
        text = QtGui.QFileDialog.getOpenFileName(self._windows, "Open File", "", "Files (*.abc)")
        self._windows.modelPathEdit.setText(text[0])

    def chooseAboutModel(self):
        text = QtGui.QFileDialog.getOpenFileName(self._windows, "Open File", "", "Files (*.abc)")
        self._windows.aboutModelEdit.setText(text[0])

    def okBtn(self):
        abcPath = self._windows.modelPathEdit.text()
        aboutPath = self._windows.aboutModelEdit.text()
        self.importMayaFile(abcPath)
        self.connectAbc(aboutPath)
        QtGui.QMessageBox.information(self._windows,"Message",u"关联成功")

    def cancleBtn(self):
        self._windows.done(0)

class MainWindows(QtGui.QDialog):
    def __init__(self,parent=None):
        super(MainWindows,self).__init__(parent)
        self._initUI()

    def _initUI(self):
        self.setWindowTitle(u"Maya关联abc")
        self.resize(600,250)
        modelAbcLabel = QtGui.QLabel(u"模型abc路径:")
        self.modelPathEdit = QtGui.QLineEdit()
        self.modelPathEdit.setPlaceholderText(u"选择模型Alembic文件")
        modelChooseBtn = QtGui.QPushButton(u"选择")

        labeltext = QtGui.QLabel(u"请选择带有动画的abc文件")
        labeltext.setAlignment(QtCore.Qt.AlignCenter)

        aboutModelLabel = QtGui.QLabel(u"关联abc路径:")
        self.aboutModelEdit = QtGui.QLineEdit()
        self.aboutModelEdit.setPlaceholderText(u"选择动画Alembic文件")
        aboutModelBtn = QtGui.QPushButton(u"选择")

        labelLayout = QtGui.QHBoxLayout()
        labelLayout.addWidget(modelAbcLabel)
        labelLayout.addWidget(self.modelPathEdit)
        labelLayout.addWidget(modelChooseBtn)

        aboutModelLayout = QtGui.QHBoxLayout()
        aboutModelLayout.addWidget(aboutModelLabel)
        aboutModelLayout.addWidget(self.aboutModelEdit)
        aboutModelLayout.addWidget(aboutModelBtn)

        okBtn = QtGui.QPushButton(u"确定")
        cancleBtn = QtGui.QPushButton(u"取消")

        btnLayout = QtGui.QHBoxLayout()
        #btnLayout.addStretch(1)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(cancleBtn)

        lastLayout = QtGui.QVBoxLayout()
        lastLayout.addLayout(labelLayout)
        #lastLayout.addWidget(labeltext)
        lastLayout.addLayout(aboutModelLayout)
        lastLayout.addLayout(btnLayout)
        self.setLayout(lastLayout)
        self._windowsData = WindowsData(self)
        modelChooseBtn.clicked.connect(self._windowsData.chooseModel)
        aboutModelBtn.clicked.connect(self._windowsData.chooseAboutModel)
        okBtn.clicked.connect(self._windowsData.okBtn)
        cancleBtn.clicked.connect(self._windowsData.cancleBtn)



if __name__ == "__main__":
    #app = QtGui.QApplication(sys.argv)
    windows = QtGui.QApplication.activeWindow()
    mainWindows = MainWindows(windows)
    mainWindows.show()
    #sys.exit(app.exec_())





