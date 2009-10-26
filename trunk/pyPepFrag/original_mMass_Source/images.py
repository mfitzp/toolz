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
import wx
from wx.tools import img2py


# IMAGES
# ------

lib = {}

def loadImages():
    """Load images from lib."""
    
    # load image library
    if wx.Platform == '__WXMAC__':
        import images_lib_mac as images_lib
    elif wx.Platform == '__WXMSW__':
        import images_lib_msw as images_lib
    else:
        import images_lib_gtk as images_lib
    
    # common
    lib['icon16'] = images_lib.getIcon16Icon()
    lib['icon32'] = images_lib.getIcon32Icon()
    lib['icon48'] = images_lib.getIcon48Icon()
    lib['icon128'] = images_lib.getIcon128Icon()
    lib['icon256'] = images_lib.getIcon256Icon()
    lib['icon512'] = images_lib.getIcon512Icon()
    
    lib['iconAbout'] = images_lib.getIconAboutBitmap()
    lib['iconError'] = images_lib.getIconErrorBitmap()
    
    # backgrounds
    lib['bgrToolbar'] = images_lib.getBgrToolbarBitmap()
    lib['bgrToolbarNoBorder'] = images_lib.getBgrToolbarNoBorderBitmap()
    lib['bgrControlbar'] = images_lib.getBgrControlbarBitmap()
    lib['bgrBottombar'] = images_lib.getBgrBottombarBitmap()
    lib['bgrPeakEditor'] = images_lib.getBgrPeakEditorBitmap()
    
    # bullets
    bulletsOn = images_lib.getBulletsOnBitmap()
    bulletsOff = images_lib.getBulletsOffBitmap()
    lib['bulletDocuments'] = bulletsOn.GetSubBitmap(wx.Rect(0, 0, 13, 12))
    lib['bulletAnnotationsOn'] = bulletsOn.GetSubBitmap(wx.Rect(13, 0, 13, 12))
    lib['bulletAnnotationsOff'] = bulletsOff.GetSubBitmap(wx.Rect(13, 0, 13, 12))
    lib['bulletSequenceOn'] = bulletsOn.GetSubBitmap(wx.Rect(26, 0, 13, 12))
    lib['bulletSequenceOff'] = bulletsOff.GetSubBitmap(wx.Rect(26, 0, 13, 12))
    lib['bulletMatchOn'] = bulletsOn.GetSubBitmap(wx.Rect(39, 0, 13, 12))
    lib['bulletMatchOff'] = bulletsOff.GetSubBitmap(wx.Rect(39, 0, 13, 12))
    
    # tools
    if wx.Platform == '__WXMAC__':
        tools = images_lib.getToolsBitmap()
        lib['toolProcessing'] = tools.GetSubBitmap(wx.Rect(0, 0, 30, 22))
        lib['toolCalibration'] = tools.GetSubBitmap(wx.Rect(30, 0, 30, 22))
        lib['toolSequence'] = tools.GetSubBitmap(wx.Rect(60, 0, 30, 22))
        lib['toolMasscalc'] = tools.GetSubBitmap(wx.Rect(90, 0, 30, 22))
        lib['toolDifferences'] = tools.GetSubBitmap(wx.Rect(120, 0, 30, 22))
        lib['toolMascot'] = tools.GetSubBitmap(wx.Rect(150, 0, 30, 22))
        lib['toolInfo'] = tools.GetSubBitmap(wx.Rect(180, 0, 30, 22))
        lib['toolReport'] = tools.GetSubBitmap(wx.Rect(210, 0, 30, 22))
        lib['toolExport'] = tools.GetSubBitmap(wx.Rect(240, 0, 30, 22))
        lib['toolMethods'] = tools.GetSubBitmap(wx.Rect(270, 0, 30, 22))
    else:
        tools = images_lib.getToolsBitmap()
        lib['toolOpen'] = tools.GetSubBitmap(wx.Rect(0, 0, 22, 22))
        lib['toolSave'] = tools.GetSubBitmap(wx.Rect(22, 0, 22, 22))
        lib['toolPrint'] = tools.GetSubBitmap(wx.Rect(44, 0, 22, 22))
        lib['toolCrop'] = tools.GetSubBitmap(wx.Rect(0, 22, 22, 22))
        lib['toolSmoothing'] = tools.GetSubBitmap(wx.Rect(22, 22, 22, 22))
        lib['toolBaseline'] = tools.GetSubBitmap(wx.Rect(44, 22, 22, 22))
        lib['toolPeakpicking'] = tools.GetSubBitmap(wx.Rect(66, 22, 22, 22))
        lib['toolDeisotoping'] = tools.GetSubBitmap(wx.Rect(88, 22, 22, 22))
        lib['toolCalibration'] = tools.GetSubBitmap(wx.Rect(110, 22, 22, 22))
        lib['toolSequence'] = tools.GetSubBitmap(wx.Rect(0, 44, 22, 22))
        lib['toolDigest'] = tools.GetSubBitmap(wx.Rect(22, 44, 22, 22))
        lib['toolFragment'] = tools.GetSubBitmap(wx.Rect(44, 44, 22, 22))
        lib['toolSearch'] = tools.GetSubBitmap(wx.Rect(66, 44, 22, 22))
        lib['toolMasscalc'] = tools.GetSubBitmap(wx.Rect(0, 66, 22, 22))
        lib['toolDifferences'] = tools.GetSubBitmap(wx.Rect(22, 66, 22, 22))
        lib['toolMascot'] = tools.GetSubBitmap(wx.Rect(44, 66, 22, 22))
        lib['toolMethods'] = tools.GetSubBitmap(wx.Rect(66, 66, 22, 22))
        lib['toolInfo'] = tools.GetSubBitmap(wx.Rect(0, 88, 22, 22))
        lib['toolReport'] = tools.GetSubBitmap(wx.Rect(22, 88, 22, 22))
        lib['toolExport'] = tools.GetSubBitmap(wx.Rect(44, 88, 22, 22))
    
    # bottombars
    bottombarsOn = images_lib.getBottombarsOnBitmap()
    bottombarsOff = images_lib.getBottombarsOffBitmap()
    
    lib['documentsAdd'] = bottombarsOff.GetSubBitmap(wx.Rect(0, 0, 29, 22))
    lib['documentsDelete'] = bottombarsOff.GetSubBitmap(wx.Rect(29, 0, 29, 22))
    
    lib['peaklistAdd'] = bottombarsOff.GetSubBitmap(wx.Rect(0, 22, 29, 22))
    lib['peaklistDelete'] = bottombarsOff.GetSubBitmap(wx.Rect(29, 22, 29, 22))
    lib['peaklistAnnotate'] = bottombarsOff.GetSubBitmap(wx.Rect(58, 22, 29, 22))
    lib['peaklistEditorOn'] = bottombarsOn.GetSubBitmap(wx.Rect(87, 22, 29, 22))
    lib['peaklistEditorOff'] = bottombarsOff.GetSubBitmap(wx.Rect(87, 22, 29, 22))
    
    lib['spectrumParams'] = bottombarsOff.GetSubBitmap(wx.Rect(0, 44, 29, 22))
    lib['spectrumLabelsOn'] = bottombarsOn.GetSubBitmap(wx.Rect(29, 44, 29, 22))
    lib['spectrumLabelsOff'] = bottombarsOff.GetSubBitmap(wx.Rect(29, 44, 29, 22))
    lib['spectrumTicksOn'] = bottombarsOn.GetSubBitmap(wx.Rect(58, 44, 29, 22))
    lib['spectrumTicksOff'] = bottombarsOff.GetSubBitmap(wx.Rect(58, 44, 29, 22))
    lib['spectrumLabelAngleOn'] = bottombarsOn.GetSubBitmap(wx.Rect(87, 44, 29, 22))
    lib['spectrumLabelAngleOff'] = bottombarsOff.GetSubBitmap(wx.Rect(87, 44, 29, 22))
    lib['spectrumPosBarOn'] = bottombarsOn.GetSubBitmap(wx.Rect(116, 44, 29, 22))
    lib['spectrumPosBarOff'] = bottombarsOff.GetSubBitmap(wx.Rect(116, 44, 29, 22))
    lib['spectrumGelOn'] = bottombarsOn.GetSubBitmap(wx.Rect(145, 44, 29, 22))
    lib['spectrumGelOff'] = bottombarsOff.GetSubBitmap(wx.Rect(145, 44, 29, 22))
    lib['spectrumTrackerOn'] = bottombarsOn.GetSubBitmap(wx.Rect(174, 44, 29, 22))
    lib['spectrumTrackerOff'] = bottombarsOff.GetSubBitmap(wx.Rect(174, 44, 29, 22))
    lib['spectrumAutoscaleOn'] = bottombarsOn.GetSubBitmap(wx.Rect(203, 44, 29, 22))
    lib['spectrumAutoscaleOff'] = bottombarsOff.GetSubBitmap(wx.Rect(203, 44, 29, 22))
    
    lib['spectrumMeasureOn'] = bottombarsOn.GetSubBitmap(wx.Rect(29, 66, 29, 22))
    lib['spectrumMeasureOff'] = bottombarsOff.GetSubBitmap(wx.Rect(29, 66, 29, 22))
    lib['spectrumLabelPeakOn'] = bottombarsOn.GetSubBitmap(wx.Rect(58, 66, 29, 22))
    lib['spectrumLabelPeakOff'] = bottombarsOff.GetSubBitmap(wx.Rect(58, 66, 29, 22))
    lib['spectrumLabelPointOn'] = bottombarsOn.GetSubBitmap(wx.Rect(87, 66, 29, 22))
    lib['spectrumLabelPointOff'] = bottombarsOff.GetSubBitmap(wx.Rect(87, 66, 29, 22))
    lib['spectrumDeleteLabelOn'] = bottombarsOn.GetSubBitmap(wx.Rect(116, 66, 29, 22))
    lib['spectrumDeleteLabelOff'] = bottombarsOff.GetSubBitmap(wx.Rect(116, 66, 29, 22))
    
    # toolbars
    toolbarsOn = images_lib.getToolbarsOnBitmap()
    toolbarsOff = images_lib.getToolbarsOffBitmap()
    
    lib['calibrationReferencesOn'] = toolbarsOn.GetSubBitmap(wx.Rect(0, 0, 29, 22))
    lib['calibrationReferencesOff'] = toolbarsOff.GetSubBitmap(wx.Rect(0, 0, 29, 22))
    lib['calibrationErrorsOn'] = toolbarsOn.GetSubBitmap(wx.Rect(29, 0, 29, 22))
    lib['calibrationErrorsOff'] = toolbarsOff.GetSubBitmap(wx.Rect(29, 0, 29, 22))
    
    lib['exportImageOn'] = toolbarsOn.GetSubBitmap(wx.Rect(0, 22, 29, 22))
    lib['exportImageOff'] = toolbarsOff.GetSubBitmap(wx.Rect(0, 22, 29, 22))
    lib['exportPeaklistOn'] = toolbarsOn.GetSubBitmap(wx.Rect(29, 22, 29, 22))
    lib['exportPeaklistOff'] = toolbarsOff.GetSubBitmap(wx.Rect(29, 22, 29, 22))
    lib['exportSpectrumOn'] = toolbarsOn.GetSubBitmap(wx.Rect(58, 22, 29, 22))
    lib['exportSpectrumOff'] = toolbarsOff.GetSubBitmap(wx.Rect(58, 22, 29, 22))
    
    lib['infoSummaryOn'] = toolbarsOn.GetSubBitmap(wx.Rect(0, 44, 29, 22))
    lib['infoSummaryOff'] = toolbarsOff.GetSubBitmap(wx.Rect(0, 44, 29, 22))
    lib['infoSpectrumOn'] = toolbarsOn.GetSubBitmap(wx.Rect(29, 44, 29, 22))
    lib['infoSpectrumOff'] = toolbarsOff.GetSubBitmap(wx.Rect(29, 44, 29, 22))
    lib['infoNotesOn'] = toolbarsOn.GetSubBitmap(wx.Rect(58, 44, 29, 22))
    lib['infoNotesOff'] = toolbarsOff.GetSubBitmap(wx.Rect(58, 44, 29, 22))
    
    lib['mascotPMFOn'] = toolbarsOn.GetSubBitmap(wx.Rect(0, 66, 29, 22))
    lib['mascotPMFOff'] = toolbarsOff.GetSubBitmap(wx.Rect(0, 66, 29, 22))
    lib['mascotSQOn'] = toolbarsOn.GetSubBitmap(wx.Rect(29, 66, 29, 22))
    lib['mascotSQOff'] = toolbarsOff.GetSubBitmap(wx.Rect(29, 66, 29, 22))
    lib['mascotMISOn'] = toolbarsOn.GetSubBitmap(wx.Rect(58, 66, 29, 22))
    lib['mascotMISOff'] = toolbarsOff.GetSubBitmap(wx.Rect(58, 66, 29, 22))
    lib['mascotQueryOn'] = toolbarsOn.GetSubBitmap(wx.Rect(87, 66, 29, 22))
    lib['mascotQueryOff'] = toolbarsOff.GetSubBitmap(wx.Rect(87, 66, 29, 22))
    
    lib['masscalcSummaryOn'] = toolbarsOn.GetSubBitmap(wx.Rect(0, 88, 29, 22))
    lib['masscalcSummaryOff'] = toolbarsOff.GetSubBitmap(wx.Rect(0, 88, 29, 22))
    lib['masscalcIonSeriesOn'] = toolbarsOn.GetSubBitmap(wx.Rect(29, 88, 29, 22))
    lib['masscalcIonSeriesOff'] = toolbarsOff.GetSubBitmap(wx.Rect(29, 88, 29, 22))
    lib['masscalcPatternOn'] = toolbarsOn.GetSubBitmap(wx.Rect(58, 88, 29, 22))
    lib['masscalcPatternOff'] = toolbarsOff.GetSubBitmap(wx.Rect(58, 88, 29, 22))
    
    lib['processingCropOn'] = toolbarsOn.GetSubBitmap(wx.Rect(0, 110, 29, 22))
    lib['processingCropOff'] = toolbarsOff.GetSubBitmap(wx.Rect(0, 110, 29, 22))
    lib['processingSmoothingOn'] = toolbarsOn.GetSubBitmap(wx.Rect(29, 110, 29, 22))
    lib['processingSmoothingOff'] = toolbarsOff.GetSubBitmap(wx.Rect(29, 110, 29, 22))
    lib['processingBaselineOn'] = toolbarsOn.GetSubBitmap(wx.Rect(58, 110, 29, 22))
    lib['processingBaselineOff'] = toolbarsOff.GetSubBitmap(wx.Rect(58, 110, 29, 22))
    lib['processingPeakpickingOn'] = toolbarsOn.GetSubBitmap(wx.Rect(87, 110, 29, 22))
    lib['processingPeakpickingOff'] = toolbarsOff.GetSubBitmap(wx.Rect(87, 110, 29, 22))
    lib['processingDeisotopingOn'] = toolbarsOn.GetSubBitmap(wx.Rect(116, 110, 29, 22))
    lib['processingDeisotopingOff'] = toolbarsOff.GetSubBitmap(wx.Rect(116, 110, 29, 22))
    
    lib['sequenceEditorOn'] = toolbarsOn.GetSubBitmap(wx.Rect(0, 132, 29, 22))
    lib['sequenceEditorOff'] = toolbarsOff.GetSubBitmap(wx.Rect(0, 132, 29, 22))
    lib['sequenceModificationsOn'] = toolbarsOn.GetSubBitmap(wx.Rect(29, 132, 29, 22))
    lib['sequenceModificationsOff'] = toolbarsOff.GetSubBitmap(wx.Rect(29, 132, 29, 22))
    lib['sequenceDigestOn'] = toolbarsOn.GetSubBitmap(wx.Rect(58, 132, 29, 22))
    lib['sequenceDigestOff'] = toolbarsOff.GetSubBitmap(wx.Rect(58, 132, 29, 22))
    lib['sequenceFragmentOn'] = toolbarsOn.GetSubBitmap(wx.Rect(87, 132, 29, 22))
    lib['sequenceFragmentOff'] = toolbarsOff.GetSubBitmap(wx.Rect(87, 132, 29, 22))
    lib['sequenceSearchOn'] = toolbarsOn.GetSubBitmap(wx.Rect(116, 132, 29, 22))
    lib['sequenceSearchOff'] = toolbarsOff.GetSubBitmap(wx.Rect(116, 132, 29, 22))
