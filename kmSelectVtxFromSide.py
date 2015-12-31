# -*- coding: utf-8 -*-
###############################################################################
##  
#  @file 		kmSelectVtxFromSide.py
#  @brief 		select Vertex from Side
#  @date		2015/04/29
#  @version	1.1.1
#  @note		cleanup
#    
#  @usage
#  	import kmSelectVtxFromSide as SVFS
#  	reload(SVFS)
#  	SVFS.main()
#  
###############################################################################
import maya.cmds as mc
###############################################################################
## 
#  @brief UI
#  
#  @return Return_Description
#  
#  @details Details
#  
def main():

	if mc.window( 'SelectVtxFromSideUI', exists=True ):
		mc.deleteUI('SelectVtxFromSideUI')
	WinName = mc.window( 'SelectVtxFromSideUI',title='Select Vertex From Side', iconName='SelectVtxFromSideUI' )
	
	mc.python( 'import kmSelectVtxFromSide as SVFS;reload(SVFS)' )
	mc.python( 'import maya.cmds as mc' )
	
	mc.columnLayout( adjustableColumn=True , parent=WinName)

	mc.checkBoxGrp(
		'cBG_plus',
		numberOfCheckBoxes=3, 
		label='', 
		labelArray3=['+X', '+Y', '+Z'] ,
		columnWidth=[(1,60),(2,60),(3,60)],
		onCommand1='mc.checkBoxGrp(\'cBG_minus\',edit=True, value1=False)',
		onCommand2='mc.checkBoxGrp(\'cBG_minus\',edit=True, value2=False)',
		onCommand3='mc.checkBoxGrp(\'cBG_minus\',edit=True, value3=False)'
	)
	mc.checkBoxGrp(
		'cBG_minus',
		numberOfCheckBoxes=3, 
		label='', 
		labelArray3=['-X', '-Y', '-Z'],
		columnWidth=[(1,60),(2,60),(3,60)],
		onCommand1='mc.checkBoxGrp(\'cBG_plus\',edit=True, value1=False)',
		onCommand2='mc.checkBoxGrp(\'cBG_plus\',edit=True, value2=False)',
		onCommand3='mc.checkBoxGrp(\'cBG_plus\',edit=True, value3=False)'
	)
	
	mc.rowColumnLayout( 
		'rCL_Extra',
		visible=False,
		numberOfColumns=2 , 
		columnWidth=[(1, 20), (2, 300)],
		columnAttach=[(1,'right',1),(2,'both',1)],
		rowAttach=[(1,'top',1),(2,'top',1)],
		parent=WinName
	)
	
	mc.checkBox(
		'cB_Extra',
		label='',
		onCommand='mc.floatFieldGrp(\'fFG_Extra\',edit=True, enable=True);mc.checkBoxGrp(\'cBG_plus\',edit=True,enable=False);mc.checkBoxGrp(\'cBG_minus\',edit=True,enable=False)',
		offCommand='mc.floatFieldGrp(\'fFG_Extra\',edit=True, enable=False);mc.checkBoxGrp(\'cBG_plus\',edit=True,enable=True);mc.checkBoxGrp(\'cBG_minus\',edit=True,enable=True)'
	)
	mc.floatFieldGrp( 
		'fFG_Extra',
		enable=False,
		numberOfFields=3, 
		label='Position', 
		value1=0, 
		value2=0,
		value3=0,
		columnWidth=[(1,60),(2,60),(3,60)],
		columnAttach=[(1,'both',1),(2,'both',1),(3,'both',1)]
	)
	mc.setParent('..') #rowColumnLayout
	
	mc.button(label='Select', command=('SVFS.getSVFSsetting()'))
	
	mc.setParent('..') #columnLayout
	
	mc.window( WinName,edit=True, width=300, height=60)
	
	mc.showWindow(WinName)
		
	return
###############################################################################
## 
#  @brief Brief
#  
#  @return Return_Description
#  
#  @details Details
#  
def getSVFSsetting():
	posX = 0
	posY = 0
	posZ = 0
	if( mc.checkBoxGrp('cBG_plus',q=True, value1=True) ):
		posX = 1
	elif( mc.checkBoxGrp('cBG_minus',q=True, value1=True) ):
		posX = -1
	elif ( mc.checkBox('cB_Extra',q=True, value=True ) ):
		posX = mc.floatFieldGrp('fFG_Extra', q=True, value1=True )
		
	if( mc.checkBoxGrp('cBG_plus',q=True, value2=True) ):
		posY = 1
	elif( mc.checkBoxGrp('cBG_minus',q=True, value2=True) ):
		posY = -1
	elif ( mc.checkBox('cB_Extra',q=True, value=True ) ):
		posY = mc.floatFieldGrp('fFG_Extra', q=True, value2=True )
		
	if( mc.checkBoxGrp('cBG_plus',q=True, value3=True) ):
		posZ = 1
	elif( mc.checkBoxGrp('cBG_minus',q=True, value3=True) ):
		posZ = -1
	elif ( mc.checkBox('cB_Extra',q=True, value=True ) ):
		posZ = mc.floatFieldGrp('fFG_Extra', q=True, value3=True )
		
	kmSelectVtxFromSide( mc.ls(sl=True, fl=True), [posX, posY, posZ] )
	return
	
###############################################################################
## 
#  @brief Brief
#  
#  @param [in] searchVtx Parameter_Description
#  @param [in] pos Parameter_Description
#  @return Return_Description
#  
#  @details Details
#  
def kmSelectVtxFromSide(searchVtx, pos):
	pX = []
	mc.select(clear=True)
	for vtx in searchVtx:
		
		vtxPos = mc.pointPosition(vtx)

		if pos[0] > 0:
			if vtxPos[0] > 0:
				pX.append( vtx )
		elif pos[0] < 0:
			if vtxPos[0] < 0:
				pX.append( vtx )
				
		if pos[1] > 0:
			if vtxPos[1] > 0:
				pX.append( vtx )
		elif pos[1] < 0:
			if vtxPos[1] < 0:
				pX.append( vtx )
				
		if pos[2] > 0:
			if vtxPos[2] > 0:
				pX.append( vtx )
		elif pos[2] < 0:
			if vtxPos[2] < 0:
				pX.append( vtx )
				
	mc.select( pX )
###############################################################################
