# globalPlugins\NVDAExtensionGlobalPlugin\settings\dialog.py
# a part of NVDAExtensionGlobalPlugin add-on
# Copyright (C) 2016 - 2021 Paulber19
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import addonHandler
import globalVars
import wx
from gui.settingsDialogs import MultiCategorySettingsDialog, SettingsPanel
import gui
import core
import characterProcessing
import queueHandler
from ..settings import _addonConfigManager
from ..settings import *  # noqa:F403
from ..utils.NVDAStrings import NVDAString
from ..utils import makeAddonWindowTitle
from .addonConfig import *  # noqa:F403

addonHandler.initTranslation()


def askForNVDARestart():
	if gui.messageBox(
		# Translators: A message asking the user if they wish to restart NVDA as NVDAExtensionGlobalPlugin addon settings changes have been made.
		_("Some changes have been made. You must save the configuration and restart NVDA for these changes to take effect. Would you like to do it now?"),
		makeAddonWindowTitle(NVDAString("Restart NVDA")),
		wx.YES | wx.NO | wx.ICON_WARNING) == wx.YES:
		_addonConfigManager.saveSettings(True)
		queueHandler.queueFunction(queueHandler.eventQueue, core.restart)
		return
	gui.messageBox(
		# Translators: A message to user
		_("Don't forget to save the configuration for the changes to take effect !"),
		makeAddonWindowTitle(NVDAString("Warning")),
		wx.OK | wx.ICON_WARNING)


