#NVDAExtensionGlobalPlugin/volumeControl/__init__.py
#A part of NVDAExtensionGlobalPlugin add-on
#Copyright (C) 2017-2019  paulber19
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
import addonHandler
addonHandler.initTranslation()
from logHandler import log
import speech
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import sys
import api
import appModuleHandler
from ..utils.py3Compatibility import getUtilitiesPath
sys.path.append(getUtilitiesPath())
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
del sys.path[-1]

def toggleProcessVolume(processName):
	""" Mutes or unmute process volume """
	try:
		sessions = AudioUtilities.GetAllSessions()
	except:
		# no supported 
		raise RuntimeError("AudioUtilities not supported on this system")
	for session in sessions:
		try:
			name = session.Process.name()
		except:
			continue
		if name == processName:
			volume = session.SimpleAudioVolume
			mute = volume.GetMute() 
			volume.SetMute(not mute, None)
			if volume.GetMute()  == False:
				speech.speakMessage(_("Volume on"))
			else:
				speech.speakMessage(_("volume off"))
			return
	speech.speakMessage(_("No audio controller for this application"))


def getSpeakerVolume():
	try:
		devices = AudioUtilities.GetSpeakers()
	except:
		# no supported 
		return None
	interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
	volume = cast(interface, POINTER(IAudioEndpointVolume))
	volumeLevel = volume.GetMasterVolumeLevelScalar()
	return volumeLevel
	
def setSpeakerVolume(withMin = False):
	from ..settings import _addonConfigManager 
	""" Unmute speaker volume if it's mute
	and set level volume to configured volume if it's lowest than configured min volume level """
	try:
		devices = AudioUtilities.GetSpeakers()
	except:
		# no supported 
		return False
	
	interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
	volume = cast(interface, POINTER(IAudioEndpointVolume))
	volumeLevel = volume.GetMasterVolumeLevelScalar()
	mute = volume.GetMute()
	if mute:
		volume.SetMute(0, None)
		log.warning(" Unmute master volume")
	minLevel = float(_addonConfigManager .getMinMasterVolumeLevel())/100
	if not withMin or (withMin and volumeLevel <= minLevel):
		level = float(_addonConfigManager .getMasterVolumeLevel())/100
		volume.SetMasterVolumeLevelScalar(level, None)
		log.warning("Master volume is set to %s" %_addonConfigManager .getMasterVolumeLevel())
	return True
def getNVDAVolume():
	try:
		sessions = AudioUtilities.GetAllSessions()
	except:
		# no supported
		return False
	for session in sessions:
		try:
			name = session.Process.name()
		except:
			continue
		if name.lower() == "nvda.exe":
			volume = session.SimpleAudioVolume
			volumeLevel = volume.GetMasterVolume()
			return volumeLevel
	return None
def setNVDAVolume(withMin = False):
	from ..settings import _addonConfigManager 
	try:
		sessions = AudioUtilities.GetAllSessions()
	except:
		# no supported
		return False
	for session in sessions:
		try:
			name = session.Process.name()
		except:
			continue
		if name.lower() == "nvda.exe":
			volume = session.SimpleAudioVolume
			mute = volume.GetMute() 
			if mute:
				volume.SetMute(not mute, None)
				log.warning("Unmute NVDA volume")
			volumeLevel = volume.GetMasterVolume()
			minLevel = float(_addonConfigManager.getMinNVDAVolumeLevel())/100
			if not withMin or (withMin and volumeLevel <= minLevel):
				levels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
				index = _addonConfigManager.getNVDAVolumeLevel()/10
				level = float(levels[index])
				volume.SetMasterVolume(level, None)
				log.warning("NVDA volume is set to %s"%level)
				
			return True
	return False
def changeFocusedAppVolume(action = "increase"):
	focus=api.getFocusObject()
	appName=appModuleHandler.getAppNameFromProcessID(focus.processID,True)
	if appName == "nvda.exe":
		speech.speakMessage(_("Unavailable for NVDA"))
		return
	from ..settings import _addonConfigManager , toggleReportVolumeChangeAdvancedOption
	try:
		sessions = AudioUtilities.GetAllSessions()
	except:
		# no supported
		return
	for session in sessions:
		try:
			name = session.Process.name()
		except:
			continue
		if name.lower() == appName.lower():
			volume = session.SimpleAudioVolume
			mute = volume.GetMute() 
			if mute:
				volume.SetMute(not mute, None)
			offset  = 0.015*_addonConfigManager.getVolumeChangeStepLevel()
			level = volume.GetMasterVolume() 
			if action == "increase":
				level = min(1, level+offset)
				# Translators: message to user to report volume change.
				msg = _("stronger")
			elif action == "decrease":
				level = max(0, level-offset)
				# Translators: message to user to report volume change.
				msg = _("strongest")
			elif action == "max":
				level = 1.0
				# Translators: message to user to report volume change.
				msg = _("max")
			elif action == "min":
				level = 0.0
				# Translators: message to user to report volume change.
				msg = _("min")
			else:
				# no action
				log.warning("changeFocusedAppVolume: %s action is not known"%action)
				return
			volume.SetMasterVolume(level, None)
			if toggleReportVolumeChangeAdvancedOption(False):
				speech.speakMessage(msg)
			log.warning("%s volume is set to %s"%(appName ,level))
			return


	
def changeSpeakersVolume(action = "increase"):
	from ..settings import _addonConfigManager , toggleReportVolumeChangeAdvancedOption
	try:
		devices = AudioUtilities.GetSpeakers()
	except:
		# no supported 
		return False
	
	interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
	volume = cast(interface, POINTER(IAudioEndpointVolume))
	mute = volume.GetMute()
	if mute:
		volume.SetMute(not mute, None)
		log.warning(" Unmute master volume")
	offset  = 0.010*_addonConfigManager.getVolumeChangeStepLevel()

	minLevel = float(_addonConfigManager .getMinMasterVolumeLevel())/100
	speakersVolume = volume.GetMasterVolumeLevelScalar()
	if action == "increase":
		level = min(1, speakersVolume +offset)
		# Translators: message to user to report volume change.
		msg = _("stronger")
	elif action == "decrease":
		level = max(minLevel, speakersVolume -offset)
		# Translators: message to user to report volume change.
		msg = _("strongest")
	elif action == "max":
		level = 1.0
		# Translators: message to user to report volume change.
		msg = _("max")		
	elif action == "min":
		level = float(_addonConfigManager .getMasterVolumeLevel())/100
		# Translators: message to user to report volume change.
		msg = _("min")
	else:
		log.warning("changeSpeakerVolume: %s action is not known"%action)
		return
	volume.SetMasterVolumeLevelScalar(level, None)
	newSpeakersVolume = volume.GetMasterVolumeLevelScalar()
	if newSpeakersVolume == speakersVolume:
		if newSpeakersVolume == 1:
			# Translators:  message to user whenthe maximum limit is reached.
			msg = _("At maximum")
		else:
			# Translators: message to user when minimum level is reached.
			msg = _("At minimum")

	if toggleReportVolumeChangeAdvancedOption(False):
		speech.speakMessage(msg)
		log.warning("Master volume is set to %s" %level)
	return True