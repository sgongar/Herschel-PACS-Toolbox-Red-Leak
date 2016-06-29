# coding=utf-8
# 
#  This file is part of Herschel Common Science System (HCSS).
#  Copyright 2001-2012 Herschel Science Ground Segment Consortium
# 
#  HCSS is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation, either version 3 of
#  the License, or (at your option) any later version.
# 
#  HCSS is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
# 
#  You should have received a copy of the GNU Lesser General
#  Public License along with HCSS.
#  If not, see <http://www.gnu.org/licenses/>.
# 

from herschel.pacs.signal import SlicedFrames
from herschel.pacs.signal.context import *
from herschel.pacs.spg.common import *
from herschel.pacs.spg.common import SlicingRule
from herschel.pacs.spg.spec import *
from herschel.pacs.spg.spec import SpecFlatFieldLineTask
from herschel.pacs.cal import *
from herschel.pacs.cal import GetPacsCalDataTask
from herschel.ia.numeric import *
from herschel.ia.jconsole import *
from herschel.pacs.spg.pipeline import *
from herschel.pacs.spg.pipeline.ProductSinkHandling import *
from herschel.pacs.spg.pipeline.spg_spec_tools import *

# Checks for a particular type of anomaly (H_SC-70 DECMEC) and adds a quality 
# flag if found.
# (This refers to a loss of data, and if this quality flag became set while the 
# SPG was running on your data, then your data would have gone through an extra 
# quality control.) 
# If the anomaly is present, then a Meta Data entry "qflag_DMANOG4L_p" will be 
# added to obs, and a flag is added to the "quality" of obs.
observations_dict["obs_{0}".format(obsids.keys()[i])] = checkForAnomaly70(observations_dict["obs_{0}".format(obsids.keys()[i])])

# filter meta keywords and update descriptions
modifyMetaData(observations_dict["obs_{0}".format(obsids.keys()[i])])

# add extra meta data 
pacsEnhanceMetaData(observations_dict["obs_{0}".format(obsids.keys()[i])])
   
# copy the metadata from the ObservationContext to the level0 product
pacsPropagateMetaKeywords(observations_dict["obs_{0}".format(obsids.keys()[i])], '0', observations_dict["obs_{0}".format(obsids.keys()[i])].level0)

# Extract the level0 from the ObservationContext 
level0 = PacsContext(observations_dict["obs_{0}".format(obsids.keys()[i])].level0)
level0 = level0.updateContextType()
observations_dict["obs_{0}".format(obsids.keys()[i])].level0 = level0

# Extract the pointing product
pp = observations_dict["obs_{0}".format(obsids.keys()[i])].auxiliary.pointing

# Extract the orbit ephemeris information
orbitEphem = observations_dict["obs_{0}".format(obsids.keys()[i])].auxiliary.orbitEphemeris

# Extract Time Correlation which is used to convert in addUtc
timeCorr = observations_dict["obs_{0}".format(obsids.keys()[i])].auxiliary.timeCorrelation

#-------------------------------------------------------------------------------
# SETUP 2:
# Set up the calibration tree. 
# First check whether calTree already exists, since it could have been filled 
# by the SPG pipeline 
# If not, then take it from your current HIPE build, and then put it into the 
# ObservationContext so that it is stored there for future reference
calTree = getCalTree(obs = observations_dict["obs_{0}".format(obsids.keys()[i])])
observations_dict["obs_{0}".format(obsids.keys()[i])].calibration = calTree

rsrfR1_v5 = getCalProduct("Spectrometer", "RsrfR1", 5)
print rsrfR1_v5.calFileVersion

# Extract the Horizons product
try :
    hp = observations_dict["obs_{0}".format(obsids.keys()[i])].auxiliary.refs["HorizonsProduct"].product
except :
    print "WARNING : No Horizons found !"
    hp = None

# For your camera, extract the Frames (scientific data), the rawramps (raw data 
# for one pixel), and the DMC header (the mechanisms' status information, 
# sampled at a high frequency) 
slicedFrames = SlicedFrames(level0.fitted.getCamera(camera).product)
slicedRawRamp = level0.raw.getCamera(camera).product
slicedDmcHead = level0.dmc.getCamera(camera).product    

