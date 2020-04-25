"""mhUserColorUI.py: helper UI for assigning user defined colors in Maya."""

import maya.cmds as cmds

def mhUserColorUI():
	if cmds.window('userColorUI', exists=True):
		cmds.deleteUI('userColorUI')
	window = cmds.window('userColorUI', title='User Color Helper', resizeToFitChildren=True)
	layout = cmds.columnLayout('userColorUILayout', adjustableColumn=True, parent=window)
	for idx in range(1,9):
		mhCreateRGBSlider(idx, layout)
	cmds.separator(parent=layout)
	cmds.button(parent=layout, label='Clear Assigned User Colors (Selected)', command='mhClearUserColor()')
	cmds.showWindow(window)

def mhSetUserColor(udColor):
	objs = cmds.ls(sl=True)
	cmds.color (objs, ud=udColor)

def mhClearUserColor():
	objs = cmds.ls(sl=True)
	cmds.color (objs)

def mhCreateRGBSlider(udColorIndex, parentLayout):
	rgbValue = cmds.displayRGBColor('userDefined%d'%udColorIndex, query=True)
	cmds.colorSliderButtonGrp('mhCustomColorButtonGrp%d'%udColorIndex, parent=parentLayout, label='userColor %d'%udColorIndex, buttonCommand='mhSetCustomColor(%d)'%udColorIndex, buttonLabel='assign', rgb=rgbValue, symbolButtonDisplay=False, changeCommand='mhUpdateCustomColor(%d)'%udColorIndex)

def mhUpdateUserColor(udColorIndex):
	rgbValue = cmds.colorSliderButtonGrp('mhCustomColorButtonGrp%d'%udColorIndex, query=True, rgb=True)

	cmds.displayRGBColor('userDefined%d'%udColorIndex, rgbValue[0], rgbValue[1], rgbValue[2])

