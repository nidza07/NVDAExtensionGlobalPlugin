# globalPlugins\NVDAExtensionGlobalPlugin\speechHistory\__init__.py
# A part of NVDAExtensionGlobalPlugin add-on
# Copyright (C) 2016 - 2021 paulber19
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import addonHandler
from logHandler import log
try:
	# for nvda version >= 2021.1
	from speech import speech as speech
except ImportError:
	import speech
import tones
import ui
import api
from ..utils.informationDialog import InformationDialog
from ..settings import toggleSpeechRecordWithNumberOption, toggleSpeechRecordInAscendingOrderOption  # noqa:E501

addonHandler.initTranslation()

# constants
MAX_RECORD = 200
# global variables
_speechRecorder = None
_oldSpeak = None
_oldSpeakSpelling = None


def mySpeak(sequence, *args, **kwargs):
	_oldSpeak(sequence, *args, **kwargs)
	text = " ".join([x for x in sequence if isinstance(x, str)])
	_speechRecorder.record(text)


def mySpeakSpelling(text, *args, **kwargs):
	_oldSpeakSpelling(text, *args, **kwargs)
	_speechRecorder.record(text)


def initialize():
	global _speechRecorder, _oldSpeak, _oldSpeakSpelling
	if _speechRecorder is not None:
		return
	_speechRecorder = SpeechRecorderManager()
	_oldSpeak = speech.speak
	_oldSpeakSpelling = speech.speakSpelling
	speech.speak = mySpeak
	speech.speakSpelling = mySpeakSpelling
	log.warning("speechHistory initialized")


def terminate():
	global _speechRecorder
	if _speechRecorder is None:
		return
	speech.speak = _oldSpeak
	speech.speakSpelling = _oldSpeakSpelling
	_speechRecorder = None


def getSpeechRecorder():
	return _speechRecorder


def isActive():

	return _speechRecorder is not None


class SpeechRecorderManager(object):
	def __init__(self):
		self._speechHistory = []
		self._lastSpeechHistoryReportIndex = None
		self._onMonitoring = True

	def record(self, text):
		if not text or not self._onMonitoring:
			return
		text = text.replace("\r", "")
		text = text.replace("\n", "")
		if len(text.strip()) == 0:
			return
		self._speechHistory.append(text)
		if len(self._speechHistory) > MAX_RECORD:
			self._speechHistory.pop(0)
		self._lastSpeechHistoryReportIndex = len(self._speechHistory)-1

	def reportSpeechHistory(self, position, toClip=False):
		oldOnMonitoring = self._onMonitoring
		self._onMonitoring = False
		if len(self._speechHistory) == 0:
			# Translators: message to user to report no speech history record.
			ui.message(_("There is No speech announcement recorded"))
			self._onMonitoring = oldOnMonitoring
			return
		index = self._lastSpeechHistoryReportIndex
		if position == "previous" and index > 0:
			index -= 1
		elif position == "next" and index < len(self._speechHistory) - 1:
			index += 1
		if (position != "current") and (index == self._lastSpeechHistoryReportIndex):
			tones.beep(100, 40)
		self._lastSpeechHistoryReportIndex = index
		text = self._speechHistory[index]
		ui.message(text)
		api.copyToClip(text)
		self._onMonitoring = oldOnMonitoring

	def displaySpeechHistory(self):
		text = []
		for index in range(0, len(self._speechHistory)):
			s = self._speechHistory[index]
			if toggleSpeechRecordWithNumberOption(False):
				text.append(str(" {index}: {annonce}").format(
					index=index + 1, annonce=s))
			else:
				text .append(str(s))
		if not toggleSpeechRecordInAscendingOrderOption(False):
			text.reverse()
		text = "\r\n".join(text)

		# Translators: title of informations dialog.
		dialogTitle = _("Speech history")
		if toggleSpeechRecordInAscendingOrderOption(False):
			insertionPointOnLastLine = True
		else:
			insertionPointOnLastLine = False
		# Translators: label of information area.
		informationLabel = _("Records:")
		InformationDialog.run(
			None, dialogTitle, informationLabel, text, insertionPointOnLastLine)