# ******************************************************************************
#         Processing
# ******************************************************************************
# 
# Flag the saturated data in a mask "SATURATION" (and "RAWSATURATION": this 
# exploits the raw ramps downlinked for a single pixel of the data array)
# used cal files: RampSatLimits and SignalSatLimits
# copy=1 makes slicedFrames a fully independent product
slicedFrames = specFlagSaturationFrames(slicedFrames, rawRamp = slicedRawRamp,\
                                        calTree = calTree, copy = 1)

# Convert digital units to Volts, used cal file: Readouts2Volts
slicedFrames = specConvDigit2VoltsPerSecFrames(slicedFrames, calTree = calTree)

# Identifies the calibration blocks and fills the CALSOURCE status entry
slicedFrames = detectCalibrationBlock(slicedFrames)

# This tasks adds the time information in UTC to the status
slicedFrames = addUtc(slicedFrames, timeCorr)

# Add the pointing information of the central spaxel to the Status
#   Uses the pointing, horizons product (solar system object ephemeries), 
#   orbitEphemeris products, and the SIAM cal file.
slicedFrames = specAddInstantPointing(slicedFrames, pp, calTree = calTree,\
                                      orbitEphem = orbitEphem,\
                                      horizonsProduct = hp)    
#copy the saa meta keyword to the ObservationContext meta HCSS-SCR 19230
observations_dict["obs_{0}".format(obsids.keys()[i])].meta["solarAspectAngleMean"] = slicedFrames.meta["solarAspectAngleMean"].copy()
observations_dict["obs_{0}".format(obsids.keys()[i])].meta["solarAspectAngleRms"] = slicedFrames.meta["solarAspectAngleRms"].copy()

# This task extends the Status of Frames with the parameters GRATSCAN, CHOPPER,
# CHOPPOS used cal file: ChopperThrowDescription
slicedFrames = specExtendStatus(slicedFrames, calTree = calTree)

# This task converts the chopper readouts to an angle wrt. focal plane unit and
# the sky and adds this to the status, used cal file: ChopperAngle and 
# ChopperSkyAngle
slicedFrames = convertChopper2Angle(slicedFrames, calTree = calTree)

# This task adds the positions for each pixel (Ra and Dec dataset) 
# used cal files: ArrayInstrument and ModuleArray
slicedFrames = specAssignRaDec(slicedFrames, calTree = calTree)

# This task adds the wavelength for each pixel (Wave dataset), used cal 
# file: WavePolynomes
slicedFrames = waveCalc(slicedFrames, calTree = calTree)

# This task corrects the wavelength for the s/c velocity, uses the pointing,
# orbitEphemeris and TimeCorrelation product
slicedFrames = specCorrectHerschelVelocity(slicedFrames, orbitEphem, pp,\
                                           timeCorr, horizonsProduct = hp)

# Find the major blocks of this observation and organise it in the block table 
# attached to the Frames used cal file: ObcpDescription
slicedFrames = findBlocks(slicedFrames, calTree = calTree)

# This task flags the known bad or noisy pixels in the mask "BADPIXELS" and 
# "NOISYPIXELS" used cal files: BadPixelMask and NoisyPixelMask
slicedFrames = specFlagBadPixelsFrames(slicedFrames, calTree = calTree)

# Slice the data by Line/Range, Raster Point, nod position, nod cycle, on/off 
# position and per band. 
# The parameters removeUndefined and removeMasked are for cleaning purposes
slicedFrames, additionalOutContexts = pacsSliceContext(slicedFrames,\
                                                       [slicedDmcHead],\
                                                       removeUndefined = True,\
                                                       removeMasked = True,\
                                                       spgMode = True)
slicedDmcHead = additionalOutContexts[0]

# This task flags the data effected by the chopper movement in the mask 
# "UNCLEANCHOP" it uses the high resolution Dec/Mec header and the cal files 
# ChopperAngle and ChopperJitterThreshold 
slicedFrames = flagChopMoveFrames(slicedFrames, dmcHead = slicedDmcHead,\
                                  calTree = calTree)

# This task flags the data affected by the grating movement in the mask 
# "GRATMOVE" it uses the high resolution Dec/Mec header and the cal file
# GratingJitterThreshold 
slicedFrames = flagGratMoveFrames(slicedFrames, dmcHead = slicedDmcHead,\
                                  calTree = calTree)

# Update of the observation context
observations_dict["obs_{0}".format(obsids.keys()[i])] = updatePacsObservation(observations_dict["obs_{0}".format(obsids.keys()[i])], 0.5, [slicedFrames, slicedDmcHead])

