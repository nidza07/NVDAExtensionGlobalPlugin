# -*- coding: UTF-8 -*-
#onInstall.py
#A part of NVDAExtensionGlobalPlugin add-on
#Copyright (C) 2016  paulber19
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import addonHandler
addonHandler.initTranslation()
from logHandler import log
import os
import globalVars
import characterProcessing
from characterProcessing import SpeechSymbolProcessor
import codecs
import gui
import winUser
from languageHandler import curLang

addonPath = os.path.abspath(os.path.dirname(__file__))
addonName= addonPath.split("\\")[-1]
addonName = addonName.split(".")[0]
userPath = os.path.abspath(os.path.join(globalVars.appArgs.configPath, ""))
addonNewSymbolsPath = os.path.join(addonPath,"newSymbols") 

def getNewSymbolsFile(folder):
	lang = curLang
	if "_" in curLang:
		lang = curLang.split("_")[0]
	
	newSymbolsFileName = "symbols-" +lang + ".dic"
	newSymbolsFileList = os.listdir(folder)
	if newSymbolsFileName in newSymbolsFileList:
		return newSymbolsFileName.encode("utf-8")
	
	return None

def getSymbolsFilesList(folder):
	itemList = os.listdir(folder)
	FilesList = []
	for item in itemList:
		theFile = os.path.join(folder,item)
		if not(os.path.isdir(theFile))\
			and (os.path.splitext(theFile)[1] in {".dic"}) :
			FilesList.append(item)
	
	return FilesList


def getNewSymbols(symbolsFile):
	locale = symbolsFile[:-4].split("-")[-1]
	localSymbolProcessor = SpeechSymbolProcessor(locale)
	computedSymbols = localSymbolProcessor.computedSymbols
	userSymbols=  localSymbolProcessor.userSymbols.symbols	
	symbolsList = []
	src = codecs.open( symbolsFile , "r","utf_8",errors="replace")
	for sLine in src:
		if sLine.isspace() or sLine.startswith('#') or "symbols:" in sLine:
			continue
	
		line=sLine.rstrip('\r\n')
		temp=line.split("\t")
		if len(temp) > 1:
			identifier=temp.pop(0)
			if not (identifier in computedSymbols or identifier in userSymbols):
				symbolsList.append(sLine)
	
	src.close()
	return symbolsList

def mergeNewSymbolsWithUserSymbols(symbolsFile):
	newSymbolsFile = os.path.join(addonNewSymbolsPath, symbolsFile)
	userSymbolsFile= os.path.join(userPath, symbolsFile)
	symbolsList= getNewSymbols(newSymbolsFile)
	if len(symbolsList) == 0:
		return
	dest = codecs.open(userSymbolsFile,"r","utf_8",errors="replace")
	# find  last line 
	for sLine in dest:
		lastLine = sLine

	dest.close()


	dest = codecs.open(userSymbolsFile,"a","utf_8",errors="replace")
	if "lastLine" not in locals():
		dest.write("symbols:\n")

	elif not lastLine.isspace():
		dest.write("\n")
	dest.write("# Adding by %s addon\n" %addonName )
	for line in symbolsList:
		dest.write(line)
	
	dest.write("\n# End of adding")
	dest.close()


def installNewSymbols():
	newSymbolsFile = getNewSymbolsFile(addonNewSymbolsPath)
	if newSymbolsFile == None:
		return 
		
	userSymbolsFileList = getSymbolsFilesList(userPath)
	if newSymbolsFile not in userSymbolsFileList:
		# create new symbol file in user  folder
		fileName = os.path.join(userPath,newSymbolsFile)
		f = codecs.open( fileName, "w","utf_8",errors="replace")
		f.write("symbols:")
		f.close()
		
	mergeNewSymbolsWithUserSymbols(newSymbolsFile)

def checkWindowListAddonInstalled ():
	h = winUser.getForegroundWindow()
	for addon in addonHandler.getRunningAddons():
		if addon.manifest["name"]  in ["fakeClipboardAnouncement", "listDesFenetres", "ListeIconesZoneNotification", "DitDossierOuvrirEnregistrer"] :
			# Translators: message of message box
			gui.messageBox(_("Attention, you must uninstall %s addon because it is now included in this addon.") % addon.manifest["name"])
			break
			
	winUser.setForegroundWindow(h)