class FeaturesInstallationSettingsPanel(SettingsPanel):
	# Translators: This is the label for the Installed features dialog.
	title = _("Features's installation")

	def __init__(self, parent):
		self.title = makeAddonWindowTitle(self.title)
		super(FeaturesInstallationSettingsPanel, self).__init__(parent)

	def makeSettings(self, settingsSizer):
		installChoiceLabels = {
			C_DoNotInstall: _("Do not install"),
			C_Install: _("Install"),
			C_InstallWithoutGesture: _("Install without gesture"),
			}
		installChoice = [installChoiceLabels[x] for x in [C_DoNotInstall, C_Install, C_InstallWithoutGesture]]
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("Display &systray icons and running application windows list:")
		self.installSystrayIconsListFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installSystrayIconsListFeatureOptionBox .SetSelection(getInstallFeatureOption(ID_SystrayIconsAndActiveWindowsList))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("&Complex symbols edition help:")
		self.installComplexSymbolsFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installComplexSymbolsFeatureOptionBox .SetSelection(getInstallFeatureOption(ID_ComplexSymbols))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("&Focused application's informations:")
		self.installFocusedApplicationInformationsFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installFocusedApplicationInformationsFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_FocusedApplicationInformations))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("&Extended Virtual Buffer:")
		self.installExtendedVirtualBufferFeaturesOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice[:-1])
		self.installExtendedVirtualBufferFeaturesOptionBox .SetSelection(getInstallFeatureOption(ID_ExtendedVirtualBuffer))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("C&lipboard command announcement:")
		self.installClipboardCommandAnnouncementFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice[:-1])
		self.installClipboardCommandAnnouncementFeatureOptionBox .SetSelection(getInstallFeatureOption(ID_ClipboardCommandAnnouncement))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("""Anno&uncement of the preselected folder  in "Open", "Save", "Save as" dialog boxes:""")
		self.installCurrentFolderReportFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installCurrentFolderReportFeatureOptionBox .SetSelection(getInstallFeatureOption(ID_CurrentFolderReport))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("&NVDA's log Files:")
		self.installOpenCurrentOrOldNVDALogFileFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installOpenCurrentOrOldNVDALogFileFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_OpenCurrentOrOldNVDALogFile))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("Speech &history:")
		self.installSpeechHistoryFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installSpeechHistoryFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_SpeechHistory))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("&Keyboard keys renaming:")
		self.installKeyboardKeyRenamingFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice[:-1])
		self.installKeyboardKeyRenamingFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_KeyboardKeyRenaming))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("C&ommand keys selective announcement:")
		self.installCommandKeysSelectiveAnnouncementFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice[:-1])
		self.installCommandKeysSelectiveAnnouncementFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_CommandKeysSelectiveAnnouncement))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("Minute &timer:")
		self.installMinuteTimerFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installMinuteTimerFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_MinuteTimer))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("NVDA's &restart:")
		self.installRestartInDebugModeFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installRestartInDebugModeFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_RestartInDebugMode))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("Display visible items making up the foreground &object:")
		self.installForegroundWindowObjectsListFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installForegroundWindowObjectsListFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_ForegroundWindowObjectsList))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("&Voice profile switching:")
		self.installVoiceProfileSwitchingFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installVoiceProfileSwitchingFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_VoiceProfileSwitching))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("Ke&ys's remanence:")
		self.installKeyRemanenceFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice[:-1])
		self.installKeyRemanenceFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_KeyRemanence))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("Volu&me's control:")
		self.installVolumeControlFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice)
		self.installVolumeControlFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_VolumeControl))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("&Development's tools:")
		self.installDevToolsFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice[:-1])
		self.installDevToolsFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_Tools))
		# Translators: This is the label for a listbox in the FeaturesInstallation settings panel.
		labelText = _("&Date and time - supplements:")
		self.installDateAndTimeFeatureOptionBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=installChoice[:])
		self.installDateAndTimeFeatureOptionBox.SetSelection(getInstallFeatureOption(ID_DateAndTime))

	def saveSettingChanges(self):
		self.restartNVDA = False
		if self.installExtendedVirtualBufferFeaturesOptionBox.GetSelection() != getInstallFeatureOption(ID_ExtendedVirtualBuffer):
			setInstallFeatureOption(ID_ExtendedVirtualBuffer, self.installExtendedVirtualBufferFeaturesOptionBox.GetSelection())
			self.restartNVDA = True
			if getInstallFeatureOption(ID_ExtendedVirtualBuffer) == C_Install:
				# set LoopInNavigationModeOption to default state (False)
				if toggleLoopInNavigationModeOption(False):
					toggleLoopInNavigationModeOption(True)
		if self.installSystrayIconsListFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_SystrayIconsAndActiveWindowsList):
			setInstallFeatureOption(ID_SystrayIconsAndActiveWindowsList, self.installSystrayIconsListFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installComplexSymbolsFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_ComplexSymbols):
			setInstallFeatureOption(ID_ComplexSymbols, self.installComplexSymbolsFeatureOptionBox.GetSelection())
			self.restartNVDA = True
			if getInstallFeatureOption(ID_ComplexSymbols) == C_DoNotInstall:
				# set parameters to default values
				_addonConfigManager.setMaximumOfLastUsedSymbols(C_MaximumOfLastUsedSymbols)
				_addonConfigManager.deleceAllUserComplexSymbols()
		if self.installClipboardCommandAnnouncementFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_ClipboardCommandAnnouncement):
			setInstallFeatureOption(ID_ClipboardCommandAnnouncement, self.installClipboardCommandAnnouncementFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installCurrentFolderReportFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_CurrentFolderReport):
			setInstallFeatureOption(ID_CurrentFolderReport, self.installCurrentFolderReportFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installFocusedApplicationInformationsFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_FocusedApplicationInformations):
			setInstallFeatureOption(ID_FocusedApplicationInformations, self.installFocusedApplicationInformationsFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installOpenCurrentOrOldNVDALogFileFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_OpenCurrentOrOldNVDALogFile):
			setInstallFeatureOption(ID_OpenCurrentOrOldNVDALogFile, self.installOpenCurrentOrOldNVDALogFileFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installSpeechHistoryFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_SpeechHistory):
			setInstallFeatureOption(ID_SpeechHistory, self.installSpeechHistoryFeatureOptionBox.GetSelection())
			self.restartNVDA = True
			if getInstallFeatureOption(ID_SpeechHistory) == C_DoNotInstall:
				# set parameters to Default values
				if not toggleSpeechRecordWithNumberOption(False):
					toggleSpeechRecordWithNumberOption(True)
				if toggleSpeechRecordInAscendingOrderOption(False):
					toggleSpeechRecordInAscendingOrderOption(True)
		if self.installKeyboardKeyRenamingFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_KeyboardKeyRenaming):
			setInstallFeatureOption(ID_KeyboardKeyRenaming, self.installKeyboardKeyRenamingFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installCommandKeysSelectiveAnnouncementFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_CommandKeysSelectiveAnnouncement):
			setInstallFeatureOption(ID_CommandKeysSelectiveAnnouncement, self.installCommandKeysSelectiveAnnouncementFeatureOptionBox.GetSelection())
			self.restartNVDA = True
			if getInstallFeatureOption(ID_CommandKeysSelectiveAnnouncement) == C_DoNotInstall:
				# delete all command selective announcement feature configuration
				_addonConfigManager.deleceCommandKeyAnnouncementConfiguration()
		if self.installMinuteTimerFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_MinuteTimer):
			setInstallFeatureOption(ID_MinuteTimer, self.installMinuteTimerFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installForegroundWindowObjectsListFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_ForegroundWindowObjectsList):
			setInstallFeatureOption(ID_ForegroundWindowObjectsList, self.installForegroundWindowObjectsListFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installVoiceProfileSwitchingFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_VoiceProfileSwitching):
			setInstallFeatureOption(ID_VoiceProfileSwitching, self.installVoiceProfileSwitchingFeatureOptionBox.GetSelection())
			self.restartNVDA = True
			if getInstallFeatureOption(ID_VoiceProfileSwitching) == C_DoNotInstall:
				from ..switchVoiceProfile import SwitchVoiceProfilesManager
				SwitchVoiceProfilesManager().deleteAllProfiles()

		if self.installKeyRemanenceFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_KeyRemanence):
			setInstallFeatureOption(ID_KeyRemanence, self.installKeyRemanenceFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installRestartInDebugModeFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_RestartInDebugMode):
			setInstallFeatureOption(ID_RestartInDebugMode, self.installRestartInDebugModeFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installVolumeControlFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_VolumeControl):
			setInstallFeatureOption(ID_VolumeControl, self.installVolumeControlFeatureOptionBox.GetSelection())
			self.restartNVDA = True
			if getInstallFeatureOption(ID_VolumeControl) != C_DoNotInstall:
				# set parameters to default values
				if not toggleSetOnMainAndNVDAVolumeAdvancedOption(False):
					toggleSetOnMainAndNVDAVolumeAdvancedOption(True)
				_addonConfigManager.setMinMasterVolumeLevel(int(C_MinMasterVolumeLevel))
				_addonConfigManager.setMasterVolumeLevel(C_MasterVolumeLevel)
				_addonConfigManager.setMinNVDAVolumeLevel(int(C_MinNVDAVolumeLevel))
				_addonConfigManager.setNVDAVolumeLevel(int(C_NVDAVolumeLevel))
		if self.installDevToolsFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_Tools):
			setInstallFeatureOption(ID_Tools, self.installDevToolsFeatureOptionBox.GetSelection())
			self.restartNVDA = True
		if self.installDateAndTimeFeatureOptionBox.GetSelection() != getInstallFeatureOption(ID_DateAndTime):
			setInstallFeatureOption(ID_DateAndTime, self.installDateAndTimeFeatureOptionBox.GetSelection())
			if not getInstallFeatureOption(ID_DateAndTime) == C_Install:
				# set report time with second to default value
				if toggleReportTimeWithSecondsOption(False):
					toggleReportTimeWithSecondsOption(True)
			self.restartNVDA = True

	def onSave(self):
		self.saveSettingChanges()