# remove some variables (clean-up of memory)
# del pp, orbitEphem, slicedDmcHead, slicedFrames, slicedRawRamp 
# del timeCorr, hp, level0, additionalOutContexts


"""
VERSION     
  $Id: L1_ChopNod.py,v 1.40 2015/10/15 18:39:45 jdejong Exp $      <do not touch. This field is changed by CVS>

PURPOSE
   PACS Spectrometer Pipeline of chop/nod AORs starting at level 0.5

   This is the second level of the pipeline scripts of the SPG - the Standard Product Generation, 
   a.k.a. the automatic pipeline that the HSC runs - and that which your HSA-gotten ObservationContext  
   were reduced with, if they were reduced in this same track. 

   The SPG scripts are similar to the interactive pipeline (ipipe) scripts that PACS provides in HIPE,  
   but there are extra tasks that the ipipe scripts include, and so users should consider re-reducing
   their data with the ipipe scripts.
   This SPG script is provided so you can see what your HSA-gotten Observation Context levels 
   were reduced with. We provide some comments explaining what the individual tasks do, but for detailed 
   comments see the ipipe scripts, and for a detailed explanation of the pipeline, see the PACS Data 
   Reduction Guide.

   The ipipe scripts can be found under the HIPE menu Pipelines->Spectrometer->. From there you go 
   to the pipeline suited for your observation, such as Chopped line scan and short range scan->lineScan. 


AUTHOR
   Juergen Schreiber <schreiber@mpia.de>

WARNING: 
   Do not edit this file! This is the reference copy for your current 
   installation of HIPE. We recommend you first copy it to a different  
   location before editing.



INPUTS
   - obs : ObservationContext
       - Products needed to run the pipeline are extracted from it
       - Must already be loaded in HIPE, and should contain the previously-reduced Level 0.5
   - camera : camera to reduce (only one done at a time)
       - "red" or "blue"
   - calTree : Calibration Tree from the observation, or generated within your HIPE session 

HISTORY
  2009-03-13 JS 1.0 initial version 
  2009-06-24 JS 1.1 updated
  2009-07-16 JS 1.2 introduce slicing   
  2013-04-04 KME improve comments
"""

# Extract the (previously-reduced and saved) level 0_5 out of the ObservationContext
level0_5 = PacsContext(observations_dict["obs_{0}".format(obsids.keys()[i])].level0_5)

# extract the frames for your camera
slicedFrames = level0_5.fitted.getCamera(camera).product

# Check that the science frames are not masked out
checkScienceAvailable(slicedFrames)

#*******************************************************************************
#         Processing
#*******************************************************************************

# Detect and flag glitches ("GLITCH" mask)
# copy=True makes slicedFrames a fully independent product
# Activate all masks, for all slices, before deglitching
slicedFrames = activateMasks(slicedFrames, String1d([" "]), exclusive = True,\
                             copy = True)
slicedFrames = specFlagGlitchFramesQTest(slicedFrames)

# add quality information to meta data (such as glitch and saturation rate)
slicedFrames = activateMasks(slicedFrames, slicedFrames.get(0).getMaskTypes())
slicedFrames = addQualityInformation(slicedFrames)

# converts the signal level to the smallest capacitance
# used cal file: capacitanceRatios
slicedFrames = convertSignal2StandardCap(slicedFrames, calTree=calTree)


"""
# calculate the differential signal of each on-off pair for each chopper cycle
slicedFrames = specDiffChop(slicedFrames, scical = "sci", keepall = False,\
                            normalize = True)
"""

# Derive detectors' response from calibration block
# used cal files: observedResponse, calSourceFlux
calBlock = selectSlices(slicedFrames, scical = "cal").get(0)
csResponseAndDark = specDiffCs(calBlock, calTree = calTree)

# subtract the dark, using the nominal dark current in the calibration tree 
# calFile used: spectrometer.darkCurrent
slicedFrames = specSubtractDark(slicedFrames, calTree = calTree)

# Before applying the RSRF, get the signal gaps between consecutive slices
# in time order for the transient correction that will be made after the
# RSRF and respsonse calibrations have been applied..
gaps = specSignalGap(slicedFrames)

# Divide by the relative spectral response function 
# Used cal files: rsrfR1, rsrfB2A, rsrfB2B or rsrfB3A
slicedFrames = rsrfCal(slicedFrames, calTree = calTree)

