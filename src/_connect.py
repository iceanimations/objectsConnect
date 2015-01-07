'''
Created on Jan 7, 2015

@author: qurban.ali
'''
import pymel.core as pc
import appUsageApp

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
    
    _set.forCache.disconnect()
    _set.forCache.connect(mesh.forCache)
    
    appUsageApp.updateDatabase('ObjectsConnect')