class NVDAEnhancementSettingsPanel(SettingsPanel):
	# Translators: This is the label for the settings dialog.
	title = _("NVDA enhancements")

	def __init__(self, parent):
		self.title = makeAddonWindowTitle(self.title)
		super(NVDAEnhancementSettingsPanel, self).__init__(parent)

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is the label for a group of editing options in the
		# NVDAEnhancement settings panel
		groupText = _("Editing")
		groupSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		sHelper.addItem(group)
		# bug fix in nvda 2020.3
		# so hide it for nvda version higher or equal  to this version
		# Translators: This is the label for a checkbox in the NVDAEnhancement settings panel.
		labelText = _("&Report next word on deletion")
		self.ReportNextWordOnDeletionOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.ReportNextWordOnDeletionOptionBox.SetValue(toggleReportNextWordOnDeletionOption(False))
		import versionInfo
		NVDAVersion = [versionInfo.version_year, versionInfo.version_major]
		if globalVars.appArgs.secure\
			or NVDAVersion >= [2020, 3]:
			self.ReportNextWordOnDeletionOptionBox .Hide()
		# Translators: This is the label for a comboBox in the NVDAEnhancement settings panel.
		labelText = _("maximum number of last &used symbols recorded:")
		choice = [x*10 for x in range(1, 11)]
		choice = list(reversed(choice))
		self.maximumOfLastUsedSymbolsBox = group.addLabeledControl(labelText, wx.Choice, choices=[str(x) for x in choice])
		self.maximumOfLastUsedSymbolsBox.SetSelection(choice.index(_addonConfigManager.getMaximumOfLastUsedSymbols()))
		if getInstallFeatureOption(ID_ComplexSymbols) == C_DoNotInstall:
			self.maximumOfLastUsedSymbolsBox.Disable()
		# Translators: This is the label for a group of cursor's movement options in the
		# NVDAEnhancement settings panel
		groupText = _("Cursor's moving")
		groupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		sHelper.addItem(group)
		# Translators: This is the label for a combobox in the NVDAEnhancement settings panel.
		labelText = _("&Punctuation/symbol level on word movement:")
		symbolLevelLabels = characterProcessing.SPEECH_SYMBOL_LEVEL_LABELS
		symbolLevelChoices = [symbolLevelLabels[level] for level in characterProcessing.CONFIGURABLE_SPEECH_SYMBOL_LEVELS]
		# Translators: This is the label for an item in combobox in the
		# NVDAEnhancement settings panel.
		symbolLevelChoices = [_("Current configuration profile's level"), ] + symbolLevelChoices[:]
		self.symbolLevelList = group.addLabeledControl(labelText, wx.Choice, choices=symbolLevelChoices)
		symbolLevelOnWordCaretMovement = _addonConfigManager .getSymbolLevelOnWordCaretMovement()
		if symbolLevelOnWordCaretMovement is None:
			self.symbolLevelList.SetSelection(0)
		else:
			self.symbolLevelList.SetSelection(1+characterProcessing.CONFIGURABLE_SPEECH_SYMBOL_LEVELS.index((symbolLevelOnWordCaretMovement)))
		# Translators: This is the label for a group in NVDAEnhancement settings panel
		groupText = _("Speech history")
		groupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		sHelper.addItem(group)
		# Translators: This is the label for a checkbox in the NVDAEnhancement settings panel.
		labelText = _("&Number the records ")
		self.speechRecordWithNumberOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.speechRecordWithNumberOptionBox.SetValue(toggleSpeechRecordWithNumberOption(False))
		# Translators: This is the label for a checkbox in the NVDAEnhancement settings panel.
		labelText = _("&Display records in ascending order")
		self.speechRecordInAscendingOrderOptionBox = group.addItem(wx.CheckBox(groupBox, wx.ID_ANY, label=labelText))
		self.speechRecordInAscendingOrderOptionBox.SetValue(toggleSpeechRecordInAscendingOrderOption(False))
		if getInstallFeatureOption(ID_SpeechHistory) == C_DoNotInstall:
			for item in range(0, group.sizer.GetItemCount()):
				group.sizer.Hide(item)
		# Translators: This is the label for a group NVDAEnhancement settings panel
		groupText = _("Browser")
		groupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		sHelper.addItem(group)
		# Translators: This is the label for a checkbox in the NVDAEnhancement settings panel.
		labelText = _("&Browse in loop")
		self.loopInNavigationModeOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.loopInNavigationModeOptionBox.SetValue(toggleLoopInNavigationModeOption(False))
		if getInstallFeatureOption(ID_ExtendedVirtualBuffer) == C_DoNotInstall:
			group.sizer.Hide(0)

	def saveSettingChanges(self):
		from . import _addonConfigManager
		self.restartNVDA = False
		if self.ReportNextWordOnDeletionOptionBox.IsChecked() != toggleReportNextWordOnDeletionOption(False):
			toggleReportNextWordOnDeletionOption()
			self.restartNVDA = True
		if self.symbolLevelList.GetSelection() == 0:
			_addonConfigManager .saveSymbolLevelOnWordCaretMovement(None)
		else:
			_addonConfigManager .saveSymbolLevelOnWordCaretMovement(characterProcessing.CONFIGURABLE_SPEECH_SYMBOL_LEVELS[self.symbolLevelList.GetSelection()-1])
		if self.speechRecordWithNumberOptionBox.IsChecked() != toggleSpeechRecordWithNumberOption(False):
			toggleSpeechRecordWithNumberOption()
		if self.speechRecordInAscendingOrderOptionBox.IsChecked() != toggleSpeechRecordInAscendingOrderOption(False):
			toggleSpeechRecordInAscendingOrderOption()
		if self.loopInNavigationModeOptionBox.IsChecked() != toggleLoopInNavigationModeOption(False):
			toggleLoopInNavigationModeOption()
		maximumOfLastUsedSymbols = int(self.maximumOfLastUsedSymbolsBox.GetString(self.maximumOfLastUsedSymbolsBox.GetSelection()))
		_addonConfigManager.setMaximumOfLastUsedSymbols(maximumOfLastUsedSymbols)

	def onSave(self):
		self.saveSettingChanges()