# Divide by the response
# Use intermediate product from specDiffCs : csResponseAndDark
slicedFrames = specRespCal(slicedFrames, csResponseAndDark = csResponseAndDark,\
                           calTree = calTree)

# convert the Frames to a PacsCube
slicedCubes = specFrames2PacsCube(slicedFrames)        

# compute ra/dec meta keywords
slicedCubes = centerRaDecMetaData(slicedCubes)

# Update of the observation context
observations_dict["obs_{0}".format(obsids.keys()[i])] = updatePacsObservation(observations_dict["obs_{0}".format(obsids.keys()[i])], 1.0, [slicedFrames, slicedCubes])

# Remove some variables (memory clean-up)
# del slicedFrames, slicedCubes, level0_5


"""
VERSION     
  $Id: L2_ChopNod.py,v 1.79 2016/06/17 14:06:15 jdejong Exp $      <do not touch. This field is changed by CVS>

PURPOSE
   PACS Spectrometer Pipeline of chop/nod AORs starting at level 1

   This is the third level of the pipeline scripts of the SPG - the Standard Product Generation, 
   a.k.a. the automatic pipeline that the HSC runs - and that which your HSA-gotten ObservationContext  
   were reduced with, if they were reduced in this same track. 

   The SPG scripts are similar to the interactive pipeline (ipipe) scripts that PACS provides in HIPE,  
   but there are extra tasks that the ipipe scripts include, and so users should consider re-reducing
   their data with the ipipe scripts.
   This SPG script is provided so you can see what your HSA-gotten Observation Context levels 
   were reduced with. We provide some comments explaining what the individual tasks do, but for detailed 
   comments see the ipipe scripts, and for a detailed explanation of the pipeline, see the PACS Data 
   Reduction Guide.

   The ipipe scripts can be found under the HIPE menu Pipelines->Spectrometer->. From there you go 
   to the pipeline suited for your observation, such as Chopped line scan and short range scan->lineScan. 

HISTORY 
  2009-03-13 JS 1.0 initial version 
  2009-06-24 JS 1.1 updated
  2009-07-16 JS 1.2 introduce slicing  
  2013-04-04 KME improve comments 
"""

#*******************************************************************************
# Preparation
#*******************************************************************************
    
# Always use the product sink for this script
sink.setUsed(True)

# Extract the (previously-reduced and saved) level 1 out of the ObservationContext
level1 = PacsContext(observations_dict["obs_{0}".format(obsids.keys()[i])].level1)

# SETUP 2:

# extract level1 frames  and cubes for your camera   
slicedCubes = level1.cube.getCamera(camera).product
slicedFrames = level1.fitted.getCamera(camera).product

# Computes the telescope background flux and scales the normalized signal with 
# the telescope background flux using asymmetric chopping
slicedFramesCal, background = specRespCalToTelescope(slicedFrames,\
                                                     observations_dict["obs_{0}".format(obsids.keys()[i])].auxiliary.hk,\
                                                     calTree = calTree,\
                                                     reduceNoise = 1, copy = 1)
# convert the Frames to a PacsCube
slicedCubesCal = specFrames2PacsCube(slicedFramesCal)     
# compute ra/dec meta keywords
slicedCubesCal = centerRaDecMetaData(slicedCubesCal)
#
# ******************************************************************************
#         Processing
# ******************************************************************************   

# copyCube = True makes slicedCubes a fully independent product
copyCube = True

# Flatfielding for line spectroscopy and short range scans (up to 5 micron) only
# (See the ipipe scripts and the PDRG for an explanation of the 
# flatfielding tasks.)

# For SED and large range spectroscopy, note that flatfielding is done in the 
# ipipe scripts. (For line spectroscopy, you should anyway redo the flatfielding
# so you can check the results)

lineSpec = isLineSpec(slicedCubes)
shortRange = isShortRange(observations_dict["obs_{0}".format(obsids.keys()[i])])
maskNotFF = False

# lineSpec of shortRange

# if lineSpec or shortRange:
    
ffUpsample = getUpsample(observations_dict["obs_{0}".format(obsids.keys()[i])])
        
# 1. Flag outliers and rebin
waveGrid = wavelengthGrid(slicedCubes, oversample = 2,\
                          upsample = ffUpsample, calTree = calTree)
