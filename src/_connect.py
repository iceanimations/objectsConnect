'''
Created on Jan 7, 2015

@author: qurban.ali
'''
import pymel.core as pc
import appUsageApp
import msgBox
import qtify_maya_window as qtfy
from PyQt4.QtGui import QMessageBox

def connect():
    objects = pc.ls(sl=True)
    if not objects:
        pc.warning('No selection found in the scene')
        return
    
    if len(objects) != 2:
        pc.warning('Select 2 objects only (One mesh and one set)')
        return
    
    try:
        _set = pc.ls(objects, type=pc.nt.ObjectSet)[0]
    except IndexError:
        pc.warning('Set not found in the selection')
        return
    
    for obj in objects:
        if not pc.hasAttr(obj, 'forCache'):
            pc.addAttr(obj, shortName='forCache', longName='forCache', at='message')
    
    objects.remove(_set)
    mesh = objects[0]
    
    if pc.polyEvaluate(_set, f=True) != pc.polyEvaluate(mesh, f=True):
        msgBox.showMessage(qtfy.getMayaWindow(), title='Compatibility Error',
                           msg='Selected objects are not compatible',
                           icon=QMessageBox.Information)
        return
    
    try:
        _set.forCache.disconnect()
        _set.forCache.connect(mesh.forCache)
    except Exception as ex:
        pc.confirmDialog(title='Error', message=str(ex), button='Ok')
        return
    
    pc.inViewMessage(amg='<hl>Objects connected successfully</hl>', pos='midCenter', fade=True )
    
    appUsageApp.updateDatabase('ObjectsConnect')