class ComputerSettingsPanel(SettingsPanel):
	# Translators: This is the label for the options settings dialog.
	title = _("Computer")

	def __init__(self, parent):
		self.title = makeAddonWindowTitle(self.title)
		super(ComputerSettingsPanel, self).__init__(parent)

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is the label for a group of editing options in the computer settings panel.
		groupText = _("Windows")
		groupSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		sHelper.addItem(group)
		# Translators: This is the label for a checkbox in the Computer settings panel.
		labelText = _("&No object description in Windows ribbons")
		self.noDescriptionReportInRibbonOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.noDescriptionReportInRibbonOptionBox.SetValue(toggleNoDescriptionReportInRibbonOption(False))
		if globalVars.appArgs.secure:
			self.noDescriptionReportInRibbonOptionBox .Hide()
		# Translators: This is the label for a checkbox in the Computer settings panel.
		labelText = _("Automatically &maximize windows")
		self.AutomaticWindowMaximizationOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.AutomaticWindowMaximizationOptionBox.SetValue(toggleAutomaticWindowMaximizationOption(False))
		# Translators: This is the label for a checkbox in the Computer settings panel.
		labelText = _("Report &windows clock's time with seconds")
		self.reportTimeWithSecondsOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.reportTimeWithSecondsOptionBox.SetValue(toggleReportTimeWithSecondsOption(False))
		if getInstallFeatureOption(ID_DateAndTime) == C_DoNotInstall:
			self.reportTimeWithSecondsOptionBox.Disable()

		# Translators: This is the label for a group in computer settings panel.
		groupText = _("Volume control")
		volumeGroup = gui.guiHelper.BoxSizerHelper(self, sizer=wx.StaticBoxSizer(wx.StaticBox(self, label=groupText), wx.VERTICAL))
		sHelper.addItem(volumeGroup)
		# Translators: This is the label for a group in computer settings panel.
		groupText = _("Main and NVDA volume")
		groupSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		volumeGroup.addItem(group)
		# Translators: This is the label for a checkbox in the computer settings panel.
		labelText = _("Set on &volume at the loading of the add-on")
		self.setOnMainAndNVDAVolumeOptionCheckBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.setOnMainAndNVDAVolumeOptionCheckBox.SetValue(toggleSetOnMainAndNVDAVolumeAdvancedOption(False))
		# Translators: This is the label for a group of main volume options in the computer settings panel.
		groupText = _("Main volume")
		groupSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		volumeGroup.addItem(group)
		# Translators: This is a label for a choice box in computer settings panel.
		labelText = _("&Threshold of recovery of the volume:")
		choice = [10 * x for x in reversed(list(range(0, 11)))]
		self.minMasterVolumeLevelBox = group.addLabeledControl(labelText, wx.Choice, choices=[str(x) for x in choice[5:]])
		self.minMasterVolumeLevelBox.SetSelection(choice[5:].index(_addonConfigManager.getMinMasterVolumeLevel()))
		# Translators: This is a label for a choice box in computer settings panel.
		labelText = _("Recovery &level:")
		self.masterVolumeLevelBox = group.addLabeledControl(labelText, wx.Choice, choices=[str(x) for x in choice])
		self.masterVolumeLevelBox.SetSelection(choice.index(_addonConfigManager.getMasterVolumeLevel()))
		# Translators: This is the label for a group of NVDA volume options in the computer settings panel.
		groupText = _("NVDA volume")
		groupSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		volumeGroup.addItem(group)
		# Translators: This is a label for a choice box in computer settings panel.
		labelText = _("T&hreshold of recovery of the volume:")
		self.minNVDAVolumeLevelBox = group.addLabeledControl(labelText, wx.Choice, choices=[str(x) for x in choice[5:]])
		self.minNVDAVolumeLevelBox.SetSelection(choice[5:].index(_addonConfigManager.getMinNVDAVolumeLevel()))
		# Translators: This is a label for a choice box in computer settings panel.
		labelText = _("&Recovery level:")
		self.NVDAVolumeLevelBox = group.addLabeledControl(labelText, wx.Choice, choices=[str(x) for x in choice[5:]])
		self.NVDAVolumeLevelBox.SetSelection(choice[5:].index(_addonConfigManager.getNVDAVolumeLevel()))
		# Translators: This is the label for a group in computer settings panel.
		groupText = _("Volume c&hange")
		groupSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		volumeGroup.addItem(group)
		# Translators: This is a label for a choice box in computer settings panel.
		labelText = _("Ste&ps's size:")
		choice = [str(x) for x in range(1, 21)]
		self.volumeChangeStepLevelBox = group.addLabeledControl(labelText, wx.Choice, choices=list(reversed(choice)))
		self.volumeChangeStepLevelBox.SetStringSelection(str(_addonConfigManager.getVolumeChangeStepLevel())	)
		# Translators: This is the label for a checkbox in the computer settings panel.
		labelText = _("R&eport volume changes")
		self.reportVolumeChangeOptionCheckBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.reportVolumeChangeOptionCheckBox.SetValue(toggleReportVolumeChangeAdvancedOption(False))
		# Translators: This is the label for a checkbox in the computer settings panel.
		labelText = _("&Announce application volume level in percent")
		self.appVolumeLevelAnnouncementInPercentOptionCheckBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.appVolumeLevelAnnouncementInPercentOptionCheckBox .SetValue(toggleAppVolumeLevelAnnouncementInPercentAdvancedOption(False))
		if not getInstallFeatureOption(ID_VolumeControl):
			for item in range(0, volumeGroup.sizer.GetItemCount()):
				volumeGroup.sizer.Hide(item)

	def saveSettingChanges(self):
		self.restartNVDA = False
		if self.noDescriptionReportInRibbonOptionBox.IsChecked() != toggleNoDescriptionReportInRibbonOption(False):
			toggleNoDescriptionReportInRibbonOption()
			self.restartNVDA = True
		if self.AutomaticWindowMaximizationOptionBox.IsChecked() != toggleAutomaticWindowMaximizationOption(False):
			toggleAutomaticWindowMaximizationOption()
		if getInstallFeatureOption(ID_DateAndTime) != C_DoNotInstall:
			if self.reportTimeWithSecondsOptionBox.IsChecked() != toggleReportTimeWithSecondsOption(False):
				toggleReportTimeWithSecondsOption()
		if self.setOnMainAndNVDAVolumeOptionCheckBox.IsChecked() != toggleSetOnMainAndNVDAVolumeAdvancedOption(False):
			toggleSetOnMainAndNVDAVolumeAdvancedOption()
		levelString = self.minMasterVolumeLevelBox.GetStringSelection()
		_addonConfigManager.setMinMasterVolumeLevel(int(levelString))
		levelString = self.masterVolumeLevelBox.GetStringSelection()
		_addonConfigManager.setMasterVolumeLevel(int(levelString))
		levelString = self.NVDAVolumeLevelBox.GetStringSelection()
		_addonConfigManager.setMinNVDAVolumeLevel(int(levelString))
		levelString = self.NVDAVolumeLevelBox.GetStringSelection()
		_addonConfigManager.setNVDAVolumeLevel(int(levelString))
		levelString = self.volumeChangeStepLevelBox.GetStringSelection()
		_addonConfigManager.setVolumeChangeStepLevel(int(levelString))
		if self.reportVolumeChangeOptionCheckBox.IsChecked() != toggleReportVolumeChangeAdvancedOption(False):
			toggleReportVolumeChangeAdvancedOption()
		if self.appVolumeLevelAnnouncementInPercentOptionCheckBox.IsChecked() != toggleAppVolumeLevelAnnouncementInPercentAdvancedOption(False):
			toggleAppVolumeLevelAnnouncementInPercentAdvancedOption(True)

	def onSave(self):
		self.saveSettingChanges()


