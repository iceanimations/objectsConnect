'''
Created on Jan 7, 2015

@author: qurban.ali
'''
import pymel.core as pc
import appUsageApp
import qtify_maya_window as qtfy
from uiContainer import uic
from PyQt4.QtGui import QMessageBox, QFileDialog
import msgBox
import os.path as osp

root_path = osp.dirname(osp.dirname(__file__))
ui_path = osp.join(root_path, 'ui')

Form, Base = uic.loadUiType(osp.join(ui_path, 'main.ui'))
class LD(Form, Base):
    def __init__(self, parent=qtfy.getMayaWindow()):
        super(LD, self).__init__(parent)
        self.setupUi(self)
        
        self.addButton.clicked.connect(self.add)
        self.browseButton.clicked.connect(self.setPath)
        
        appUsageApp.updateDatabase('AddLD')
        
    def setPath(self):
        filename = QFileDialog.getOpenFileName(self, 'Select File',
                                               '', '*.ma *.mb')
        if filename:
            self.pathBox.setText(filename)
        
    def setStatus(self, msg):
        self.statusBar().showMessage(msg, 2000)

    def add(self):
        
        objects = pc.ls(sl=True)
        if not objects:
            self.setStatus('No selection found in the scene')
            return
        
        if len(objects) > 1:
            self.setStatus('Select 1 object only (Maya object set)')
            return
        
        _set = objects[0]
        
        if not pc.hasAttr(_set, 'forCache'):
            pc.addAttr(_set, shortName='forCache', longName='forCache', niceName='LD', dt='string')
            
        # set the attribute
        path = self.getPath()
        if not path:
            return
        try:
            _set.forCache.set(path)
        except Exception as ex:
            msgBox.showMessage(self, title='Error', msg=str(ex),
                               icon=QMessageBox.Information)
            return
        
        pc.inViewMessage(amg='<hl>LD added successfully</hl>', pos='midCenter', fade=True )
        
        self.close()
    
    def getPath(self):
        path = self.pathBox.text()
        if not path:
            self.setStatus('Path not specified')
            return ''
        if not osp.exists(path):
            self.setStatus('Path does not exist')
            return ''
        if not osp.isfile(path):
            self.setStatus('Specified path is not a file')
            return ''
        if osp.splitext(path)[-1] not in ['.ma', '.mb']:
            self.setStatus('Specified file is not a Maya file')
            return ''
        return path
    
    def closeEvent(self, event):
        self.deleteLater()