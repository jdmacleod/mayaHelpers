import os
import json
import maya.cmds as cmds

tempDir = os.environ.get('TMP', '/tmp')

attrFile = tempDir+'/mhSavedView.json'

def mhSaveView(viewToSave='active'):
	if viewToSave=='active':
		activePanel = cmds.getPanel( withFocus=True )
		if cmds.modelPanel( activePanel, exists=True):
			viewCam = cmds.modelPanel ( activePanel, query=True, camera=True )
		else:
			cmds.error('Active panel %s is not a modelPanel: can not save view.' % activePanel)
	else:
		viewCam=viewToSave

	if cmds.objExists(viewCam)==False:
		cmds.error('Can not find camera %s to save view.' % viewCam)

	attrNames = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']
	camAttrs = {}
	for attr in attrNames:
		thisAttr = '%s.%s'%(activeCam,attr)
		camAttrs[thisAttr] = cmds.getAttr(thisAttr)
	try:
		with open(attrFile, 'w') as fp:
			json.dump(camAttrs, fp)
			fp.close()
	except IOError:
		cmds.error('Could not open file %s for writing.' % attrFile)


def mhLoadView():
	try:
		with open(attrFile, 'r') as fp:
			savedAttrs = json.load(fp)
			fp.close()

		for attr in savedAttrs.keys():
			cmds.setAttr(attr, savedAttrs[attr])

	except IOError:
		cmds.error('Could not open file %s for reading.' % attrFile)