class AdvancedSettingsPanel(SettingsPanel):
	# Translators: This is the label for the Advanced settings panel.
	title = _("advanced")
	_playSoundOnErrorsOptionLabels = [  # becarefull: order is important
		# Translators: This is a label for a choice item in Advanced options settings dialog.
		_("For No NVDA's version"),  # PSOE_NoVersion
		# Translators: This is a label for a choice item in Advanced options settings dialog.
		_("For Only the NVDA's snapshot versions"),  # PSOE_SnapshotVersions
		# Translators: This is a label for a choice item in Advanced options settings dialog.
		_("Only until the next NVDA restart"),  # PSOE_UntilNVDARestart
		# Translators: This is a label for a choice item in Advanced options settings dialog.
		_("For all NVDA's versions"),  # PSOE_AllVersions
		]

	def __init__(self, parent):
		self.title = makeAddonWindowTitle(self.title)
		super(AdvancedSettingsPanel, self).__init__(parent)

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is the label for a choice box in the advanced settings panel.
		labelText = _("&Play sound on logged errors:")
		self.playSoundOnErrorsOptionChoiceBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=self._playSoundOnErrorsOptionLabels)
		self.playSoundOnErrorsOptionChoiceBox.SetSelection(_addonConfigManager.getPlaySoundOnErrorsOption())
		# Translators: This is the label for a checkbox in the Advanced settings panel.
		labelText = _("&Title dialog with add-on name")
		self.dialogTitleWithAddonSummaryOptionBox = sHelper.addItem(wx.CheckBox(self, wx.ID_ANY, label=labelText))
		self.dialogTitleWithAddonSummaryOptionBox.SetValue(toggleDialogTitleWithAddonSummaryAdvancedOption(False))
		# Translators: This is the label for a comboBox in the advanced settings panel.
		labelText = _("&Delay between repeat of same gesture:")
		choice = [x for x in range(100, 3050, 50)]
		choice = list(reversed(choice))
		self.MaximumDelayBetweenSameScriptBox = sHelper.addLabeledControl(labelText, wx.Choice, choices=[str(x) for x in choice])
		self.MaximumDelayBetweenSameScriptBox.SetSelection(choice.index(_addonConfigManager.getMaximumDelayBetweenSameScript()))
		# Translators: This is the label for a checkbox in the Advanced settings panel.
		labelText = _("""&Do not take account of the option called "Report object descriptions" during the display of the dialog box same as confirmation""")
		self.byPassNoDescriptionOptionBox = sHelper.addItem(wx.CheckBox(self, wx.ID_ANY, label=labelText))
		self.byPassNoDescriptionOptionBox.SetValue(toggleByPassNoDescriptionAdvancedOption(False))
		if globalVars.appArgs.secure:
			self.MaximumDelayBetweenSameScriptBox .Hide()
			self.byPassNoDescriptionOptionBox.Hide()

	def saveSettingChanges(self):
		self.restartNVDA = False
		playSoundOnErrorsOption = self.playSoundOnErrorsOptionChoiceBox.GetSelection()
		_addonConfigManager.setPlaySoundOnErrorsOption(playSoundOnErrorsOption)
		if self.dialogTitleWithAddonSummaryOptionBox.IsChecked() != toggleDialogTitleWithAddonSummaryAdvancedOption(False):
			toggleDialogTitleWithAddonSummaryAdvancedOption()
		maximumDelayBetweenSameScript = int(self.MaximumDelayBetweenSameScriptBox.GetString(self.MaximumDelayBetweenSameScriptBox.GetSelection()))
		if maximumDelayBetweenSameScript != _addonConfigManager.getMaximumDelayBetweenSameScript():
			_addonConfigManager.setMaximumDelayBetweenSameScript(maximumDelayBetweenSameScript)
			self.restartNVDA = True
		if self.byPassNoDescriptionOptionBox.IsChecked() != toggleByPassNoDescriptionAdvancedOption(False):
			toggleByPassNoDescriptionAdvancedOption()
			self.restartNVDA = True

	def onSave(self):
		self.saveSettingChanges()