slicedCubes = activateMasks(slicedCubes,\
                            String1d(["GLITCH", "UNCLEANCHOP",\
                                      "NOISYPIXELS", "RAWSATURATION",\
                                      "SATURATION", "GRATMOVE", "BADPIXELS",\
                                      "INVALID"]), exclusive = True,\
                                                   copy = copyCube)
slicedCubesCal = activateMasks(slicedCubesCal,\
                               String1d(["GLITCH", "UNCLEANCHOP",\
                                         "NOISYPIXELS", "RAWSATURATION",\
                                         "SATURATION", "GRATMOVE", "BADPIXELS",\
                                         "INVALID"]), exclusive = True,\
                                                      copy = copyCube)
copyCube = False
slicedCubes = specFlagOutliers(slicedCubes, waveGrid, nSigma = 5, nIter = 1)
slicedCubesCal = specFlagOutliers(slicedCubesCal, waveGrid, nSigma = 5,\
                                      nIter = 1)
slicedCubes = activateMasks(slicedCubes,\
                            String1d(["GLITCH", "UNCLEANCHOP",\
                                      "NOISYPIXELS", "RAWSATURATION",\
                                      "SATURATION", "GRATMOVE",\
                                      "OUTLIERS", "BADPIXELS",\
                                      "INVALID"]), exclusive = True)
slicedRebinnedCubes = specWaveRebin(slicedCubes, waveGrid)
slicedCubes = selectSlices(slicedCubes,\
                           refContext = slicedRebinnedCubes)
slicedCubesCal = selectSlices(slicedCubesCal,\
                              refContext = slicedRebinnedCubes)

width = 2.5
if isRangeSpec(observations_dict["obs_{0}".format(obsids.keys()[i])]):
    width = 1.5
        
# 2. mask the line !!!!!!!!!!!!!!!!!!!
slicedCubes = maskLines(slicedCubes, slicedRebinnedCubes,\
                        calTree = calTree, widthDetect = width,\
                        widthMask = width, threshold = 10.0,\
                        maskType = "INLINE")
slicedCubesCal = maskLines(slicedCubesCal, slicedRebinnedCubes,\
                           calTree = calTree, widthDetect = width,\
                           widthMask = width, threshold = 10.0,\
                           maskType = "INLINE")
# 3. do the flatfielding
print "antes de specFlatFieldLine"
slicedCubes = specFlatFieldLine(slicedCubes, calTree = calTree,\
                                scaling = 1, maxrange = [55.,190.],\
                                slopeInContinuum = 1, maxScaling = 2.,\
                                maskType = "OUTLIERS_FF", offset = 0)
print "en mitad de specFlatFieldLine"
slicedCubesCal = specFlatFieldLine(slicedCubesCal, calTree = calTree,\
                                   scaling = 1, maxrange = [55.,190.],\
                                   slopeInContinuum = 1, maxScaling = 2.,\
                                   maskType = "OUTLIERS_FF", offset = 0)
print "despues de specFlatFieldLine"
# 4. Rename mask OUTLIERS to OUTLIERS_B4FF (specFlagOutliers would refuse 
# to overwrite OUTLIERS) & deactivate mask INLINE
slicedCubes.renameMask("OUTLIERS", "OUTLIERS_B4FF")
slicedCubes = deactivateMasks(slicedCubes,\
                              String1d(["INLINE", "OUTLIERS_B4FF"]))
slicedCubesCal.renameMask("OUTLIERS", "OUTLIERS_B4FF")
slicedCubesCal = deactivateMasks(slicedCubesCal,\
                                 String1d(["INLINE", "OUTLIERS_B4FF"]))
# del ffUpsample, width

# Range spec option
"""
elif isRangeSpec(observations_dict["obs_{0}".format(obsids.keys()[i])]):
    slicedFrames = specFlatFieldRange(slicedFrames, useSplinesModel = True,\
                                      excludeLeaks = True, calTree = calTree,\
                                      copy = copyCube)
    slicedFramesCal = specFlatFieldRange(slicedFramesCal,\
                                         useSplinesModel = True,\
                                         excludeLeaks = True,\
                                         calTree = calTree, copy = copyCube)
    copyCube = False
    maskNotFF = True
    slicedCubes = specFrames2PacsCube(slicedFrames)
    slicedCubesCal = specFrames2PacsCube(slicedFramesCal)
    slicedCubes = centerRaDecMetaData(slicedCubes)
    slicedCubesCal = centerRaDecMetaData(slicedCubesCal)
"""
    
# Building the wavelength grids for each slice
# Used cal file: wavelengthGrid

