import re
import maya.cmds as cmds

def mhNamerUI():
	if cmds.window('namerUI', exists=True):
		cmds.deleteUI('namerUI')
	window = cmds.window('namerUI', title='Naming Helper', resizeToFitChildren=True)
	layout = cmds.columnLayout('namerUILayout', adjustableColumn=True, parent=window)
	searchLayout = cmds.rowLayout('namerSearchLayout', adjustableColumn=1, numberOfColumns=2, parent=layout)
	searchTextGrp = cmds.textFieldGrp('namerSearchGrp', label='Search String:', adjustableColumn=2, parent=searchLayout) 
	findBtn = cmds.button('namerFindBtn', label='Find', command='mhNamerFindCB()', width=110, parent=searchLayout) 
	replaceLayout = cmds.rowLayout('namerReplaceLayout', adjustableColumn=1, numberOfColumns=2, parent=layout)
	replaceTextGrp = cmds.textFieldGrp('namerReplaceGrp', label='Replace String:', adjustableColumn=2, parent=replaceLayout) 
	searchReplaceBtn = cmds.button('namerSearchReplaceBtn', label='Find and Replace', command='mhNamerFindReplaceCB()', width=110, parent=replaceLayout) 
	cmds.separator(parent=layout)
	addPrefixLayout = cmds.rowLayout('namerAPLayout', adjustableColumn=1, numberOfColumns=2, columnAttach2=('both','both'), parent=layout)
	addPrefixGrp = cmds.textFieldGrp('namerAddPrefixGrp', label='Prefix to Add:', adjustableColumn=2, parent=addPrefixLayout)
	addPrefixBtn = cmds.button('namerAddPrefixBtn', label='Add Prefix', command='mhNamerAddPrefixCB()', width=110, parent=addPrefixLayout)
	addSuffixLayout = cmds.rowLayout('namerASLayout', adjustableColumn=1, numberOfColumns=2, parent=layout)
	addSuffixGrp = cmds.textFieldGrp('namerAddSuffixGrp', label='Suffix to Add:', adjustableColumn=2, parent=addSuffixLayout)
	addSuffixBtn = cmds.button('namerAddSuffixBtn', label='Add Suffix', command='mhNamerAddSuffixCB()', width=110, parent=addSuffixLayout)
	cmds.separator(parent=layout)
	newNameLayout = cmds.rowLayout('namerNNLayout', adjustableColumn=1, numberOfColumns=2, parent=layout)
	newNameTextLayout = cmds.columnLayout('namerNNTLayout', adjustableColumn=True, parent=newNameLayout)
	newNameGrp = cmds.textFieldGrp('namerNewNameGrp', label='New Name:', text='exampleName_###', adjustableColumn=2, parent=newNameTextLayout)
	newIndexGrp = cmds.textFieldGrp('namerNewIndexGrp', label='Start Index:', text='1', adjustableColumn=2, parent=newNameTextLayout)
	newNameBtn = cmds.button('namerNewNameBtn', label='Rename', command='mhNamerRenameCB()', width=110, parent=newNameLayout) 
	cmds.separator(parent=layout)
	conformShapesLayout = cmds.rowLayout('namerCSLayout', adjustableColumn=1, numberOfColumns=2, columnAttach2=('both','both'), parent=layout)
	conformShapesTxt = cmds.text('namerConformShapesTxt', label='Conform shape names to "transform"-->"transformShape"', parent=conformShapesLayout)
	conformShapesBtn = cmds.button('namerConformShapesBtn', label='Conform Shapes', command='mhConformShapeNames()', width=110, parent=conformShapesLayout)
	cmds.showWindow(window)

def mhNamerFindCB():
	searchStr = cmds.textFieldGrp('namerSearchGrp', text=True, query=True)	
	if searchStr:
		objs = cmds.ls( selection=True, flatten=True, dag=True )
		matchedObjs = []
		p = re.compile(searchStr)
		for objName in objs:
			if cmds.objExists(objName):
				if p.search(objName):
					matchedObjs.append(objName)
		cmds.select(matchedObjs)	

def mhNamerFindReplaceCB():
        searchStr = cmds.textFieldGrp('namerSearchGrp', text=True, query=True)
        if searchStr:
		replaceStr = cmds.textFieldGrp('namerReplaceGrp', text=True, query=True)
		mhSearchReplaceNames(searchStr, replaceStr)

def mhNamerAddPrefixCB():
        prefixStr = cmds.textFieldGrp('namerAddPrefixGrp', text=True, query=True)
        if prefixStr:
		mhAddNamePrefix(prefixStr)

def mhNamerAddSuffixCB():
        suffixStr = cmds.textFieldGrp('namerAddSuffixGrp', text=True, query=True)
        if suffixStr:
		mhAddNameSuffix(suffixStr)

def mhNamerRenameCB():
        newNameStr = cmds.textFieldGrp('namerNewNameGrp', text=True, query=True)
        if newNameStr:
		indexStart = int(cmds.textFieldGrp('namerNewIndexGrp', text=True, query=True))
		if indexStart is None or indexStart < 1 or not indexStart:
			indexStart = 1
		mhRenameRenumber(newNameStr,indexStart)

def mhConformShapeNames():
	shapes = cmds.ls( selection=True, geometry=True, flatten=True, shapes=True, dag=True, noIntermediate=True ) 
	for shape in shapes:
		shapeParent = cmds.listRelatives( shape, parent=True )[0]
		conformedShapeName = '%sShape' % shapeParent	
		if shape != conformedShapeName:
			print('%s --> %s' % (shape, conformedShapeName))
			cmds.rename(shape, conformedShapeName)

def mhSearchReplaceNames(searchStr, replaceStr):
	objs = cmds.ls( selection=True, flatten=True, dag=True )
	p = re.compile(searchStr)
	for objName in objs:
		if cmds.objExists(objName):
			newObjName = p.sub(replaceStr, objName)
			if newObjName != objName:
				print('%s --> %s' % (objName, newObjName))
				cmds.rename(objName, newObjName)
	mhConformShapeNames()

def mhAddNamePrefix(prefix):
        objs = cmds.ls( selection=True, flatten=True, dag=True )
        p = re.compile('^%s' % prefix)
        for objName in objs:
                if cmds.objExists(objName):
                        if p.match(objName) == None:
				newObjName = '%s%s' %(prefix, objName)
                                print('%s --> %s' % (objName, newObjName))
                                cmds.rename(objName, newObjName)
        mhConformShapeNames()

def mhAddNameSuffix(suffix):
        transforms = cmds.ls( selection=True, flatten=True, dag=True, exactType='transform' )
        p = re.compile('%s$' % suffix)
        for transformName in transforms:
                if cmds.objExists(transformName):
                        if p.search(transformName) == None:
                                newtransformName = '%s%s' %(transformName, suffix)
                                print('%s --> %s' % (transformName, newtransformName))
                                cmds.rename(transformName, newtransformName)
        mhConformShapeNames()

def mhRenameRenumber(newName,indexStart=1):
        transforms = cmds.ls( selection=True, flatten=True, dag=True, exactType='transform' )
	padding = newName.count('#')
	index = max(indexStart, 0)
	p = re.compile('#+')
	for transformName in transforms:
                if cmds.objExists(transformName):
			padIndex = str(index).zfill(padding)
			newtransformName = p.sub(padIndex, newName)
			print('%s --> %s' % (transformName, newtransformName))
			cmds.rename(transformName, newtransformName)
			index += 1