class KeyboardSettingsPanel(SettingsPanel):
	# Translators: This is the label for the Keyboard settings panel.
	title = _("Keyboard")

	def __init__(self, parent):
		self.title = makeAddonWindowTitle(self.title)
		super(KeyboardSettingsPanel, self).__init__(parent)

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is the label for a group of editing options in the Keyboard settings panel.
		groupText = _("Keys's remanence")
		groupSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		sHelper.addItem(group)
		# Translators: This is the label for a checkbox in the Keyboard settings panel.
		labelText = _("&Only NVDA key in remanence")
		self.onlyNVDAKeyInRemanenceAdvancedOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.onlyNVDAKeyInRemanenceAdvancedOptionBox.SetValue(toggleOnlyNVDAKeyInRemanenceAdvancedOption(False))
		# Translators: This is the label for a checkbox in the Keyboard settings panel.
		labelText = _("Activate &remanence at NVDA's start")
		self.remanenceAtNVDAStartAdvancedOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.remanenceAtNVDAStartAdvancedOptionBox.SetValue(toggleRemanenceAtNVDAStartAdvancedOption(False))
		# Translators: This is the label for a combobox in the Keyboard settings panel.
		labelText = _("&Remanence's delay (in milliseconds):")
		remanenceDelayChoice = [x for x in range(1000, 10500, 500)]
		self.remanenceDelayChoice = list(reversed(remanenceDelayChoice))
		self.remanenceDelayBox = group.addLabeledControl(labelText, wx.Choice, choices=[str(x) for x in self.remanenceDelayChoice])
		self.remanenceDelayBox.SetSelection(self.remanenceDelayChoice.index(_addonConfigManager.getRemanenceDelay()))
		# Translators: This is the label for a check box in the Keyboard settings panel.
		labelText = _("Play &sound at the start of remanence")
		self.beepAtRemanenceStartOptionCheckBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.beepAtRemanenceStartOptionCheckBox .SetValue(toggleBeepAtRemanenceStartAdvancedOption(False))
		# Translators: This is the label for a check box in the Keyboard settings panel.
		labelText = _("Play sound at the &end of remanence")
		self.beepAtRemanenceEndOptionCheckBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.beepAtRemanenceEndOptionCheckBox .SetValue(toggleBeepAtRemanenceEndAdvancedOption(False))
		# Translators: This is the label for a check box in the Keyboard settings panel.
		labelText = _("Special remanence for &Gmail.com")
		self.remanenceForGmailOptionCheckBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.remanenceForGmailOptionCheckBox .SetValue(toggleRemanenceForGmailAdvancedOption(False))
		if not getInstallFeatureOption(ID_KeyRemanence):
			for item in range(0, group.sizer.GetItemCount()):
				group.sizer.Hide(item)
		# Translators: This is the label for a group of editing options in the Keyboard settings panel.
		groupText = _("Numeric keypad")
		groupSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=groupText)
		groupBox = groupSizer.GetStaticBox()
		group = gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer)
		sHelper.addItem(group)
		# Translators: This is the label for a checkbox in the keyboard settings panel.
		labelText = _("&Allow the standard use of the numeric keypad")
		self.enableNumpadNavigationModeToggleOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.enableNumpadNavigationModeToggleOptionBox.SetValue(toggleEnableNumpadNavigationModeToggleAdvancedOption(False))
		# Translators: This is the label for a checkbox in the keyboard settings panel.
		labelText = _("&Enable the standard use of the numeric keypad at NVDA's start")
		self.activateNumpadNavigationModeAtStartOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.activateNumpadNavigationModeAtStartOptionBox.SetValue(toggleActivateNumpadNavigationModeAtStartAdvancedOption(False))
		# Translators: This is the label for a checkbox in the keyboard settings panel.
		labelText = _("&Enable / disable numeric keypad's standard use with num lock key")
		self.activateNumpadStandardUseWithNumLockOptionBox = group.addItem(wx.CheckBox(groupBox, label=labelText))
		self.activateNumpadStandardUseWithNumLockOptionBox.SetValue(toggleActivateNumpadStandardUseWithNumLockAdvancedOption(False))

	def saveSettingChanges(self):
		self.restartNVDA = False
		if getInstallFeatureOption(ID_KeyRemanence):
			if self.onlyNVDAKeyInRemanenceAdvancedOptionBox.IsChecked() != toggleOnlyNVDAKeyInRemanenceAdvancedOption(False):
				toggleOnlyNVDAKeyInRemanenceAdvancedOption()
			if self.remanenceAtNVDAStartAdvancedOptionBox.IsChecked() != toggleRemanenceAtNVDAStartAdvancedOption(False):
				toggleRemanenceAtNVDAStartAdvancedOption()
			remanenceDelay = self.remanenceDelayBox.GetSelection()
			_addonConfigManager.setRemanenceDelay(self.remanenceDelayChoice[remanenceDelay])
			if self.beepAtRemanenceStartOptionCheckBox.IsChecked() != toggleBeepAtRemanenceStartAdvancedOption(False):
				toggleBeepAtRemanenceStartAdvancedOption()
			if self.beepAtRemanenceEndOptionCheckBox.IsChecked() != toggleBeepAtRemanenceEndAdvancedOption(False):
				toggleBeepAtRemanenceEndAdvancedOption()
			if self.remanenceForGmailOptionCheckBox.IsChecked() != toggleRemanenceForGmailAdvancedOption(False):
				toggleRemanenceForGmailAdvancedOption()
		if self.enableNumpadNavigationModeToggleOptionBox.IsChecked() != toggleEnableNumpadNavigationModeToggleAdvancedOption(False):
			toggleEnableNumpadNavigationModeToggleAdvancedOption()
			# in all cases, disable numpad navigation mode
			from ..commandKeysSelectiveAnnouncementAndRemanence import _myInputManager
			if _myInputManager is not None:
				_myInputManager .setNumpadNavigationMode(False)
		if self.activateNumpadNavigationModeAtStartOptionBox.IsChecked() != toggleActivateNumpadNavigationModeAtStartAdvancedOption(False):
			toggleActivateNumpadNavigationModeAtStartAdvancedOption()
		if self.activateNumpadStandardUseWithNumLockOptionBox.IsChecked() != toggleActivateNumpadStandardUseWithNumLockAdvancedOption(False):
			toggleActivateNumpadStandardUseWithNumLockAdvancedOption()

	def onSave(self):
		self.saveSettingChanges()