# ----


def convertImages():
    """Convert an image to PNG format and embed it in a Python file. """
    
    # get libs to import images
    try:
        from wx.lib.embeddedimage import PyEmbeddedImage
        imp = '#load libs\nfrom wx.lib.embeddedimage import PyEmbeddedImage\n\n\n'
    except:
        imp = '#load libs\nimport cStringIO\nfrom wx import ImageFromStream, BitmapFromImage\n\n\n'
    
    # convert images
    for platform in ('mac', 'msw', 'gtk'):
        
        # create file
        imageFile = file('images_lib_'+platform+'.py', 'w')
        imageFile.write(imp)
        imageFile.close()
        
        # make commands
        commands = [
            "-a -u -i -n Icon16 images/"+platform+"/icon_16.png images_lib_"+platform+".py",
            "-a -u -i -n Icon32 images/"+platform+"/icon_32.png images_lib_"+platform+".py",
            "-a -u -i -n Icon48 images/"+platform+"/icon_48.png images_lib_"+platform+".py",
            "-a -u -i -n Icon128 images/"+platform+"/icon_128.png images_lib_"+platform+".py",
            "-a -u -i -n Icon256 images/"+platform+"/icon_256.png images_lib_"+platform+".py",
            "-a -u -i -n Icon512 images/"+platform+"/icon_512.png images_lib_"+platform+".py",
            
            "-a -u -n IconAbout images/"+platform+"/icon_about.png images_lib_"+platform+".py",
            "-a -u -n IconError images/"+platform+"/icon_error.png images_lib_"+platform+".py",
            
            "-a -u -n BgrToolbar images/"+platform+"/bgr_toolbar.png images_lib_"+platform+".py",
            "-a -u -n BgrToolbarNoBorder images/"+platform+"/bgr_toolbar_noborder.png images_lib_"+platform+".py",
            "-a -u -n BgrControlbar images/"+platform+"/bgr_controlbar.png images_lib_"+platform+".py",
            "-a -u -n BgrBottombar images/"+platform+"/bgr_bottombar.png images_lib_"+platform+".py",
            "-a -u -n BgrPeakEditor images/"+platform+"/bgr_peakeditor.png images_lib_"+platform+".py",
            
            "-a -u -n BulletsOn images/"+platform+"/bullets_on.png images_lib_"+platform+".py",
            "-a -u -n BulletsOff images/"+platform+"/bullets_off.png images_lib_"+platform+".py",
            
            "-a -u -n Tools images/"+platform+"/tools.png images_lib_"+platform+".py",
            
            "-a -u -n BottombarsOn images/"+platform+"/bottombars_on.png images_lib_"+platform+".py",
            "-a -u -n BottombarsOff images/"+platform+"/bottombars_off.png images_lib_"+platform+".py",
            "-a -u -n ToolbarsOn images/"+platform+"/toolbars_on.png images_lib_"+platform+".py",
            "-a -u -n ToolbarsOff images/"+platform+"/toolbars_off.png images_lib_"+platform+".py",
        ]
        
        # convert images
        for command in commands:
            img2py.main(command.split())
# ----


if __name__ == "__main__":
    convertImages()