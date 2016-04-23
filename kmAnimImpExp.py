# -*- coding: utf-8 -*-
###############################################################################
## 
#  @file	kmAnimImpExp.py
#  @brief	AnimファイルとSelectファイル同時書き出し
#  @version	1.0.1
#  @date	2016/04/23
#  @note	- edit
#  					- cleanup
#  @todo	
#  
###############################################################################
import os
import maya.cmds as mc
import maya.mel as mm
###############################################################################
if not mc.pluginInfo("animImportExport",q=True,loaded=True):
	mc.loadPlugin( 'animImportExport' )
	mc.pluginInfo( 'animImportExport', edit=True, autoload=True )
###############################################################################
def main():
	mc.python('from kmAnimImpExp import *')

	if mc.window( 'AnimImpExpUI', exists=True ):
		mc.deleteUI('AnimImpExpUI')
		
	WinName = mc.window( 
		'AnimImpExpUI', 
		title='Anim Import/Export with select', 
		iconName='AnimImpExpUI', 
		width=100, 
		height=200,
		menuBar=True
	)
	mc.menu( label='Menu', tearOff=False )
	mc.menuItem( label='Reload',command='from kmAnimImpExp import *;main()')
	mc.menuItem( divider=True )
	mc.menuItem( label='Quit' )
	
	mc.columnLayout(adj=True)
	mc.button(label='Import Anim',command='kmAnimImp()')
	mc.button(label='Export Anim',command='kmAnimExp()')
	mc.setParent('..') #columnLayout
		
	mc.showWindow(WinName)
	
###############################################################################
## 
#  @brief	Brief
#  
#  @return	Return_Description
#  
#  @details	Details
#  
def kmAnimImp():
	#select controllers
	strAnimFile = kmAnimFilePath( 1, 'animImport(*.anim)', 'anim', 'Load Key Animation')
	if strAnimFile == '':
		return
		
	strSelectFile = strAnimFile.replace('.anim', '.mel')
	
	mm.eval('source "' + strSelectFile + '";') 
	
	mc.file(
		strAnimFile,
		force=True,
		type='animImport',
		i=True,
		ignoreVersion=True,
		renameAll=True,
		options='targetTime=4;option=replace;connect=0'
	)
	
###############################################################################
## 
#  @brief	Brief
#  
#  @return	Return_Description
#  
#  @details	Details
#  
def kmAnimExp():
	#get export full path
	strAnimFile = kmAnimFilePath(0, ('animExport(*.anim)'), 'anim', 'Save Key Animation')
	if strAnimFile == '':
		return
		
	strSelectFile = strAnimFile.replace('.anim','.mel')
	
	#get range
	iStart = mc.playbackOptions(q=True,min=True)
	iEnd = mc.playbackOptions(q=True,max=True)
	
	#export animFile
	mc.file(
		strAnimFile,
		force=True, 
		exportSelectedAnim=True, 
		type='animExport',
		options=('options=keys;hierarchy=none;precision=8;intValue=17;nodeNames=1;verboseUnits=0;whichRange=1;range='+str(iStart)+':'+str(iEnd)+';'+'helpPictures=0;useChannelBox=0;controlPoints=0;shapes=0;copyKeyCmd=-animation objects -option keys -hierarchy none -controlPoints 0 -shape 0')
	)
	
	# #expor select file
	kmExportSelects(strSelectFile)

###############################################################################
## 
#  @brief	Brief
#  
#  @param	[in]	iFileMode 
#  @param	[in]	strFileFilter		ex) 'nimImport(*.anim)
#  @param	[in]	strSelectFilter	ex) anim
#  @param	[in]	strCaption		window title
#  @return	Return_Description
#  
#  @details	Details
#  
def kmAnimFilePath( iFileMode, strFileFilter, strSelectFilter, strCaption):
	
	strlPath = []
	strlPath = mc.fileDialog2(
		fileMode=iFileMode,
		fileFilter=strFileFilter, 
		selectFileFilter=strSelectFilter, 
		dialogStyle=2,
		caption=strCaption
	)
	
	try:
		if len(strlPath) > 0:
			return strlPath[0]
	except:
		return ''

###############################################################################
def kmExportSelects( strFullPath ):
	strlData = []
	strlData = mc.ls(sl=True)

	strlData.insert(0, 'select -r')
	strlData.append(';')
	strData = '\r\n'.join(strlData)
	
	f = open(strFullPath, 'w') 
	f.write(strData) 
	f.close() 

###############################################################################