class UpdateSettingsPanel(SettingsPanel):
	# Translators: This is the label for the Advanced settings panel.
	title = _("Update")

	def __init__(self, parent):
		self.title = makeAddonWindowTitle(self.title)
		super(UpdateSettingsPanel, self).__init__(parent)

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is the label for a checkbox in the Update settings panel.
		labelText = _("Automatically check for &updates")
		self.autoCheckForUpdatesCheckBox = sHelper.addItem(wx.CheckBox(self, wx.ID_ANY, label=labelText))
		self.autoCheckForUpdatesCheckBox.SetValue(toggleAutoUpdateGeneralOptions(False))
		# Translators: This is the label for a checkbox in the Update settings panel.
		labelText = _("Update also release versions to &development versions")
		self.updateReleaseVersionsToDevVersionsCheckBox = sHelper.addItem(wx.CheckBox(self, wx.ID_ANY, label=labelText))
		self.updateReleaseVersionsToDevVersionsCheckBox.SetValue(toggleUpdateReleaseVersionsToDevVersionsGeneralOptions(False))
		# translators: this is a label for a button in update settings panel.
		labelText = _("&Check for update")
		checkForUpdateButton = wx.Button(self, label=labelText)
		sHelper.addItem(checkForUpdateButton)
		checkForUpdateButton.Bind(wx.EVT_BUTTON, self.onCheckForUpdate)
		# translators: this is a label for a button in update settings panel.
		labelText = _("View &history")
		seeHistoryButton = wx.Button(self, label=labelText)
		sHelper.addItem(seeHistoryButton)
		seeHistoryButton.Bind(wx.EVT_BUTTON, self.onSeeHistory)

	def onCheckForUpdate(self, evt):
		from ..updateHandler import addonUpdateCheck
		self.saveSettingChanges()
		releaseToDevVersion = self.updateReleaseVersionsToDevVersionsCheckBox.IsChecked()
		wx.CallAfter(addonUpdateCheck, auto=False, releaseToDev=releaseToDevVersion)
		self.Close()

	def onSeeHistory(self, evt):
		addon = addonHandler.getCodeAddon()
		from languageHandler import curLang
		theFile = os.path.join(addon.path, "doc", curLang, "changes.html")
		if not os.path.exists(theFile):
			lang = curLang
			theFile = os.path.join(addon.path, "doc", lang, "changes.html")
			if not os.path.exists(theFile):
				lang = "en"
				theFile = os.path.join(addon.path, "doc", lang, "changes.html")
		os.startfile(theFile)

	def saveSettingChanges(self):
		self.restartNVDA = False
		if self.autoCheckForUpdatesCheckBox.IsChecked() != toggleAutoUpdateGeneralOptions(False):
			toggleAutoUpdateGeneralOptions()
		if self.updateReleaseVersionsToDevVersionsCheckBox.IsChecked() != toggleUpdateReleaseVersionsToDevVersionsGeneralOptions(False):
			toggleUpdateReleaseVersionsToDevVersionsGeneralOptions()

	def onSave(self):
		self.saveSettingChanges()


