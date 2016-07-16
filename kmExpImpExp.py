# -*- coding: utf-8 -*-
###############################################################################
## 
#  @file	kmExpImpExp.py
#  @brief	expression import/export
#  @version	0.2.0
#  @date	2016/07/16
#  @note	- edit
#  				- 改行処理（出す時改行コード(\r\n)入れて、入れる時\nにする
#  @todo	
#  
###############################################################################
import os
import os.path
import maya.cmds as mc
###############################################################################
g_tSL_expNode = ''
g_sF_expString = ''
###############################################################################
## 
#  @brief	Brief
#  
#  @return	Return_Description
#  
#  @details	Details
#  
def main():
	mc.python('from kmExpImpExp import *')
	
	global g_tSL_expNode
	global g_sF_expString
	
	if mc.window( 'ExpImpExpUI', exists=True ):
		mc.deleteUI('ExpImpExpUI')
	WinName = mc.window( 
		'ExpImpExpUI',
		title='Expression Import / Export', 
		iconName='ExpImpExpUI', 
		width=500 , 
		height=300,
		menuBar=True
	)
	mc.menu('ExpImpExpMenu',label='Menu', tearOff=False)
	mc.menuItem(label='Reload', sourceType='python',command='main()' )
	mc.menuItem(label='Quit',sourceType='python',command='mc.deleteUI(\'ExpImpExpUI\')')
	
	form = mc.formLayout(numberOfDivisions=100)
	
	g_tSL_expNode = mc.textScrollList(	allowMultiSelection=True )
	g_sF_expString = mc.scrollField( wordWrap=True, text='',editable=True )
	
	mc.textScrollList( g_tSL_expNode, edit=True, selectCommand=('update_sF_expString()') )
	
	btnImport = mc.button(label='Import',command='importExp()')
	btnExport = mc.button(label='Export',command='exportExp()')
	
	mc.formLayout( 
		form, 
		edit=True, 
		attachForm=[
			(g_tSL_expNode, 'top', 5), 
			(g_tSL_expNode, 'left', 5), 
			(g_tSL_expNode, 'right', 5), 
						
			(g_sF_expString, 'top', 5),
			(g_sF_expString, 'left', 5),
			(g_sF_expString, 'right', 5),
			# (g_sF_expString, 'bottom', 5),
			
			(btnImport, 'left', 5), 
			# (btnImport, 'right', 5), 
			(btnImport, 'bottom', 5), 
			
			# (btnExport, 'left', 5), 
			(btnExport, 'right', 5),
			(btnExport, 'bottom', 5), 

		], 
		attachControl=[
			(g_tSL_expNode, "bottom", 5, btnImport),
			(g_sF_expString, "bottom", 5, btnExport), 
			# (btnImport, "right", 5, btnExport), 
			# (txWarn, 'bottom', 5, None)
		], 
		attachPosition=[
				(g_tSL_expNode,'top', 0,0),
				(g_tSL_expNode, 'right', 5, 30), 
				
				(g_sF_expString, 'top', 0, 0),
				(g_sF_expString, 'left', 0, 30),
				
				# (btnImport,'top', 0,0),
				(btnImport, 'right', 5, 50), 
				
				# (btnExport, 'top', 0, 0),
				(btnExport, 'left', 0, 50),
			
				# (btnImport, 'bottom', 0, 0), 
				# (btnExport, 'bottom', 0, 0),
				
		], 
		# attachNone=[
			# (gL_option, 'top') ,
			# (txWarn, 'top')
		# ]
	)
	
	update_tSL_expNode( g_tSL_expNode )
	
	mc.showWindow( WinName )

###############################################################################
## 
#  @brief	Brief
#  
#  @param	[in]	tSL Parameter_Description
#  @return	Return_Description
#  
#  @details	Details
#  
def update_tSL_expNode( tSL ):
	expList = mc.ls(type='expression')
	
	mc.textScrollList( tSL, edit=True, removeAll=True)
	mc.textScrollList( tSL, edit=True, append=expList )
	
	
###############################################################################
## 
#  @brief	Brief
#  
#  @return	Return_Description
#  
#  @details	Details
#  
def update_sF_expString( ):
	global g_tSL_expNode
	global g_sF_expString
	strlSel = mc.textScrollList(g_tSL_expNode, q=True, si=True )
	expString = mc.expression( strlSel[0], q=True, string=True)
	
	mc.scrollField( g_sF_expString, edit=True, text=expString )

###############################################################################
## 
#  @brief	Brief
#  
#  @param	[in]	strCap    Parameter_Description
#  @param	[in]	strOKcap  Parameter_Description
#  @param	[in]	iFileMode Parameter_Description
#  @return	Return_Description
#  
#  @details	Details
#  
def getExpPath( strCap , strOKcap, iFileMode ):
	basicFilter = "*.txt"
	singleFilter = "All Files (*.*)"
	
	strlPath = mc.fileDialog2(
		caption=strCap,
		fileFilter=basicFilter, 
		dialogStyle=2,
		# selectFileFilter='txt',
		fileMode=iFileMode,
		okCaption=strOKcap,
	)
	
	return strlPath
###############################################################################
## 
#  @brief	Brief
#  
#  @return	Return_Description
#  
#  @details	Details
#  
def importExp():
	global g_tSL_expNode
	
	strlPath = getExpPath( 'Import Expression', 'Import', 4 )
	if strlPath[0] == None:
		pass
		
	for strPath in strlPath:
		#get expression name from file
		expName = os.path.basename( strPath )
		expName = os.path.splitext(expName)[0]
	
		if mc.objExists( expName ):
			mc.delete( expName )
		
		#file open
		f = open( strPath )
		tmpString = f.read()
		f.close()
		
		tmpString = tmpString.replace( '\r\n', '\n')
		mc.expression( name=expName, string=tmpString)
		
	update_tSL_expNode( g_tSL_expNode )

###############################################################################
## 
#  @brief	Brief
#  
#  @return	Return_Description
#  
#  @details	Details
#  
def exportExp():
	global g_tSL_expNode
	
	strlSel = mc.textScrollList(g_tSL_expNode, q=True, si=True )
	
	if strlSel == None:
		print ('Nothing Selected')
		return
	
	strlPath = getExpPath( '[Export Expression]::Select Export Directory', 'Export', 2 )
	
	if strlPath == None:
		return
	
	for strExp in strlSel:
		expString = mc.expression( strExp, q=True, string=True)
		expString = expString.replace( '\n', '\r\n')
	
		#file Output
		strPath = os.path.join( strlPath[0] , ( strExp + '.txt' ) )

		f = open( strPath , 'w')
		f.write(expString)
		f.close()
		
		print ( 'Exported : ' + strPath)
	
	
###############################################################################