print "antes de wavelengthgrid"

upsample = getUpsample(observations_dict["obs_{0}".format(obsids.keys()[i])])
waveGrid = wavelengthGrid(slicedCubes, oversample = 2, upsample = upsample,\
                          calTree = calTree)

print "despues de wavelengthgrid"

# Active masks 
slicedCubes = activateMasks(slicedCubes,\
                            String1d(["GLITCH", "UNCLEANCHOP", "SATURATION",\
                                      "GRATMOVE", "BADFITPIX",\
                                      "BADPIXELS"]), exclusive = True,\
                                                     copy = copyCube)
slicedCubesCal = activateMasks(slicedCubesCal,\
                               String1d(["GLITCH", "UNCLEANCHOP", "SATURATION",\
                                         "GRATMOVE", "BADFITPIX",\
                                         "BADPIXELS"]), exclusive = True,\
                                                        copy = copyCube)

# Flag the remaining outliers (sigma-clipping in wavelength domain), 
# with default parameters here
slicedCubes = specFlagOutliers(slicedCubes, waveGrid)
slicedCubesCal = specFlagOutliers(slicedCubesCal, waveGrid)

# Rebin all cubes on consistent wavelength grids
masksForRebinning = String1d(["OUTOFBAND", "GLITCH", "UNCLEANCHOP",\
                             "SATURATION", "GRATMOVE", "BADFITPIX",\
                              "OUTLIERS", "BADPIXELS"])

masksForRebinning.append("NOTFFED")
slicedCubes = activateMasks(slicedCubes, masksForRebinning, exclusive = True)
slicedRebinnedCubes = specWaveRebin(slicedCubes, waveGrid)

print "El tamanio de slicedRebinnedCubes es: ", slicedRebinnedCubes.refs.size()