class MultiCategorySettingsDialogEx(MultiCategorySettingsDialog):
	def _doSave(self):
		askForRestart = False
		super(MultiCategorySettingsDialogEx, self)._doSave()
		for panel in self.catIdToInstanceMap.values():
			askForRestart = askForRestart or panel.restartNVDA
		if askForRestart:
			askForNVDARestart()


class AddonSettingsDialog(MultiCategorySettingsDialogEx):
	INITIAL_SIZE = (1000, 480)
	# Min height required to show the OK, Cancel, Apply buttons
	MIN_SIZE = (470, 240)
	baseCategoryClasses = [
		FeaturesInstallationSettingsPanel,
		NVDAEnhancementSettingsPanel,
		ComputerSettingsPanel,
		KeyboardSettingsPanel,
		AdvancedSettingsPanel,
		UpdateSettingsPanel,
		]

	def __init__(self, parent, initialCategory=None):
		curAddon = addonHandler.getCodeAddon()
		# Translators: title of add-on settings dialog.
		dialogTitle = _("Settings")
		self.title = "%s - %s" % (curAddon.manifest["summary"], dialogTitle)
		self.categoryClasses = self.baseCategoryClasses[:]
		# if in secur mode, some panels must be disabled
		if globalVars.appArgs.secure:
			self.categoryClasses.remove(FeaturesInstallationSettingsPanel)
			self.categoryClasses .remove(UpdateSettingsPanel)
		super(AddonSettingsDialog, self).__init__(parent, initialCategory)
