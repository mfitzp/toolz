# -------------------------------------------------------------------------
#     Copyright (C) 2008-2010 Martin Strohalm <mmass@biographics.cz>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file LICENSE in the
#     main directory of the program
# -------------------------------------------------------------------------

# load libs
import threading
import wx
import numpy

# load modules
#from ids import *
import configGUI as config
import mwx
import images
import mspy

#from gui.panel_match import panelMatch


# FLOATING PANEL WITH SEQUENCE TOOLS
# ----------------------------------

class panelSequence(wx.MiniFrame):
    """Sequence tools."""

    def __init__(self, parent, tool='sequence'):
        wx.MiniFrame.__init__(self, parent, -1, 'Sequence', size=(500, 300), style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BOX | wx.MAXIMIZE_BOX))

        self.parent = parent
        self.processing = None
        self.matchPanel = None

        self.currentTool = tool
        self.currentSequence = mspy.sequence('')
        self.currentDigest = None
        self.currentFragments = None
        self.currentSearch = None

        # make gui items
        self.makeGUI()
        wx.EVT_CLOSE(self, self.onClose)

        # select default tool
        self.onToolSelected(tool=self.currentTool)
    # ----


    def makeGUI(self):
        """Make gui notebook."""

        # make toolbar
        toolbar = self.makeToolbar()

        # make panels
        sequence = self.makeSequencePanel()
        modify = self.makeModificationsPanel()
        digest = self.makeDigestPanel()
        fragment = self.makeFragmentPanel()
        search = self.makeSearchPanel()
        gauge = self.makeGaugePanel()

        # pack elements
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(toolbar, 0, wx.EXPAND, 0)
        self.mainSizer.Add(sequence, 1, wx.EXPAND, 0)
        self.mainSizer.Add(modify, 1, wx.EXPAND, 0)
        self.mainSizer.Add(digest, 1, wx.EXPAND, 0)
        self.mainSizer.Add(fragment, 1, wx.EXPAND, 0)
        self.mainSizer.Add(search, 1, wx.EXPAND, 0)
        self.mainSizer.Add(gauge, 0, wx.EXPAND, 0)

        self.mainSizer.Hide(1)
        self.mainSizer.Hide(2)
        self.mainSizer.Hide(3)
        self.mainSizer.Hide(4)
        self.mainSizer.Hide(5)
        self.mainSizer.Hide(6)

        self.mainSizer.Fit(self)
        self.SetSizer(self.mainSizer)
    # ----


    def makeToolbar(self):
        """Make toolbar."""

        # init toolbar
        panel = mwx.bgrPanel(self, -1, images.lib['bgrToolbar'], size=(-1, mwx.TOOLBAR_HEIGHT))

        # make buttons
        self.editor_butt = wx.BitmapButton(panel, ID_sequenceEditor, images.lib['sequenceEditorOff'], size=(mwx.TOOLBAR_TOOLSIZE), style=wx.BORDER_NONE)
        self.editor_butt.SetToolTip(wx.ToolTip("Sequence editor"))
        self.editor_butt.Bind(wx.EVT_BUTTON, self.onToolSelected)

        self.modifications_butt = wx.BitmapButton(panel, ID_sequenceModifications, images.lib['sequenceModificationsOff'], size=(mwx.TOOLBAR_TOOLSIZE), style=wx.BORDER_NONE)
        self.modifications_butt.SetToolTip(wx.ToolTip("Sequence modifications"))
        self.modifications_butt.Bind(wx.EVT_BUTTON, self.onToolSelected)

        self.digest_butt = wx.BitmapButton(panel, ID_sequenceDigest, images.lib['sequenceDigestOff'], size=(mwx.TOOLBAR_TOOLSIZE), style=wx.BORDER_NONE)
        self.digest_butt.SetToolTip(wx.ToolTip("Protein digest"))
        self.digest_butt.Bind(wx.EVT_BUTTON, self.onToolSelected)

        self.fragment_butt = wx.BitmapButton(panel, ID_sequenceFragment, images.lib['sequenceFragmentOff'], size=(mwx.TOOLBAR_TOOLSIZE), style=wx.BORDER_NONE)
        self.fragment_butt.SetToolTip(wx.ToolTip("Peptide fragmentation"))
        self.fragment_butt.Bind(wx.EVT_BUTTON, self.onToolSelected)

        self.search_butt = wx.BitmapButton(panel, ID_sequenceSearch, images.lib['sequenceSearchOff'], size=(mwx.TOOLBAR_TOOLSIZE), style=wx.BORDER_NONE)
        self.search_butt.SetToolTip(wx.ToolTip("Sequence search"))
        self.search_butt.Bind(wx.EVT_BUTTON, self.onToolSelected)

        # pack elements
        tools = wx.BoxSizer(wx.HORIZONTAL)
        tools.AddSpacer(mwx.TOOLBAR_LSPACE)
        tools.Add(self.editor_butt, 0, wx.ALIGN_CENTER_VERTICAL)
        tools.Add(self.modifications_butt, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, mwx.BUTTON_SIZE_CORRECTION)
        tools.Add(self.digest_butt, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, mwx.BUTTON_SIZE_CORRECTION)
        tools.Add(self.fragment_butt, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, mwx.BUTTON_SIZE_CORRECTION)
        tools.Add(self.search_butt, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, mwx.BUTTON_SIZE_CORRECTION)

        self.toolbar = wx.BoxSizer(wx.HORIZONTAL)
        self.toolbar.Add(tools, 0, wx.ALIGN_CENTER_VERTICAL)
        self.toolbar.Add(self.makeSequenceToolbar(panel), 0, wx.ALIGN_CENTER_VERTICAL)
        self.toolbar.Add(self.makeModificationsToolbar(panel), 1, wx.ALIGN_CENTER_VERTICAL)
        self.toolbar.Add(self.makeDigestToolbar(panel), 1, wx.ALIGN_CENTER_VERTICAL)
        self.toolbar.Add(self.makeFragmentToolbar(panel), 1, wx.ALIGN_CENTER_VERTICAL)
        self.toolbar.Add(self.makeSearchToolbar(panel), 1, wx.ALIGN_CENTER_VERTICAL)

        self.toolbar.Hide(1)
        self.toolbar.Hide(2)
        self.toolbar.Hide(3)
        self.toolbar.Hide(4)
        self.toolbar.Hide(5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.toolbar, 1, wx.EXPAND)

        panel.SetSizer(mainSizer)
        mainSizer.Fit(panel)

        return panel
    # ----


    def makeSequenceToolbar(self, panel):
        """Make toolbar for sequence panel."""

        # make elements
        self.sequenceInfo_label = wx.StaticText(panel, -1, "", size=(330,-1))
        self.sequenceInfo_label.SetFont(wx.SMALL_FONT)

        self.pattern_butt = wx.Button(panel, -1, "Pattern", size=(-1, mwx.SMALL_BUTTON_HEIGHT))
        self.pattern_butt.SetFont(wx.SMALL_FONT)
        self.pattern_butt.Bind(wx.EVT_BUTTON, self.onSequencePattern)

        # pack elements
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(20)
        sizer.Add(self.sequenceInfo_label, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddStretchSpacer()
        sizer.AddSpacer(20)
        sizer.Add(self.pattern_butt, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(mwx.TOOLBAR_RSPACE)

        return sizer
    # ----


    def makeModificationsToolbar(self, panel):
        """Make toolbar for modifications panel."""

        # make elements
        self.modsSpecifity_check = wx.CheckBox(panel, -1, "Show specific modifications only")
        self.modsSpecifity_check.SetFont(wx.SMALL_FONT)
        self.modsSpecifity_check.SetValue(True)
        self.modsSpecifity_check.Bind(wx.EVT_CHECKBOX, self.onSpecifityFilter)

        self.modsAdd_butt = wx.Button(panel, -1, "Add", size=(-1, mwx.SMALL_BUTTON_HEIGHT))
        self.modsAdd_butt.SetFont(wx.SMALL_FONT)
        self.modsAdd_butt.Bind(wx.EVT_BUTTON, self.onAddModification)

        self.modsRemove_butt = wx.Button(panel, -1, "Remove", size=(-1, mwx.SMALL_BUTTON_HEIGHT))
        self.modsRemove_butt.SetFont(wx.SMALL_FONT)
        self.modsRemove_butt.Bind(wx.EVT_BUTTON, self.onRemoveModifications)

        # pack elements
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(20)
        sizer.Add(self.modsSpecifity_check, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddStretchSpacer()
        sizer.AddSpacer(20)
        sizer.Add(self.modsAdd_butt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        sizer.Add(self.modsRemove_butt, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(mwx.TOOLBAR_RSPACE)

        return sizer
    # ----


    def makeDigestToolbar(self, panel):
        """Make toolbar for digest panel."""

        # make elements
        digestMassType_label = wx.StaticText(panel, -1, "Mass:")
        digestMassType_label.SetFont(wx.SMALL_FONT)

        self.digestMassTypeMo_radio = wx.RadioButton(panel, -1, "Mo", style=wx.RB_GROUP)
        self.digestMassTypeMo_radio.SetFont(wx.SMALL_FONT)
        self.digestMassTypeMo_radio.SetValue(True)

        self.digestMassTypeAv_radio = wx.RadioButton(panel, -1, "Av")
        self.digestMassTypeAv_radio.SetFont(wx.SMALL_FONT)
        self.digestMassTypeAv_radio.SetValue(config.sequence['digest']['massType'])

        digestMaxCharge_label = wx.StaticText(panel, -1, "Max charge:")
        digestMaxCharge_label.SetFont(wx.SMALL_FONT)

        self.digestMaxCharge_value = wx.TextCtrl(panel, -1, str(config.sequence['digest']['maxCharge']), size=(40, mwx.SMALL_TEXTCTRL_HEIGHT), validator=mwx.validator('int'))
        self.digestMaxCharge_value.SetFont(wx.SMALL_FONT)

        self.digestGenerate_butt = wx.Button(panel, -1, "Digest", size=(-1, mwx.SMALL_BUTTON_HEIGHT))
        self.digestGenerate_butt.SetFont(wx.SMALL_FONT)
        self.digestGenerate_butt.Bind(wx.EVT_BUTTON, self.onDigest)

        self.digestMatch_butt = wx.Button(panel, -1, "Match", size=(-1, mwx.SMALL_BUTTON_HEIGHT))
        self.digestMatch_butt.SetFont(wx.SMALL_FONT)
        self.digestMatch_butt.Bind(wx.EVT_BUTTON, self.onMatch)

        self.digestStore_butt = wx.Button(panel, -1, "Store", size=(-1, mwx.SMALL_BUTTON_HEIGHT))
        self.digestStore_butt.SetFont(wx.SMALL_FONT)
        self.digestStore_butt.Bind(wx.EVT_BUTTON, self.onStore)

        # pack elements
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(20)
        sizer.Add(digestMassType_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.digestMassTypeMo_radio, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.digestMassTypeAv_radio, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(digestMaxCharge_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.digestMaxCharge_value, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddStretchSpacer()
        sizer.AddSpacer(20)
        sizer.Add(self.digestGenerate_butt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        sizer.Add(self.digestMatch_butt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        sizer.Add(self.digestStore_butt, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(mwx.TOOLBAR_RSPACE)

        return sizer
    # ----


    def makeFragmentToolbar(self, panel):
        """Make toolbar for fragment panel."""

        # make elements
        fragmentMassType_label = wx.StaticText(panel, -1, "Mass:")
        fragmentMassType_label.SetFont(wx.SMALL_FONT)

        self.fragmentMassTypeMo_radio = wx.RadioButton(panel, -1, "Mo", style=wx.RB_GROUP)
        self.fragmentMassTypeMo_radio.SetFont(wx.SMALL_FONT)
        self.fragmentMassTypeMo_radio.SetValue(True)

        self.fragmentMassTypeAv_radio = wx.RadioButton(panel, -1, "Av")
        self.fragmentMassTypeAv_radio.SetFont(wx.SMALL_FONT)
        self.fragmentMassTypeAv_radio.SetValue(config.sequence['fragment']['massType'])

        fragmentMaxCharge_label = wx.StaticText(panel, -1, "Max charge:")
        fragmentMaxCharge_label.SetFont(wx.SMALL_FONT)

        self.fragmentMaxCharge_value = wx.TextCtrl(panel, -1, str(config.sequence['fragment']['maxCharge']), size=(40, mwx.SMALL_TEXTCTRL_HEIGHT), validator=mwx.validator('int'))
        self.fragmentMaxCharge_value.SetFont(wx.SMALL_FONT)

        self.fragmentGenerate_butt = wx.Button(panel, -1, "Fragment", size=(-1, mwx.SMALL_BUTTON_HEIGHT))
        self.fragmentGenerate_butt.SetFont(wx.SMALL_FONT)
        self.fragmentGenerate_butt.Bind(wx.EVT_BUTTON, self.onFragment)

        self.fragmentMatch_butt = wx.Button(panel, -1, "Match", size=(-1, mwx.SMALL_BUTTON_HEIGHT))
        self.fragmentMatch_butt.SetFont(wx.SMALL_FONT)
        self.fragmentMatch_butt.Bind(wx.EVT_BUTTON, self.onMatch)

        self.fragmentStore_butt = wx.Button(panel, -1, "Store", size=(-1, mwx.SMALL_BUTTON_HEIGHT))
        self.fragmentStore_butt.SetFont(wx.SMALL_FONT)
        self.fragmentStore_butt.Bind(wx.EVT_BUTTON, self.onStore)

        # pack elements
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(20)
        sizer.Add(fragmentMassType_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentMassTypeMo_radio, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentMassTypeAv_radio, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(fragmentMaxCharge_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentMaxCharge_value, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddStretchSpacer()
        sizer.AddSpacer(20)
        sizer.Add(self.fragmentGenerate_butt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        sizer.Add(self.fragmentMatch_butt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        sizer.Add(self.fragmentStore_butt, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(mwx.TOOLBAR_RSPACE)

        return sizer
    # ----


    def makeSearchToolbar(self, panel):
        """Make toolbar for search panel."""

        # make elements
        searchMassType_label = wx.StaticText(panel, -1, "Mass:")
        searchMassType_label.SetFont(wx.SMALL_FONT)

        self.searchMass_value = wx.TextCtrl(panel, -1, "", size=(100, -1), style=wx.TE_PROCESS_ENTER, validator=mwx.validator('floatPos'))
        self.searchMass_value.Bind(wx.EVT_TEXT_ENTER, self.onSearch)

        self.searchMassTypeMo_radio = wx.RadioButton(panel, -1, "Mo", style=wx.RB_GROUP)
        self.searchMassTypeMo_radio.SetFont(wx.SMALL_FONT)
        self.searchMassTypeMo_radio.SetValue(True)

        self.searchMassTypeAv_radio = wx.RadioButton(panel, -1, "Av")
        self.searchMassTypeAv_radio.SetFont(wx.SMALL_FONT)
        self.searchMassTypeAv_radio.SetValue(config.sequence['search']['massType'])

        searchMaxCharge_label = wx.StaticText(panel, -1, "Max charge:")
        searchMaxCharge_label.SetFont(wx.SMALL_FONT)

        self.searchMaxCharge_value = wx.TextCtrl(panel, -1, str(config.sequence['search']['maxCharge']), size=(40, mwx.SMALL_TEXTCTRL_HEIGHT), validator=mwx.validator('int'))
        self.searchMaxCharge_value.SetFont(wx.SMALL_FONT)

        self.searchGenerate_butt = wx.Button(panel, -1, "Search", size=(-1, mwx.SMALL_BUTTON_HEIGHT))
        self.searchGenerate_butt.SetFont(wx.SMALL_FONT)
        self.searchGenerate_butt.Bind(wx.EVT_BUTTON, self.onSearch)

        # pack elements
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(20)
        sizer.Add(searchMassType_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.searchMass_value, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.searchMassTypeMo_radio, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.searchMassTypeAv_radio, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(searchMaxCharge_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.searchMaxCharge_value, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddStretchSpacer()
        sizer.AddSpacer(20)
        sizer.Add(self.searchGenerate_butt, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(mwx.TOOLBAR_RSPACE)

        return sizer
    # ----


    def makeSequencePanel(self):
        """Make compound summary panel."""

        panel = wx.Panel(self, -1)

        # make elements
        self.sequenceTitle_value = wx.TextCtrl(panel, -1, self.currentSequence.title, size=(300, -1))
        self.sequenceTitle_value.Bind(wx.EVT_TEXT, self.onSequenceTitle)

        self.sequenceCanvas = sequenceCanvas(panel, -1, sequence=self.currentSequence,  size=(300, 200))
        self.sequenceCanvas.Bind(wx.EVT_KEY_DOWN, self.onSequence)
        self.sequenceCanvas.Bind(wx.EVT_LEFT_DOWN, self.onSequence)
        self.sequenceCanvas.Bind(wx.EVT_RIGHT_DOWN, self.onSequence)
        self.sequenceCanvas.Bind(wx.EVT_MOTION, self.onSequence)

        # pack elements
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.sequenceTitle_value, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, mwx.PANEL_SPACE_MAIN)
        mainSizer.Add(self.sequenceCanvas, 1, wx.EXPAND|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, mwx.PANEL_SPACE_MAIN)

        # fit layout
        mainSizer.Fit(panel)
        panel.SetSizer(mainSizer)

        return panel
    # ----


    def makeModificationsPanel(self):
        """Make controls for sequence modifications."""

        # init panel
        ctrlPanel = mwx.bgrPanel(self, -1, images.lib['bgrControlbar'], size=(-1, mwx.CONTROLBAR_HEIGHT))

        # make controls
        modsPosition_label = wx.StaticText(ctrlPanel, -1, "Position:")
        modsPosition_label.SetFont(wx.SMALL_FONT)

        self.modsResidue_combo = wx.ComboBox(ctrlPanel, -1, choices=['Glutamic acid'], size=(130,22), style=wx.CB_READONLY)
        self.modsResidue_combo.SetFont(wx.SMALL_FONT)
        self.modsResidue_combo.Bind(wx.EVT_COMBOBOX, self.onResidueSelected)

        self.modsPosition_combo = wx.ComboBox(ctrlPanel, -1, choices=[], size=(80,22), style=wx.CB_READONLY)
        self.modsPosition_combo.SetFont(wx.SMALL_FONT)
        self.modsPosition_combo.Bind(wx.EVT_COMBOBOX, self.onPositionSelected)

        modsMod_label = wx.StaticText(ctrlPanel, -1, "Modification:")
        modsMod_label.SetFont(wx.SMALL_FONT)

        self.modsMod_combo = wx.ComboBox(ctrlPanel, -1, choices=[], size=(150,22), style=wx.CB_READONLY)
        self.modsMod_combo.SetFont(wx.SMALL_FONT)

        self.modsType_combo = wx.ComboBox(ctrlPanel, -1, choices=['Fixed', 'Variable'], size=(90,22), style=wx.CB_READONLY)
        self.modsType_combo.SetFont(wx.SMALL_FONT)
        self.modsType_combo.Select(0)

        self.makeModificationsList()

        # pack controls
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.AddSpacer(mwx.CONTROLBAR_LSPACE)
        sizer.Add(modsPosition_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.modsResidue_combo, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(10)
        sizer.Add(self.modsPosition_combo, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(modsMod_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.modsMod_combo, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(10)
        sizer.Add(self.modsType_combo, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(mwx.CONTROLBAR_RSPACE)

        controls = wx.BoxSizer(wx.VERTICAL)
        controls.Add(sizer, 1, wx.EXPAND)

        controls.Fit(ctrlPanel)
        ctrlPanel.SetSizer(controls)

        # pack main
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(ctrlPanel, 0, wx.EXPAND)
        mainSizer.Add(self.modificationsList, 1, wx.EXPAND|wx.ALL, mwx.LISTCTRL_NO_SPACE)

        return mainSizer
    # ----


    def makeDigestPanel(self):
        """Make controls for protein digest."""

        # init panel
        ctrlPanel = mwx.bgrPanel(self, -1, images.lib['bgrControlbar'], size=(-1, mwx.CONTROLBAR_HEIGHT))

        # make controls
        digestEnzyme_label = wx.StaticText(ctrlPanel, -1, "Enzyme:")
        digestEnzyme_label.SetFont(wx.SMALL_FONT)

        enzymes = mspy.enzymes.keys()
        enzymes.sort()
        self.digestEnzyme_combo = wx.ComboBox(ctrlPanel, -1, choices=enzymes, size=(150,22), style=wx.CB_READONLY)
        self.digestEnzyme_combo.SetFont(wx.SMALL_FONT)
        if config.sequence['digest']['enzyme'] in enzymes:
            self.digestEnzyme_combo.Select(enzymes.index(config.sequence['digest']['enzyme']))
        else:
            self.digestEnzyme_combo.Select(0)

        digestMiscl_label = wx.StaticText(ctrlPanel, -1, "Miscl.:")
        self.digestMiscl_value = wx.TextCtrl(ctrlPanel, -1, str(config.sequence['digest']['miscl']), size=(40, mwx.SMALL_TEXTCTRL_HEIGHT), validator=mwx.validator('intPos'))
        digestMiscl_label.SetFont(wx.SMALL_FONT)
        self.digestMiscl_value.SetFont(wx.SMALL_FONT)

        digestLimits_label = wx.StaticText(ctrlPanel, -1, "Mass limit:")
        digestLimits_label.SetFont(wx.SMALL_FONT)

        self.digestLowMass_value = wx.TextCtrl(ctrlPanel, -1, str(config.sequence['digest']['lowMass']), size=(60, mwx.SMALL_TEXTCTRL_HEIGHT), validator=mwx.validator('intPos'))
        self.digestLowMass_value.SetFont(wx.SMALL_FONT)

        digestLimitsTo_label = wx.StaticText(ctrlPanel, -1, "-")
        digestLimitsTo_label.SetFont(wx.SMALL_FONT)

        self.digestHighMass_value = wx.TextCtrl(ctrlPanel, -1, str(config.sequence['digest']['highMass']), size=(60, mwx.SMALL_TEXTCTRL_HEIGHT), validator=mwx.validator('intPos'))
        self.digestHighMass_value.SetFont(wx.SMALL_FONT)

        self.digestAllowMods_check = wx.CheckBox(ctrlPanel, -1, "Ignore modifications")
        self.digestAllowMods_check.SetFont(wx.SMALL_FONT)
        self.digestAllowMods_check.SetValue(config.sequence['digest']['allowMods'])

        self.makeDigestList()

        # pack controls
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(mwx.CONTROLBAR_LSPACE)
        sizer.Add(digestEnzyme_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.digestEnzyme_combo, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(digestMiscl_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.digestMiscl_value, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(digestLimits_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.digestLowMass_value, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(digestLimitsTo_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.digestHighMass_value, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(self.digestAllowMods_check, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(mwx.CONTROLBAR_RSPACE)

        controls = wx.BoxSizer(wx.VERTICAL)
        controls.Add(sizer, 1, wx.EXPAND)

        controls.Fit(ctrlPanel)
        ctrlPanel.SetSizer(controls)

        # pack main
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(ctrlPanel, 0, wx.EXPAND)
        mainSizer.Add(self.digestList, 1, wx.EXPAND|wx.ALL, mwx.LISTCTRL_NO_SPACE)

        return mainSizer
    # ----


    def makeFragmentPanel(self):
        """Make controls for peptide fragmentation."""

        # init panel
        ctrlPanel = mwx.bgrPanel(self, -1, images.lib['bgrControlbar'], size=(-1, mwx.CONTROLBAR_HEIGHT))

        # make controls
        fragmentIons_label = wx.StaticText(ctrlPanel, -1, "Ions:")
        fragmentIons_label.SetFont(wx.SMALL_FONT)

        self.fragmentA_check = wx.CheckBox(ctrlPanel, -1, "a")
        self.fragmentA_check.SetFont(wx.SMALL_FONT)
        self.fragmentA_check.SetValue(config.sequence['fragment']['fragments'].count('a'))

        self.fragmentB_check = wx.CheckBox(ctrlPanel, -1, "b")
        self.fragmentB_check.SetFont(wx.SMALL_FONT)
        self.fragmentB_check.SetValue(config.sequence['fragment']['fragments'].count('b'))

        self.fragmentC_check = wx.CheckBox(ctrlPanel, -1, "c")
        self.fragmentC_check.SetFont(wx.SMALL_FONT)
        self.fragmentC_check.SetValue(config.sequence['fragment']['fragments'].count('c'))

        self.fragmentX_check = wx.CheckBox(ctrlPanel, -1, "x")
        self.fragmentX_check.SetFont(wx.SMALL_FONT)
        self.fragmentX_check.SetValue(config.sequence['fragment']['fragments'].count('x'))

        self.fragmentY_check = wx.CheckBox(ctrlPanel, -1, "y")
        self.fragmentY_check.SetFont(wx.SMALL_FONT)
        self.fragmentY_check.SetValue(config.sequence['fragment']['fragments'].count('y'))

        self.fragmentZ_check = wx.CheckBox(ctrlPanel, -1, "z")
        self.fragmentZ_check.SetFont(wx.SMALL_FONT)
        self.fragmentZ_check.SetValue(config.sequence['fragment']['fragments'].count('z'))

        fragmentLoss_label = wx.StaticText(ctrlPanel, -1, 'Loss:')
        fragmentLoss_label.SetFont(wx.SMALL_FONT)

        self.fragmentNH3_check = wx.CheckBox(ctrlPanel, -1, "-NH3")
        self.fragmentNH3_check.SetFont(wx.SMALL_FONT)
        self.fragmentNH3_check.SetValue(config.sequence['fragment']['fragments'].count('-NH3'))

        self.fragmentH2O_check = wx.CheckBox(ctrlPanel, -1, "-H2O")
        self.fragmentH2O_check.SetFont(wx.SMALL_FONT)
        self.fragmentH2O_check.SetValue(config.sequence['fragment']['fragments'].count('-H2O'))

        self.fragmentInt_check = wx.CheckBox(ctrlPanel, -1, "Internal")
        self.fragmentInt_check.SetFont(wx.SMALL_FONT)
        self.fragmentInt_check.SetValue(config.sequence['fragment']['fragments'].count('int'))

        self.fragmentNLadder_check = wx.CheckBox(ctrlPanel, -1, "N-ladder")
        self.fragmentNLadder_check.SetFont(wx.SMALL_FONT)
        self.fragmentNLadder_check.SetValue(config.sequence['fragment']['fragments'].count('n-ladder'))

        self.fragmentCLadder_check = wx.CheckBox(ctrlPanel, -1, "C-ladder")
        self.fragmentCLadder_check.SetFont(wx.SMALL_FONT)
        self.fragmentCLadder_check.SetValue(config.sequence['fragment']['fragments'].count('c-ladder'))

        self.fragmentFilter_check = wx.CheckBox(ctrlPanel, -1, "Filter")
        self.fragmentFilter_check.SetFont(wx.SMALL_FONT)
        self.fragmentFilter_check.SetValue(config.sequence['fragment']['filterFragments'])

        self.makeFragmentsList()

        # pack controls
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.AddSpacer(mwx.CONTROLBAR_LSPACE)
        sizer.Add(fragmentIons_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentA_check, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentB_check, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentC_check, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentX_check, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentY_check, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentZ_check, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(fragmentLoss_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentNH3_check, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentH2O_check, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(self.fragmentInt_check, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentNLadder_check, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.fragmentCLadder_check, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(self.fragmentFilter_check, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(mwx.CONTROLBAR_RSPACE)

        controls = wx.BoxSizer(wx.VERTICAL)
        controls.Add(sizer, 1, wx.EXPAND)

        controls.Fit(ctrlPanel)
        ctrlPanel.SetSizer(controls)

        # pack main
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(ctrlPanel, 0, wx.EXPAND)
        mainSizer.Add(self.fragmentsList, 1, wx.EXPAND|wx.ALL, mwx.LISTCTRL_NO_SPACE)

        return mainSizer
    # ----


    def makeSearchPanel(self):
        """Make controls for sequence search."""

        # init panel
        ctrlPanel = mwx.bgrPanel(self, -1, images.lib['bgrControlbar'], size=(-1, mwx.CONTROLBAR_HEIGHT))

        # make controls
        searchEnzyme_label = wx.StaticText(ctrlPanel, -1, "Endings by:")
        searchEnzyme_label.SetFont(wx.SMALL_FONT)

        enzymes = mspy.enzymes.keys()
        enzymes.sort()
        self.searchEnzyme_combo = wx.ComboBox(ctrlPanel, -1, choices=enzymes, size=(150,22), style=wx.CB_READONLY)
        self.searchEnzyme_combo.SetFont(wx.SMALL_FONT)
        if config.sequence['search']['enzyme'] in enzymes:
            self.searchEnzyme_combo.Select(enzymes.index(config.sequence['search']['enzyme']))
        else:
            self.searchEnzyme_combo.Select(0)

        searchTolerance_label = wx.StaticText(ctrlPanel, -1, "Tolerance:")
        searchTolerance_label.SetFont(wx.SMALL_FONT)

        self.searchTolerance_value = wx.TextCtrl(ctrlPanel, -1, str(config.sequence['search']['tolerance']), size=(40, mwx.SMALL_TEXTCTRL_HEIGHT), validator=mwx.validator('floatPos'))
        self.searchTolerance_value.SetFont(wx.SMALL_FONT)

        self.searchUnitsDa_radio = wx.RadioButton(ctrlPanel, -1, "Da", style=wx.RB_GROUP)
        self.searchUnitsDa_radio.SetFont(wx.SMALL_FONT)
        self.searchUnitsDa_radio.SetValue(True)

        self.searchUnitsPpm_radio = wx.RadioButton(ctrlPanel, -1, "ppm")
        self.searchUnitsPpm_radio.SetFont(wx.SMALL_FONT)

        if config.sequence['search']['units'] == 'ppm':
            self.searchUnitsPpm_radio.SetValue(True)

        self.makeSearchList()

        # pack controls
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(mwx.CONTROLBAR_LSPACE)
        sizer.Add(searchEnzyme_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.searchEnzyme_combo, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddSpacer(20)
        sizer.Add(searchTolerance_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.searchTolerance_value, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.searchUnitsDa_radio, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(self.searchUnitsPpm_radio, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer.AddSpacer(mwx.CONTROLBAR_RSPACE)

        controls = wx.BoxSizer(wx.VERTICAL)
        controls.Add(sizer, 1, wx.EXPAND)

        controls.Fit(ctrlPanel)
        ctrlPanel.SetSizer(controls)

        # pack main
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(ctrlPanel, 0, wx.EXPAND)
        mainSizer.Add(self.searchList, 1, wx.EXPAND|wx.ALL, mwx.LISTCTRL_NO_SPACE)

        return mainSizer
    # ----


    def makeGaugePanel(self):
        """Make processing gauge."""

        panel = wx.Panel(self, -1)

        # make elements
        self.gauge = mwx.gauge(panel, -1)

        # pack elements
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.gauge, 0, wx.EXPAND|wx.ALL, mwx.GAUGE_SPACE)

        # fit layout
        mainSizer.Fit(panel)
        panel.SetSizer(mainSizer)

        return panel
    # ----


    def makeModificationsList(self):
        """Make modifications list."""

        # init peaklist
        self.modificationsList = mwx.sortListCtrl(self, -1, size=(651, 200), style=mwx.LISTCTRL_STYLE_MULTI)
        self.modificationsList.SetFont(wx.SMALL_FONT)
        self.modificationsList.setSecondarySortColumn(1)
        self.modificationsList.setAltColour(mwx.LISTCTRL_ALTCOLOUR)

        # make columns
        self.modificationsList.InsertColumn(0, "position", wx.LIST_FORMAT_LEFT)
        self.modificationsList.InsertColumn(1, "modification", wx.LIST_FORMAT_LEFT)
        self.modificationsList.InsertColumn(2, "type", wx.LIST_FORMAT_CENTER)
        self.modificationsList.InsertColumn(3, "mo. mass", wx.LIST_FORMAT_RIGHT)
        self.modificationsList.InsertColumn(4, "av. mass", wx.LIST_FORMAT_RIGHT)
        self.modificationsList.InsertColumn(5, "formula", wx.LIST_FORMAT_LEFT)

        # set column widths
        for col, width in enumerate((70,143,70,90,90,168)):
            self.modificationsList.SetColumnWidth(col, width)
    # ----


    def makeDigestList(self):
        """Make digest list."""

        # init peaklist
        self.digestList = mwx.sortListCtrl(self, -1, size=(701, 300), style=mwx.LISTCTRL_STYLE_SINGLE)
        self.digestList.SetFont(wx.SMALL_FONT)
        self.digestList.setSecondarySortColumn(2)
        self.digestList.setAltColour(mwx.LISTCTRL_ALTCOLOUR)

        # set events
        self.digestList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.digestList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onItemActivated)
        self.digestList.Bind(wx.EVT_KEY_DOWN, self.onKey)

        # make columns
        self.digestList.InsertColumn(0, "range", wx.LIST_FORMAT_CENTER)
        self.digestList.InsertColumn(1, "mis.", wx.LIST_FORMAT_CENTER)
        self.digestList.InsertColumn(2, "m/z", wx.LIST_FORMAT_RIGHT)
        self.digestList.InsertColumn(3, "z", wx.LIST_FORMAT_CENTER)
        self.digestList.InsertColumn(4, "sequence", wx.LIST_FORMAT_LEFT)
        self.digestList.InsertColumn(5, "error", wx.LIST_FORMAT_RIGHT)

        # set column widths
        for col, width in enumerate((80,47,90,40,363,60)):
            self.digestList.SetColumnWidth(col, width)
    # ----


    def makeFragmentsList(self):
        """Make fragments list."""

        # init peaklist
        self.fragmentsList = mwx.sortListCtrl(self, -1, size=(706, 300), style=mwx.LISTCTRL_STYLE_SINGLE)
        self.fragmentsList.SetFont(wx.SMALL_FONT)
        self.fragmentsList.setSecondarySortColumn(1)
        self.fragmentsList.setAltColour(mwx.LISTCTRL_ALTCOLOUR)

        # set events
        self.fragmentsList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.fragmentsList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onItemActivated)
        self.fragmentsList.Bind(wx.EVT_KEY_DOWN, self.onKey)

        # make columns
        self.fragmentsList.InsertColumn(0, "ion", wx.LIST_FORMAT_LEFT)
        self.fragmentsList.InsertColumn(1, "#", wx.LIST_FORMAT_RIGHT)
        self.fragmentsList.InsertColumn(2, "range", wx.LIST_FORMAT_CENTER)
        self.fragmentsList.InsertColumn(3, "m/z", wx.LIST_FORMAT_RIGHT)
        self.fragmentsList.InsertColumn(4, "z", wx.LIST_FORMAT_CENTER)
        self.fragmentsList.InsertColumn(5, "sequence", wx.LIST_FORMAT_LEFT)
        self.fragmentsList.InsertColumn(6, "error", wx.LIST_FORMAT_RIGHT)

        # set column widths
        for col, width in enumerate((60,40,60,90,40,335,60)):
            self.fragmentsList.SetColumnWidth(col, width)
    # ----


    def makeSearchList(self):
        """Make search list."""

        # init peaklist
        self.searchList = mwx.sortListCtrl(self, -1, size=(646, 250), style=mwx.LISTCTRL_STYLE_SINGLE)
        self.searchList.SetFont(wx.SMALL_FONT)
        self.searchList.setSecondarySortColumn(1)
        self.searchList.setAltColour(mwx.LISTCTRL_ALTCOLOUR)

        # set events
        self.searchList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.searchList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onItemActivated)
        self.searchList.Bind(wx.EVT_KEY_DOWN, self.onKey)

        # make columns
        self.searchList.InsertColumn(0, "range", wx.LIST_FORMAT_CENTER)
        self.searchList.InsertColumn(1, "m/z", wx.LIST_FORMAT_RIGHT)
        self.searchList.InsertColumn(2, "z", wx.LIST_FORMAT_CENTER)
        self.searchList.InsertColumn(3, "sequence", wx.LIST_FORMAT_LEFT)
        self.searchList.InsertColumn(4, "error", wx.LIST_FORMAT_RIGHT)

        # set column widths
        for col, width in enumerate((80,90,40,355,60)):
            self.searchList.SetColumnWidth(col, width)
    # ----


    def onClose(self, evt):
        """Hide this frame."""

        # check processing
        if self.processing != None:
            wx.Bell()
            return

        # close match panel
        if self.matchPanel:
            self.matchPanel.Close()

        # close self
        self.Destroy()
    # ----


    def onProcessing(self, status=True):
        """Show processing gauge."""

        self.gauge.SetValue(0)

        if status:
            self.MakeModal(True)
            self.mainSizer.Show(6)
        else:
            self.MakeModal(False)
            self.mainSizer.Hide(6)
            self.processing = None

        # fit layout
        self.Layout()
        self.mainSizer.Fit(self)
        try: wx.Yield()
        except: pass
    # ----


    def onToolSelected(self, evt=None, tool=None):
        """Selected tool."""

        # check processing
        if self.processing != None:
            wx.Bell()
            return

        # get the tool
        if evt != None:
            tool = 'editor'
            if evt and evt.GetId() == ID_sequenceEditor:
                tool = 'editor'
            elif evt and evt.GetId() == ID_sequenceModifications:
                tool = 'modifications'
            elif evt and evt.GetId() == ID_sequenceDigest:
                tool = 'digest'
            elif evt and evt.GetId() == ID_sequenceFragment:
                tool = 'fragment'
            elif evt and evt.GetId() == ID_sequenceSearch:
                tool = 'search'

        # set current tool
        self.currentTool = tool

        # hide panels
        self.mainSizer.Hide(1)
        self.mainSizer.Hide(2)
        self.mainSizer.Hide(3)
        self.mainSizer.Hide(4)
        self.mainSizer.Hide(5)

        # hide toolbars
        self.toolbar.Hide(1)
        self.toolbar.Hide(2)
        self.toolbar.Hide(3)
        self.toolbar.Hide(4)
        self.toolbar.Hide(5)

        # set icons off
        self.editor_butt.SetBitmapLabel(images.lib['sequenceEditorOff'])
        self.modifications_butt.SetBitmapLabel(images.lib['sequenceModificationsOff'])
        self.digest_butt.SetBitmapLabel(images.lib['sequenceDigestOff'])
        self.fragment_butt.SetBitmapLabel(images.lib['sequenceFragmentOff'])
        self.search_butt.SetBitmapLabel(images.lib['sequenceSearchOff'])

        # set panel
        if tool == 'editor':
            self.SetTitle("Sequence Editor")
            self.editor_butt.SetBitmapLabel(images.lib['sequenceEditorOn'])
            self.toolbar.Show(1)
            self.mainSizer.Show(1)

        if tool == 'modifications':
            self.SetTitle("Sequence Modifications")
            self.modifications_butt.SetBitmapLabel(images.lib['sequenceModificationsOn'])
            self.toolbar.Show(2)
            self.mainSizer.Show(2)

        elif tool == 'digest':
            self.SetTitle("Protein Digest")
            self.digest_butt.SetBitmapLabel(images.lib['sequenceDigestOn'])
            self.toolbar.Show(3)
            self.mainSizer.Show(3)

        elif tool == 'fragment':
            self.SetTitle("Peptide Fragmentation")
            self.fragment_butt.SetBitmapLabel(images.lib['sequenceFragmentOn'])
            self.toolbar.Show(4)
            self.mainSizer.Show(4)

        elif tool == 'search':
            self.SetTitle("Sequence Search")
            self.search_butt.SetBitmapLabel(images.lib['sequenceSearchOn'])
            self.toolbar.Show(5)
            self.mainSizer.Show(5)

        # fit layout
        self.SetMinSize((-1,-1))
        self.mainSizer.Fit(self)
        self.Layout()
        size = self.GetSize()
        self.SetSize((size[0]+1,size[1]))
        self.SetSize(size)
        self.SetMinSize(size)
    # ----


    def onSequenceTitle(self, evt):
        """Update sequence title."""
        self.currentSequence.title = self.sequenceTitle_value.GetValue()
        self.parent.onDocumentChanged('seqtitle')
    # ----


    def onSequence(self, evt):
        """Update gui."""
        evt.Skip()
        wx.CallAfter(self.onSequenceChanged)
    # ----


    def onSequenceChanged(self):
        """Update info and erase results if sequence has changed."""

        # update sequence info
        self.updateSequenceInfo()

        # skip if sequence has not changed - cursor move only
        if self.sequenceCanvas.isModified():
            self.sequenceCanvas.setModified(False)

            # update modifications panel
            self.updateAvailableResidues()
            self.updateModificationsList()

            # update digest panel
            if self.currentDigest !=None:
                self.currentDigest = None
                self.updateDigestList()

            # update fragment panel
            if self.currentFragments !=None:
                self.currentFragments = None
                self.updateFragmentsList()

            # update search panel
            if self.currentSearch !=None:
                self.currentSearch = None
                self.updateSearchList()

            # close match panel
            if self.matchPanel:
                self.matchPanel.Close()

            # erase matches
            if self.currentSequence.matches:
                del self.currentSequence.matches[:]
                self.parent.onDocumentChanged('matches')
    # ----


    def onSequencePattern(self, evt):
        """Show isotopic pattern for whole sequence."""

        # get formula
        if len(self.currentSequence) != 0:
            formula = self.currentSequence.getFormula()
            config.masscalc['patternFwhm'] = 0.5
        else:
            wx.Bell()
            return

        # send to masscalc
        self.parent.onToolsMasscalc(formula=formula)
    # ----


    def onAddModification(self, evt):
        """Get data and add modification."""

        # get data
        try:
            residue = self.modsResidue_combo.GetValue()
            position = self.modsPosition_combo.GetValue()
            modification = self.modsMod_combo.GetValue()
            modtype = self.modsType_combo.GetValue()
        except:
            return
        if not (position and modification and modtype):
            return

        # set residual modification
        pos = position.split(' ')
        if pos[0] == 'All':
            amino = pos[1]
        else:
            amino = int(pos[1])-1
        modtype = modtype[0].lower()
        self.currentSequence.modify(modification, amino, modtype)

        # update gui
        self.sequenceCanvas.setModified(True)
        self.sequenceCanvas.refresh()
        self.onSequenceChanged()
    # ----


    def onRemoveModifications(self, evt):
        """Remove selected modifications."""

        # get selected
        selected = self.modificationsList.getSelected()
        if not selected:
            return

        # delete modifications
        for index in selected:

            # get position
            position = self.modificationsList.GetItem(index, 0).GetText()
            pos = position.split(' ')
            if pos[0] == 'All':
                amino = pos[1]
            else:
                amino = int(pos[1])-1

            # get name
            name = self.modificationsList.GetItem(index, 1).GetText()

            # get type
            modtype = self.modificationsList.GetItem(index, 2).GetText()
            modtype = modtype[0]

            # delete modification
            self.currentSequence.removeModification([name, amino, modtype])

        # update gui
        self.sequenceCanvas.setModified(True)
        self.sequenceCanvas.refresh()
        self.onSequenceChanged()
    # ----


    def onSpecifityFilter(self, evt):
        """Update modifications according to specifity filter."""
        self.updateAvailableModifications()
    # ----


    def onResidueSelected(self, evt):
        """Update available positions and modifications."""

        self.updateAvailablePositions()
        self.updateAvailableModifications()
    # ----


    def onPositionSelected(self, evt):
        """Update available modifications for selected position."""
        self.updateAvailableModifications()
    # ----


    def onItemSelected(self, evt):
        """Show selected mass in spectrum canvas."""

        # get mass
        if self.currentTool=='digest':
            mz = self.currentDigest[evt.GetData()][2]
        elif self.currentTool=='fragment':
            mz = self.currentFragments[evt.GetData()][3]
        elif self.currentTool=='search':
            mz = self.currentSearch[evt.GetData()][1]

        # show mass
        self.parent.showMassPoints([mz])
    # ----


    def onItemActivated(self, evt):
        """Show isotopic pattern for selected peptide."""

        # get formula and charge
        if self.currentTool=='digest':
            item = self.currentDigest[evt.GetData()]
            formula = item[6].getFormula()
            charge = item[3]
        elif self.currentTool=='fragment':
            item = self.currentFragments[evt.GetData()]
            formula = item[7].getFormula()
            charge = item[4]
        elif self.currentTool=='search':
            item = self.currentSearch[evt.GetData()]
            formula = item[5].getFormula()
            charge = item[2]

        # send to masscalc
        self.parent.onToolsMasscalc(formula=formula, charge=charge)
    # ----


    def onKey(self, evt):
        """Export list if Ctrl+C."""

        # get key
        key = evt.GetKeyCode()

        # copy
        if key == 67 and evt.CmdDown():
            self.copyToClipboard()

        # other keys
        else:
            evt.Skip()
    # ----


    def onDigest(self, evt):
        """Digest sequence."""

        # clear previous data
        self.currentDigest = None

        # close match panel
        if self.matchPanel:
            self.matchPanel.Close()

        # get params
        if not self.getParams():
            self.updateDigestList()
            return

        # show processing gauge
        self.onProcessing(True)
        self.digestGenerate_butt.Enable(False)
        self.digestMatch_butt.Enable(False)
        self.digestStore_butt.Enable(False)

        # do processing
        self.processing = threading.Thread(target=self.doDigestion)
        self.processing.start()

        # pulse gauge while working
        while self.processing.isAlive():
            self.gauge.pulse()

        # update digest list
        self.updateDigestList()

        # hide processing gauge
        self.onProcessing(False)
        self.digestGenerate_butt.Enable(True)
        self.digestMatch_butt.Enable(True)
        self.digestStore_butt.Enable(True)
    # ----


    def onFragment(self, evt):
        """Fragment sequence."""

        # clear previous data
        self.currentFragments = None

        # close match panel
        if self.matchPanel:
            self.matchPanel.Close()

        # get params
        if not self.getParams():
            self.updateFragmentsList()
            return

        # show processing gauge
        self.onProcessing(True)
        self.fragmentGenerate_butt.Enable(False)
        self.fragmentMatch_butt.Enable(False)
        self.fragmentStore_butt.Enable(False)

        # do processing
        self.processing = threading.Thread(target=self.doFragmentation)
        self.processing.start()

        # pulse gauge while working
        while self.processing.isAlive():
            self.gauge.pulse()

        # update digest list
        self.updateFragmentsList()

        # hide processing gauge
        self.onProcessing(False)
        self.fragmentGenerate_butt.Enable(True)
        self.fragmentMatch_butt.Enable(True)
        self.fragmentStore_butt.Enable(True)
    # ----


    def onSearch(self, evt):
        """Search for mass in sequence."""

        # clear previous data
        self.currentSearch = None

        # close match panel
        if self.matchPanel:
            self.matchPanel.Close()

        # get params
        if not self.getParams():
            self.updateSearchList()
            return

        # show processing gauge
        self.onProcessing(True)
        self.searchGenerate_butt.Enable(False)

        # do processing
        self.processing = threading.Thread(target=self.doSearch)
        self.processing.start()

        # pulse gauge while working
        while self.processing.isAlive():
            self.gauge.pulse()

        # update search list
        self.updateSearchList()

        # hide processing gauge
        self.onProcessing(False)
        self.searchGenerate_butt.Enable(True)
    # ----


    def onMatch(self, evt):
        """Match data to current peaklist."""

        # init match panel
        if not self.matchPanel:

            # get current peaklist and show panel
            peaklist = self.parent.getCurrentPeaklist()
            if peaklist:

                # show panel
                self.matchPanel = panelMatch(self)
                self.matchPanel.Centre()
                self.matchPanel.Show(True)

                # set data
                if self.currentTool == 'digest':
                    self.matchPanel.setData('digest', self.currentDigest, peaklist)
                elif self.currentTool == 'fragment':
                    self.matchPanel.setData('fragment', self.currentFragments, peaklist)
            else:
                wx.Bell()
                return

        # match data
        else:
            self.matchPanel.Raise()
            self.matchPanel.onMatch()
    # ----


    def onStore(self, evt):
        """Store matches in document."""

        buff = []

        # get digest data
        if self.currentTool == 'digest' and self.currentDigest:
            for item in self.currentDigest:
                obj = item[6]
                title = '%s' % (obj.getFormated(config.sequence['digest']['matchFormat']))
                for match in item[-1]:
                    match.label = title
                    match.charge = item[3]
                    match.charge = item[3]
                    match.formula = obj.getFormula()
                    match.sequenceRange = obj.userRange[:]
                    buff.append((match.peakMZ, match.getDelta('Da'), match))

        # get fragment data
        elif self.currentTool == 'fragment' and self.currentFragments:
            for item in self.currentFragments:
                obj = item[7]
                title = '%s' % (obj.getFormated(config.sequence['fragment']['matchFormat']))
                for match in item[-1]:
                    match.label = title
                    match.charge = item[4]
                    match.formula = obj.getFormula()
                    match.fragmentSerie = obj.fragmentSerie
                    match.fragmentIndex = obj.fragmentIndex
                    buff.append((match.peakMZ, match.getDelta('Da'), match))

        # check data
        if buff:
            buff.sort()
            matches = []
            for match in buff:
                matches.append(match[2])
        else:
            wx.Bell()
            return

        # store matches
        self.currentSequence.matches = matches
        self.parent.onDocumentChanged('matches')
    # ----


    def setData(self, sequence=None):
        """Set current sequence."""

        # check sequence
        if sequence == None:
            sequence = mspy.sequence('')

        # set data
        self.currentSequence = sequence
        self.sequenceTitle_value.SetValue(self.currentSequence.title)
        self.sequenceCanvas.setData(self.currentSequence)
        self.sequenceCanvas.setModified(False)

        # update sequence info
        self.updateSequenceInfo()

        # update modifications panel
        self.updateAvailableResidues()
        self.updateModificationsList()

        # update digest panel
        if self.currentDigest !=None:
            self.currentDigest = None
            self.updateDigestList()

        # update fragment panel
        if self.currentFragments !=None:
            self.currentFragments = None
            self.updateFragmentsList()

        # update search panel
        if self.currentSearch !=None:
            self.currentSearch = None
            self.updateSearchList()

        # close match panel
        if self.matchPanel:
            self.matchPanel.Close()
    # ----


    def getParams(self):
        """Get all params from dialog."""

        # try to get values
        try:

            # digest
            if self.currentTool == 'digest':

                config.sequence['digest']['maxCharge'] = int(self.digestMaxCharge_value.GetValue())
                config.sequence['digest']['massType'] = 0
                if self.digestMassTypeAv_radio.GetValue():
                    config.sequence['digest']['massType'] = 1

                config.sequence['digest']['enzyme'] = self.digestEnzyme_combo.GetValue()
                config.sequence['digest']['miscl'] = int(self.digestMiscl_value.GetValue())
                config.sequence['digest']['lowMass'] = int(self.digestLowMass_value.GetValue())
                config.sequence['digest']['highMass'] = int(self.digestHighMass_value.GetValue())

                config.sequence['digest']['allowMods'] = 0
                if self.digestAllowMods_check.GetValue():
                    config.sequence['digest']['allowMods'] = 1

            # fragments
            elif self.currentTool == 'fragment':

                config.sequence['fragment']['maxCharge'] = int(self.fragmentMaxCharge_value.GetValue())
                config.sequence['fragment']['massType'] = 0
                if self.fragmentMassTypeAv_radio.GetValue():
                    config.sequence['fragment']['massType'] = 1

                config.sequence['fragment']['fragments'] = []
                if self.fragmentA_check.GetValue():
                    config.sequence['fragment']['fragments'].append('a')
                if self.fragmentB_check.GetValue():
                    config.sequence['fragment']['fragments'].append('b')
                if self.fragmentC_check.GetValue():
                    config.sequence['fragment']['fragments'].append('c')
                if self.fragmentX_check.GetValue():
                    config.sequence['fragment']['fragments'].append('x')
                if self.fragmentY_check.GetValue():
                    config.sequence['fragment']['fragments'].append('y')
                if self.fragmentZ_check.GetValue():
                    config.sequence['fragment']['fragments'].append('z')
                if self.fragmentNH3_check.GetValue():
                    config.sequence['fragment']['fragments'].append('-NH3')
                if self.fragmentH2O_check.GetValue():
                    config.sequence['fragment']['fragments'].append('-H2O')
                if self.fragmentInt_check.GetValue():
                    config.sequence['fragment']['fragments'].append('int')
                if self.fragmentNLadder_check.GetValue():
                    config.sequence['fragment']['fragments'].append('n-ladder')
                if self.fragmentCLadder_check.GetValue():
                    config.sequence['fragment']['fragments'].append('c-ladder')

                if self.fragmentFilter_check.GetValue():
                    config.sequence['fragment']['filterFragments'] = 1
                else:
                    config.sequence['fragment']['filterFragments'] = 0

            # search
            elif self.currentTool == 'search':

                config.sequence['search']['maxCharge'] = int(self.searchMaxCharge_value.GetValue())
                config.sequence['search']['massType'] = 0
                if self.searchMassTypeAv_radio.GetValue():
                    config.sequence['search']['massType'] = 1

                config.sequence['search']['tolerance'] = float(self.searchTolerance_value.GetValue())
                config.sequence['search']['units'] = 'Da'
                if self.searchUnitsPpm_radio.GetValue():
                    config.sequence['search']['units'] = 'ppm'

                config.sequence['search']['mass'] = float(self.searchMass_value.GetValue())

            return True

        except:
            wx.Bell()
            return False
    # ----


    def updateSequenceInfo(self):
        """Update sequence info."""

        # make label
        label = ''
        length = len(self.currentSequence)

        if length > 0:
            format = '%0.' + `config.main['mzDigits']` + 'f'
            mass = self.currentSequence.getMass()
            selection = self.sequenceCanvas.getSequenceSelection()

            label += 'Mo: '+format % mass[0]
            label += '     Av: '+format % mass[1]

            if selection[0]==selection[1]:
                label += '     Position: %s/%s' % (selection[0]+1,length)
            elif selection[1] > length:
                label += '     Selection: %s-%s' % ((selection[0]+1), selection[1]-1)
            else:
                label += '     Selection: %s-%s' % ((selection[0]+1), selection[1])

        self.sequenceInfo_label.SetLabel(label)
    # ----


    def updateAvailableResidues(self):
        """Update available residues."""

        # clear
        self.modsResidue_combo.Clear()
        self.modsPosition_combo.Clear()
        self.modsMod_combo.Clear()

        # get residues
        residues = []
        for amino in self.currentSequence.chain:
            name = '%s (%s)' % (mspy.aminoacids[amino].name, amino)
            if not name in residues:
                residues.append(name)

        # update combo
        for res in sorted(residues):
            self.modsResidue_combo.Append(res)
    # ----


    def updateAvailablePositions(self):
        """Update available positions."""

        # clear
        self.modsPosition_combo.Clear()

        # get selected residue
        residue = self.modsResidue_combo.GetValue()

        # residual modifications
        residue = residue[-2]
        positions = ['All ' + residue]
        for x, amino in enumerate(self.currentSequence.chain):
            if amino == residue:
                pos = '%s %s' % (amino, x+1)
                positions.append(pos)

        # update positions
        for pos in positions:
            self.modsPosition_combo.Append(str(pos))

        # select first
        self.modsPosition_combo.Select(0)
    # ----


    def updateAvailableModifications(self):
        """Update available modifications."""

        # clear
        self.modsMod_combo.Clear()

        # get selected residue
        try:
            residue = self.modsResidue_combo.GetValue()
            position = self.modsPosition_combo.GetValue()
        except:
            return

        mods = []

        # get residual modifications
        residue = residue[-2]
        checkSpecifity = self.modsSpecifity_check.GetValue()
        for mod in mspy.modifications:
            if not checkSpecifity or residue in mspy.modifications[mod].aminoSpecifity:
                mods.append(mod)

        # update modifications
        for mod in sorted(mods):
            self.modsMod_combo.Append(mod)
    # ----


    def updateModificationsList(self):
        """Update current modifications."""

        # clear previous data
        self.modificationsList.DeleteAllItems()

        # check sequence
        if self.currentSequence == None:
            return

        currentMods = []
        format = '%0.' + `config.main['mzDigits']` + 'f'

        # get residual modifications
        for mod in self.currentSequence.modifications:
            name = mod[0]

            # format position
            if type(mod[1]) == int:
                position = '%s %s' % (self.currentSequence.chain[mod[1]], mod[1]+1)
            else:
                position = 'All ' + mod[1]

            # format type
            if mod[2] == 'f':
                modtype = 'fixed'
            else:
                modtype = 'variable'

            # format masses
            massMo = format % mspy.modifications[name].mass[0]
            massAv = format % mspy.modifications[name].mass[1]

            # format formula
            formula = mspy.modifications[name].gainFormula
            if mspy.modifications[name].lossFormula:
                formula += ' - ' + mspy.modifications[name].lossFormula

            # append data
            currentMods.append((position, name, modtype, massMo, massAv, formula))

        # set current data to sorter
        self.modificationsList.setDataMap(currentMods)

        # update list
        for row, item in enumerate(currentMods):
            self.modificationsList.InsertStringItem(row, item[0])
            self.modificationsList.SetStringItem(row, 1, item[1])
            self.modificationsList.SetStringItem(row, 2, item[2])
            self.modificationsList.SetStringItem(row, 3, item[3])
            self.modificationsList.SetStringItem(row, 4, item[4])
            self.modificationsList.SetStringItem(row, 5, item[5])
            self.modificationsList.SetItemData(row, row)

        # sort data
        self.modificationsList.sort()

        # scroll top
        if currentMods:
            self.modificationsList.EnsureVisible(0)
    # ----


    def updateDigestList(self):
        """Update digest list."""

        # clear previous data and set new
        self.digestList.DeleteAllItems()
        self.digestList.setDataMap(self.currentDigest)

        # check data
        if not self.currentDigest:
            return

        # add new data
        format = '%0.' + `config.main['mzDigits']` + 'f'
        fontMatched = wx.Font(mwx.SMALL_FONT_SIZE, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        for row, item in enumerate(self.currentDigest):

            # format data
            userRange = '[%s-%s]' % tuple(item[0])
            mz = format % (item[2])

            if item[5] != None:
                error = str(item[5])
            else:
                error = ''

            # add data
            self.digestList.InsertStringItem(row, userRange)
            self.digestList.SetStringItem(row, 1, str(item[1]))
            self.digestList.SetStringItem(row, 2, mz)
            self.digestList.SetStringItem(row, 3, str(item[3]))
            self.digestList.SetStringItem(row, 4, item[4])
            self.digestList.SetStringItem(row, 5, error)
            self.digestList.SetItemData(row, row)

            # mark matched
            if item[5] != None:
                self.digestList.SetItemTextColour(row, (0,200,0))
                self.digestList.SetItemFont(row, fontMatched)

        # sort data
        self.digestList.sort()

        # scroll top
        self.digestList.EnsureVisible(0)
    # ----


    def updateFragmentsList(self):
        """Update fragments list."""

        # clear previous data and set new
        self.fragmentsList.DeleteAllItems()
        self.fragmentsList.setDataMap(self.currentFragments)

        # check data
        if not self.currentFragments:
            return

        # add new data
        format = '%0.' + `config.main['mzDigits']` + 'f'
        filtered = wx.Font(mwx.SMALL_FONT_SIZE, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
        for row, item in enumerate(self.currentFragments):

            # format data
            if type(item[1]) == int:
                index = str(item[1])
            else:
                index = '[%s-%s]' % tuple(item[1])

            urange = '[%s-%s]' % tuple(item[2])
            mz = format % (item[3])

            if item[6] != None:
                error = str(item[6])
            else:
                error = ''

            # add data
            self.fragmentsList.InsertStringItem(row, item[0])
            self.fragmentsList.SetStringItem(row, 1, index)
            self.fragmentsList.SetStringItem(row, 2, urange)
            self.fragmentsList.SetStringItem(row, 3, mz)
            self.fragmentsList.SetStringItem(row, 4, str(item[4]))
            self.fragmentsList.SetStringItem(row, 5, item[5])
            self.fragmentsList.SetStringItem(row, 6, error)
            self.fragmentsList.SetItemData(row, row)

            # mark filtered
            if item[7].fragFiltered:
                self.fragmentsList.SetItemTextColour(row, (150,150,150))
                self.fragmentsList.SetItemFont(row, filtered)

            # mark matched
            if item[6] != None:
                self.fragmentsList.SetItemTextColour(row, (0,200,0))

        # sort data
        self.fragmentsList.sort()

        # scroll top
        self.fragmentsList.EnsureVisible(0)
    # ----


    def updateSearchList(self):
        """Update search list."""

        # clear previous data and set new
        self.searchList.DeleteAllItems()
        self.searchList.setDataMap(self.currentSearch)

        # check data
        if not self.currentSearch:
            return

        # add new data
        format = '%0.' + `config.main['mzDigits']` + 'f'
        formatErr = '%0.' + `config.main['mzDigits']` + 'f'
        if config.sequence['search']['units'] == 'ppm':
            formatErr = '%0.1f'

        for row, item in enumerate(self.currentSearch):

            # format data
            userRange = '[%s-%s]' % tuple(item[0])
            mz = format % (item[1])
            error = formatErr % (item[4])

            # add data
            self.searchList.InsertStringItem(row, userRange)
            self.searchList.SetStringItem(row, 1, mz)
            self.searchList.SetStringItem(row, 2, str(item[2]))
            self.searchList.SetStringItem(row, 3, item[3])
            self.searchList.SetStringItem(row, 4, error)
            self.searchList.SetItemData(row, row)

        # sort data
        self.searchList.sort()

        # scroll top
        self.searchList.EnsureVisible(0)
    # ----


    def updateMatches(self, resultList=None):
        """Update current list."""

        # choose current
        if not resultList:
            resultList = self.currentTool

        # update digest list
        if self.currentTool == 'digest':
            self.updateDigestList()

        # update fragments list
        elif self.currentTool == 'fragment':
            self.updateFragmentsList()
    # ----


    def doDigestion(self):
        """Perform protein digest."""

        # digest sequence
        peptides = mspy.digest(self.currentSequence, config.sequence['digest']['enzyme'], miscleavage=config.sequence['digest']['miscl'], allowMods=config.sequence['digest']['allowMods'], strict=False)

        # do not cleave if modified
        enzyme=config.sequence['digest']['enzyme']
        if config.sequence['digest']['allowMods']:
            enzyme = None

        # get variations for each peptide
        variants = []
        for peptide in peptides:
            variants += mspy.variateMods(peptide, position=False, maxMods=config.sequence['digest']['maxMods'], enzyme=enzyme)
        peptides = variants

        # get max charge and polarity
        polarity = 1
        if config.sequence['digest']['maxCharge'] < 0:
            polarity = -1
        maxCharge = abs(config.sequence['digest']['maxCharge'])+1

        # calculate mz and check limits
        self.currentDigest = []
        for peptide in peptides:
            for z in range(1, maxCharge):
                mz = peptide.getMZ(z*polarity)[config.sequence['digest']['massType']]
                if mz >= config.sequence['digest']['lowMass'] and mz <= config.sequence['digest']['highMass']:
                    self.currentDigest.append([
                        peptide.userRange,
                        peptide.miscleavages,
                        mz,
                        z*polarity,
                        peptide.getFormated(config.sequence['digest']['listFormat']),
                        None,
                        peptide,
                        [],
                    ])
    # ----


    def doFragmentation(self):
        """Perform peptide fragmentation."""

        # get fragment types
        series = []

        if 'a' in config.sequence['fragment']['fragments']:
            series.append('a')
        if 'b' in config.sequence['fragment']['fragments']:
            series.append('b')
        if 'y' in config.sequence['fragment']['fragments']:
            series.append('y')

        for serie in series[:]:
            if '-NH3' in config.sequence['fragment']['fragments']:
                series.append(serie+'-NH3')
            if '-H2O' in config.sequence['fragment']['fragments']:
                series.append(serie+'-H2O')

        if 'c' in config.sequence['fragment']['fragments']:
            series.append('c')
        if 'x' in config.sequence['fragment']['fragments']:
            series.append('x')
        if 'z' in config.sequence['fragment']['fragments']:
            series.append('z')
        if 'int' in config.sequence['fragment']['fragments']:
            series.append('int')
            series.append('int-CO')
            series.append('int-NH3')
            series.append('int-H2O')
        if 'n-ladder' in config.sequence['fragment']['fragments']:
            series.append('n-ladder')
        if 'c-ladder' in config.sequence['fragment']['fragments']:
            series.append('c-ladder')

        # fragment sequence
        fragments = []
        for serie in series:
            fragments += mspy.fragment(self.currentSequence, serie)

        # variate mods
        variants = []
        for fragment in fragments:
            variants += mspy.variateMods(fragment, position=False, maxMods=config.sequence['fragment']['maxMods'])
        fragments = variants

        # get max charge and polarity
        polarity = 1
        if config.sequence['fragment']['maxCharge'] < 0:
            polarity = -1
        maxCharge = abs(config.sequence['fragment']['maxCharge'])+1

        # calculate mz and check limits
        self.currentFragments = []
        for fragment in fragments:
            for z in range(1, maxCharge):
                if not config.sequence['fragment']['filterFragments'] or not fragment.fragFiltered:
                    self.currentFragments.append([
                        fragment.fragmentSerie,
                        fragment.fragmentIndex,
                        fragment.userRange,
                        fragment.getMZ(z*polarity)[config.sequence['fragment']['massType']],
                        z*polarity,
                        fragment.getFormated(config.sequence['fragment']['listFormat']),
                        None,
                        fragment,
                        [],
                    ])
    # ----


    def doSearch(self):
        """Perform mass search."""

        # get max charge and polarity
        polarity = 1
        if config.sequence['search']['maxCharge'] < 0:
            polarity = -1
        maxCharge = abs(config.sequence['search']['maxCharge'])+1

        # search sequence
        self.currentSearch = []
        for z in range(1, maxCharge):
            charge = z*polarity
            peptides = mspy.searchSequence(self.currentSequence, config.sequence['search']['mass'], charge, tolerance=config.sequence['search']['tolerance'], enzyme=config.sequence['search']['enzyme'], tolUnits=config.sequence['search']['units'], massType=config.sequence['search']['massType'], maxMods=config.sequence['search']['maxMods'])
            for peptide in peptides:
                mz = peptide.getMZ(charge)[config.sequence['search']['massType']]
                self.currentSearch.append([
                    peptide.userRange,
                    mz,
                    charge,
                    peptide.getFormated(config.sequence['search']['listFormat']),
                    mspy.delta(mz, config.sequence['search']['mass'], config.sequence['search']['units']),
                    peptide,
                ])
    # ----


    def copyToClipboard(self):
        """Export current results list."""

        # get current list
        if self.currentTool == 'digest':
            currentList = self.digestList
        elif self.currentTool == 'fragment':
            currentList = self.fragmentsList
        elif self.currentTool == 'search':
            currentList = self.searchList
        else:
            return

        # get data
        buff = ''
        for row in range(currentList.GetItemCount()):
            for col in range(currentList.GetColumnCount()):
                item = currentList.GetItem(row, col)
                buff += item.GetText() + '\t'
            buff += '\n'

        # make text object for data
        obj = wx.TextDataObject()
        obj.SetText(buff)

        # paste to clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(obj)
            wx.TheClipboard.Close()
    # ----




class sequenceCanvas(wx.TextCtrl):
    """Sequence editor canvas."""

    def __init__(self, parent, id, sequence=None, size=(-1,-1), style=wx.TE_MULTILINE|wx.TE_RICH):
        wx.TextCtrl.__init__(self, parent, id, size=size, style=style)

        self.parent = parent
        self.modified = False

        # make sequence
        if isinstance(sequence, mspy.sequence):
            self.currentSequence = sequence
        elif sequence == None:
            self.currentSequence = mspy.sequence('')
        elif type(sequence) in (str, unicode):
            self.currentSequence = mspy.sequence(sequence)

        # set events
        self.Bind(wx.EVT_KEY_DOWN, self._onKey)

        # set fonts
        self.styles = {
            'default': wx.TextAttr(colText=(0,0,0), font=wx.Font(mwx.SEQUENCE_FONT_SIZE, wx.MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)),
            'modified': wx.TextAttr(colText=(255,0,0), font=wx.Font(mwx.SEQUENCE_FONT_SIZE, wx.MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)),
        }
        self.SetDefaultStyle(self.styles['default'])

        # show current sequence
        self.updateCanvas()
    # ----


    def _onKey(self, evt):
        """Check character and update sequence."""

        # get key
        key = evt.GetKeyCode()

        # get selections
        curSelection = self.GetSelection()
        seqSelection = self._positionEditorToSequence(curSelection)

        # skip navigation keys
        if key in (wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_UP, wx.WXK_DOWN, wx.WXK_HOME, wx.WXK_END, wx.WXK_PAGEUP, wx.WXK_PAGEDOWN):
            evt.Skip()
            return

        # select all
        elif key == 65 and evt.CmdDown():
            evt.Skip()
            return

        # copy selection to clipboard
        elif key == 67 and evt.CmdDown():
            evt.Skip()
            return

        # paste sequence
        elif key == 86 and evt.CmdDown():
            sequence = self.getSequenceFromClipboard()
            if sequence:
                self.currentSequence[seqSelection[0]:seqSelection[1]] = sequence
                self.updateCanvas()
                self.setInsertionPoint(seqSelection[0]+len(sequence))
                self.modified = True

        # delete
        elif key == wx.WXK_DELETE:
            if seqSelection[0] == seqSelection[1]:
                del self.currentSequence[seqSelection[0]:seqSelection[1]+1]
            else:
                del self.currentSequence[seqSelection[0]:seqSelection[1]]
            self.updateCanvas()
            self.setInsertionPoint(seqSelection[0])
            self.modified = True

        # backspace
        elif key == wx.WXK_BACK:
            if seqSelection[0] == seqSelection[1] and seqSelection[0] != 0:
                del self.currentSequence[seqSelection[0]-1:seqSelection[1]]
                self.updateCanvas()
                self.setInsertionPoint(seqSelection[0]-1)
                self.modified = True
            else:
                del self.currentSequence[seqSelection[0]:seqSelection[1]]
                self.updateCanvas()
                self.setInsertionPoint(seqSelection[0])
                self.modified = True

        # text
        elif key >= 65 and key <= 121:
            char = chr(key)
            char.upper()
            if char in mspy.aminoacids:
                self.currentSequence[seqSelection[0]:seqSelection[1]] = mspy.sequence(char)
                self.updateCanvas()
                self.setInsertionPoint(seqSelection[0]+1)
                self.modified = True
            else:
                wx.Bell()
                return

        # all other keys
        else:
            return
    # ----


    def _positionEditorToSequence(self, selection):
        """Get sequence coordinates for editor selection."""

        selection = list(selection)
        selection[0] -= self.GetRange(0,selection[0]).count(' ')
        selection[1] -= self.GetRange(0,selection[1]).count(' ')

        return selection
    # ----


    def _positionSequenceToEditor(self, selection):
        """Get editor coordinates for sequence selection."""

        selection = list(selection)
        selection[0] += divmod(selection[0], 10)[0]
        selection[1] += divmod(selection[1], 10)[0]

        return selection
    # ----


    def setData(self, sequence):
        """Set sequence object."""

        # make sequence
        if isinstance(sequence, mspy.sequence):
            self.currentSequence = sequence
        elif sequence == None:
            self.currentSequence = mspy.sequence('')
        elif type(sequence) in (str, unicode):
            self.currentSequence = mspy.sequence(sequence)

        # set modified
        self.modified = True

        # update gui
        self.updateCanvas()
    # ----


    def setInsertionPoint(self, pos):
        """Set insertion point in editor for current sequence position."""

        start, stop = self._positionSequenceToEditor([pos,pos])
        self.SetInsertionPoint(start)
    # ----


    def setModified(self, status=True):
        """Set modified status."""
        self.modified = status
    # ----


    def getData(self):
        """Get current sequence."""
        return self.currentSequence
    # ----


    def getSequenceSelection(self):
        """Get current selection in sequence coordinations."""
        return self._positionEditorToSequence(self.GetSelection())
    # ----


    def getSequenceFromClipboard(self):
        """Get sequence from clipboard."""

        # get data from clipboard
        success = False
        data = wx.TextDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(data)
            wx.TheClipboard.Close()

        # parse sequence if data in clipboard
        if success:

            # get text from clipboard
            data = data.GetText()

            # remove whitespaces
            for char in ('\t','\n','\r','\f','\v', ' ', '-', '*', '.'):
                data = data.replace(char, '')

            # remove numbers
            for char in ('0','1','2','3','4','5','6','7','8','9'):
                data = data.replace(char, '')

            # make sequence object
            try:
                sequence = mspy.sequence(data)
                return sequence
            except:
                pass

        wx.Bell()
        return False
    # ----


    def updateCanvas(self):
        """Show current sequence in canvas."""

        # format and sequence
        sequence = ''
        modifications = []
        for x, amino in enumerate(self.currentSequence.chain):
            sequence += amino
            if not (x+1) % 10:
                sequence += ' '
            if self.currentSequence.isModified(x, True):
                modifications.append(x)

        # update sequence
        self.ChangeValue(sequence)

        # set default style
        self.SetStyle(0, len(sequence), self.styles['default'])

        # highlight modifications
        for pos in modifications:
            x, y = self._positionSequenceToEditor([pos, pos])
            self.SetStyle(x, x+1, self.styles['modified'])
    # ----


    def refresh(self):
        """Redraw current sequence."""
        self.updateCanvas()
    # ----


    def isModified(self):
        """Modified status."""
        return self.modified
    # ----

def doFrag(curSeq):
    """Perform peptide fragmentation."""

    # get fragment types
    serTypeDict = {}
    serTypeDict['a'] = 1
    serTypeDict['b'] = 2
    serTypeDict['y'] = 3
    serTypeDict['-NH3'] = 4
    serTypeDict['-H2O'] = 5
    serTypeDict['c'] = 6
    serTypeDict['x'] = 7
    serTypeDict['z'] = 8
    serTypeDict['int'] = 9
    serTypeDict['int-CO'] = 10
    serTypeDict['int-NH3'] = 11
    serTypeDict['int-H2O'] = 12
    serTypeDict['n-ladder'] = 13
    serTypeDict['c-ladder'] = 14

    series = []
    #series.append('a')
    series.append('b')
    series.append('y')
#    series.append('a-H2O')
#    series.append('b-H2O')
    #series.append('y-H2O')
    #series.append('int')
    i = 0
    serTypeDict = {}
    #config.sequence['fragment']['fragments'].append('a')
    config.sequence['fragment']['fragments'].append('b')
    serTypeDict[config.sequence['fragment']['fragments'][-1]] = i
    i+=1
    config.sequence['fragment']['fragments'].append('y')
    serTypeDict[config.sequence['fragment']['fragments'][-1]] = i
    i+=1
#    config.sequence['fragment']['fragments'].append('a-H2O')
#    serTypeDict[config.sequence['fragment']['fragments'][-1]] = i
#    i+=1
#    config.sequence['fragment']['fragments'].append('b-H2O')
#    serTypeDict[config.sequence['fragment']['fragments'][-1]] = i
#    i+=1
    #config.sequence['fragment']['fragments'].append('y-H2O')
    #config.sequence['fragment']['fragments'].append('int')

#    i = 0
#
#    if 'a' in config.sequence['fragment']['fragments']:
#        series.append('a')
#        serTypeDict['a']=i
#        i+=1
#    if 'b' in config.sequence['fragment']['fragments']:
#        series.append('b')
#        serTypeDict['b'] = i
#        i+=1
#    if 'y' in config.sequence['fragment']['fragments']:
#        series.append('y')
#        serTypeDict['y'] = i
#        i+=1
#    for serie in series[:]:
#        if '-NH3' in config.sequence['fragment']['fragments']:
#            series.append(serie+'-NH3')
#            serTypeDict[serie+'-NH3'] = i
#            i+=1
#        if '-H2O' in config.sequence['fragment']['fragments']:
#            series.append(serie+'-H2O')
#            serTypeDict[serie+'-H2O'] = i
#            i+=1
#
#    if 'c' in config.sequence['fragment']['fragments']:
#        series.append('c')
#        serTypeDict['c'] = i
#        i+=1
#    if 'x' in config.sequence['fragment']['fragments']:
#        series.append('x')
#        serTypeDict['x'] = i
#        i+=1
#    if 'z' in config.sequence['fragment']['fragments']:
#        series.append('z')
#        serTypeDict['z'] = i
#        i+=1
#    if 'int' in config.sequence['fragment']['fragments']:
#        series.append('int')
#        serTypeDict['int'] = i
#        i+=1
#        series.append('int-CO')
#        serTypeDict['int-CO'] = i
#        i+=1
#        series.append('int-NH3')
#        serTypeDict['int-NH3'] = i
#        i+=1
#        series.append('int-H2O')
#        serTypeDict['int-H2O'] = i
#        i+=1
#
#    if 'n-ladder' in config.sequence['fragment']['fragments']:
#        series.append('n-ladder')
#        serTypeDict['n-ladder'] = i
#        i+=1
#
#    if 'c-ladder' in config.sequence['fragment']['fragments']:
#        series.append('c-ladder')
#        serTypeDict['c-ladder'] = i
#        i+=1


    # fragment sequence
    fragments = []
    for serie in series:
        fragments += mspy.fragment(curSeq, serie)

    # variate mods
    variants = []
    for fragment in fragments:
        variants += mspy.variateMods(fragment, position=False, maxMods=config.sequence['fragment']['maxMods'])
    fragments = variants

    # get max charge and polarity
    polarity = 1
    if config.sequence['fragment']['maxCharge'] < 0:
        polarity = -1
    maxCharge = abs(config.sequence['fragment']['maxCharge'])+1

    # calculate mz and check limits
    curFrags = []
    for i,fragment in enumerate(fragments):
        for z in range(1, maxCharge):
            if not config.sequence['fragment']['filterFragments'] or not fragment.fragFiltered:
                curFrags.append([
                    serTypeDict[str(fragment.fragmentSerie)],
                    fragment.fragmentSerie,
                    fragment.fragmentIndex,
                    fragment.userRange,
                    fragment.getMZ(z*polarity)[config.sequence['fragment']['massType']],
                    z*polarity,
                    fragment.getFormated(config.sequence['fragment']['listFormat']),
                    None,
                    fragment,
                    [],
                ])

#    print serTypeDict
    return curFrags, series
# ----


def main():

    COLORS = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
    '#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
    '#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
    '#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

    pep = 'CPNPPVQENFDVNK'
    mz = N.array([360.051, 371.971, 408.168, 475.257, 572.221, 592.733, 595.249, 605.034, 623.413, 635.276, 642.189,
          643.776, 648.206, 683.262, 690.683, 692.273, 700.84, 716.189, 719.344, 736.303, 749.344, 763.286,
          778.233, 780.335, 793.199, 798.8, 800.332, 812.339, 820.361, 847.438, 865.363, 866.429, 922.456,
          927.432, 959.562, 976.43, 993.534, 1092.5, 1124.54, 1140.53, 1166.53, 1171.66, 1190.57, 1268.53,
          1270.57, 1280.47, 1286.69, 1298.55, 1387.6, 1401.68])
    yVals = N.array([6, 14, 6, 6, 5, 7, 14, 4, 4, 12, 8, 100, 5, 5, 5, 10, 57, 5, 8, 21, 7, 5, 5, 4, 5, 5, 6, 12, 48, 6,
                     10, 5, 7, 9, 4, 22, 10, 5, 6, 4, 9, 6, 23, 5, 7, 4, 90, 9, 4, 7])

    sortInd = mz.argsort()
    mz = mz[sortInd]
    yVals = yVals[sortInd]


    curSeq = mspy.sequence(pep)
    ans, series = doFrag(curSeq)
    fragType = []
    fragMZ = []

    for i, item in enumerate(ans):
        fragType.append(ans[i][0])
        fragMZ.append(ans[i][4])
        print item

    fragMZ = N.array(fragMZ)
    fragMZ.sort()
    fragType = N.array(fragType)
    fragYVals = N.zeros_like(fragMZ)
    fragYVals+=1#scale to 100

    absTol = 2000#ppm
    ppmErrs = []
    for i,frag in enumerate(fragMZ):
        foundInd = mz.searchsorted(frag)

        if foundInd == 0:
            prevInd = 0
        else:
            prevInd = foundInd-1

        if foundInd >= len(mz):
            foundInd+=-1
            prevInd+=-1


#        print len(mz), foundInd, prevInd
        foundMZ = mz[foundInd]
        prevMZ = mz[prevInd]
        foundDiff = N.abs(foundMZ-frag)
        prevDiff = N.abs(prevMZ-frag)
        foundDiffOk = foundDiff < (foundMZ*absTol*1E-6)
        prevDiffOk = prevDiff < (prevMZ*absTol*1E-6)

        if foundDiffOk and prevDiffOk:
            if foundDiff < prevDiff:
                ppmErrs.append([frag, foundDiff/frag*1E6])
                fragYVals[i] = yVals[foundInd]
            else:
                ppmErrs.append([frag, prevDiff/frag*1E6])
                fragYVals[i] = yVals[prevInd]
        elif foundDiffOk:
            ppmErrs.append([frag, foundDiff/frag*1E6])
            fragYVals[i] = yVals[foundInd]
        elif prevDiffOk:
            ppmErrs.append([frag, prevDiff/frag*1E6])
            fragYVals[i] = yVals[prevInd]






    #print fragMZ

    fig = P.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.vlines(mz, 0, yVals, colors = 'k', alpha = 0.4)
    for frag in fragType:
        fragInd = N.where(fragType == frag)[0]
        tempFrag = fragMZ[fragInd]
        tempInt = fragYVals[fragInd]
        ax1.vlines(tempFrag, 0, tempInt, colors = COLORS[frag], linestyles = 'solid', alpha = 0.8)#
    ax1.legend()#legend is broken in mpl
    i = 0
    for err in ppmErrs:
        ax2.plot([err[1]], [i], 'go')
        i+=1
        print err
    P.legend()
    print series
    P.show()
#    import sys
#    app = QtGui.QApplication(sys.argv)
#    w = MPL_Widget(enableAutoScale = False, doublePlot = True, enableEdit = True)
#    x = N.arange(0, 20, 0.1)
#    y = N.sin(x)*1E8
#    y2 = N.cos(x)
#    w.canvas.ax.plot(x, y)
##    w.canvas.ax.plot(x, y2)
#    w.show()
#    sys.exit(app.exec_())

if __name__ == "__main__":
    import numpy as N
    import pylab as P
    main()