# Only continue if there is at least one slice leftover after red-leak filtering
if slicedRebinnedCubes.refs.size() > 0:

    # Select only the slices in the PACS cube which are also in the rebinned cube
    slicedCubes = selectSlices(slicedCubes,\
                               refContext = slicedRebinnedCubes)
    slicedCubesCal = selectSlices(slicedCubesCal,\
                                  refContext = slicedRebinnedCubes)

    # Combine the nod-A & nod-B rebinned cubes.
    # All cubes at the same raster position are averaged.
    # This is the final science-grade product for spatially undersampled 
    # rasters and single pointings
    slicedRebinnedCubes = specAddNodCubes(slicedRebinnedCubes)  

    # Computes the telescope background flux and scales the normalized signal 
    # with the telescope background flux
    slicedRebinnedCubes, background = specRespCalToTelescope(slicedRebinnedCubes,\
                                                             observations_dict["obs_{0}".format(obsids.keys()[i])].auxiliary.hk,\
                                                             calTree = calTree)
    
    # compute ra/dec meta keywords
    slicedRebinnedCubes = centerRaDecMetaData(slicedRebinnedCubes)
    
    # convert the cubes to a table 
    slicedTable = pacsSpecCubeToTable(slicedRebinnedCubes)
      
    # Compute equidistant wavelength grid for equidistant regridding
    equidistantWaveGrid = wavelengthGrid(slicedCubes, oversample = 2,\
                                         upsample = upsample, calTree = calTree,\
                                         regularGrid = True,\
                                         fracMinBinSize = 0.35)
    
    # determine mapping algorithm and parameters
    driz, pixelSize, interpolatePixelSize, oversampleSpace, upsampleSpace, pixFrac, source, mapType = determineMappingAlgorithm(slicedRebinnedCubes, camera)
    
    # Mosaic, per wavelength range, all raster pointings into a single cube
    slicedDrizzledCubes = None
    slicedDrizzledEquidistantCubes = None
    slicedInterpolatedCubes = None
    slicedInterpolatedEquidistantCubes = None
    slicedProjectedEquidistantCubes = None

    """
    if driz:
        oversampleWave = 2
        upsampleWave = upsample
        waveGridForDrizzle = wavelengthGrid(slicedCubes,\
                                            oversample = oversampleWave,\
                                            upsample = upsampleWave,\
                                            calTree = calTree)
        equidistantWaveGridForDrizzle = wavelengthGrid(slicedCubes,\
                                                       oversample = oversampleWave,\
                                                       upsample = upsampleWave,\
                                                       calTree = calTree,\
                                                       regularGrid = True,\
                                                       fracMinBinSize = 0.35)
        spaceGrid = spatialGrid(slicedCubes,\
                                wavelengthGrid = waveGridForDrizzle,\
                                oversample = oversampleSpace,\
                                upsample = upsampleSpace, pixfrac = pixFrac,\
                                calTree = calTree)
        slicedDrizzledCubes = drizzle(slicedCubesCal,\
                                      wavelengthGrid = waveGridForDrizzle,\
                                      spatialGrid = spaceGrid)[0]
        slicedDrizzledCubes = centerRaDecMetaData(slicedDrizzledCubes)
        sink.saveWhenMemoryShort(slicedDrizzledCubes)
        slicedDrizzledEquidistantCubes = specRegridWavelength(slicedDrizzledCubes,\
                                                              equidistantWaveGridForDrizzle)
        sink.saveWhenMemoryShort(slicedDrizzledEquidistantCubes)
        slicedProjectedCubes = specProject(slicedRebinnedCubes,\
                                           cubeWithOutputGrid = slicedDrizzledCubes)
        # del spaceGrid, waveGridForDrizzle, equidistantWaveGridForDrizzle, oversampleWave, upsampleWave
    else:
        slicedProjectedCubes = specProject(slicedRebinnedCubes,\
                                           outputPixelsize = pixelSize)
        if mapType != "oversampled":
            slicedInterpolatedCubes = specInterpolate(slicedRebinnedCubes,\
                                                      outputPixelsize = interpolatePixelSize)
            slicedInterpolatedCubes = centerRaDecMetaData(slicedInterpolatedCubes)
        
        if (mapType=="nyquist" or mapType=="oversampled"):
            slicedProjectedEquidistantCubes = specRegridWavelength(slicedProjectedCubes,\
                                                                   equidistantWaveGrid)
        else:
            slicedInterpolatedEquidistantCubes = specRegridWavelength(slicedInterpolatedCubes,\
                                                                      equidistantWaveGrid)
    
    slicedProjectedCubes = centerRaDecMetaData(slicedProjectedCubes)
    sink.saveWhenMemoryShort(slicedProjectedCubes)
    
    # do a pointsource extraction for the pointed observations only
    spectra1d = None
    if source=='point':
        if isRangeSpec(observations_dict["obs_{0}".format(obsids.keys()[i])]):
            c1, c9, c129 = extractCentralSpectrum(slicedRebinnedCubes,\
                                                  smoothing = 'filter',\
                                                  width = 50,\
                                                  preFilterWidth = 15,\
                                                  calTree = calTree)
        else:
            c1, c9, c129 = extractCentralSpectrum(slicedRebinnedCubes,\
                                                  smoothing = 'median',\
                                                  calTree = calTree)
        spectra1d = fillPacsCentralSpectra(slicedRebinnedCubes, c1, c129, c9)
        del c1, c9, c129
        
    # update the level 2 of the ObservationContext 
    observations_dict["obs_{0}".format(obsids.keys()[i])] = updatePacsObservation(observations_dict["obs_{0}".format(obsids.keys()[i])],\
                                                                                  2.0,\
                                                                                  [slicedCubesCal, slicedRebinnedCubes, slicedProjectedCubes,\
                                                                                   slicedDrizzledCubes, slicedTable, slicedInterpolatedCubes,\
                                                                                   spectra1d, slicedDrizzledEquidistantCubes,\
                                                                                   slicedInterpolatedEquidistantCubes,\
                                                                                   slicedProjectedEquidistantCubes])
    
    # remove variables to cleanup memory
    del slicedTable, equidistantWaveGrid, driz, pixelSize, interpolatePixelSize
    del oversampleSpace, upsampleSpace, pixFrac, source, mapType
    del slicedDrizzledCubes, slicedDrizzledEquidistantCubes
    del slicedInterpolatedCubes, slicedInterpolatedEquidistantCubes
    del slicedProjectedCubes, slicedProjectedEquidistantCubes, spectra1d
else:
    LOGGER.warning("No slices left anymore after filtering red-leak and out-of-band slices.")

# Delete some variables (memory clean-up)
# del slicedCubes, slicedFrames, slicedFramesCal, background, slicedCubesCal
# del copyCube, lineSpec, shortRange, maskNotFF, upsample, waveGrid
# del masksForRebinning, slicedRebinnedCubes

# restore default sink state
restoreOldSinkState()

del calTree
"""