"""
Red-leak script test for non-solar system objects.
"""

"""
Necesito la parte donde se encarga de la calibracion.
Deberia extraer la parte que utiliza el metodo moderno y substituirlo por el
antiguo.
Deberia comprobar que todo va bien, es decir, que el sistema genera lo que tiene
que generar.
Que tiene que generar??
Tengo que analizar cosas que me valgan.
"""

import os
import sys

from datetime import datetime

from herschel.pacs.signal import SlicedFrames
from herschel.pacs.spg.common import *
from herschel.pacs.spg.spec import *
from herschel.pacs.cal import *
from herschel.ia.numeric import *
from herschel.ia.jconsole import *
from herschel.pacs.signal.context import *
from herschel.pacs.spg.pipeline.spg_spec_tools import *
from herschel.pacs.spg.pipeline import *
from herschel.pacs.signal.context import *
from herschel.pacs.cal import GetPacsCalDataTask
from herschel.pacs.spg.pipeline.ProductSinkHandling import *

time_1 = datetime.now()
print "Initial time: ", time_1

camera = 'red'

""" Not needed if only a observation is analysed
if ((not locals().has_key('multiObs')) or (not multiObs)):
    obsid = 1342250905
"""
obsid = 1342250905

# Get data from pool file will improve time response
useHsa = 1
obs = getObservation(obsid, verbose = True, useHsa = useHsa,\
                     poolLocation = None, poolName = None)


# Do we need this?
# Checks for a particular type of anomaly (H_SC-70 DECMEC) and adds a quality 
# flag if found. (This refers to a loss of data, and if this quality flag became
# set while the SPG was running on your data, then your data would have gone
# through an extra quality control.) 
# If the anomaly is present, then a Meta Data entry "qflag_DMANOG4L_p" will be 
#dded to obs, and a flag is added to the "quality" of obs.
# obs = checkForAnomaly70(obs)

# It is really needed?
# filter meta keywords and update descriptions
modifyMetaData(obs)

# add extra meta data 
pacsEnhanceMetaData(obs)

pacsPropagateMetaKeywords(obs,'0', obs.level0) 
level0 = PacsContext(obs.level0)
level0 = level0.updateContextType()
obs.level0 = level0

# Extract the pointing product
pp = obs.auxiliary.pointing
# Extract the orbit ephemeris information
orbitEphem = obs.auxiliary.orbitEphemeris
# Extract Time Correlation which is used to convert in addUtc
timeCorr = obs.auxiliary.timeCorrelation

# Calibration tree.
calTree = getCalTree(version = 76)
 
# Get calibration file for RSRF and set it.
rsrfR1_v5 = getCalProduct("Spectrometer", "RsrfR1", 5)

obs.calibration = calTree
calTree.spectrometer.rsrfR1 = rsrfR1_v5

# Extract the Horizons product 
try :
    hp = obs.auxiliary.refs["HorizonsProduct"].product
except :
    print "WARNING : No Horizons found !"
    hp = None

# For your camera, extract the Frames (scientific data), the rawramps (raw data 
# for one pixel), and the DMC header (the mechanisms' status information, 
# sampled at a high frequency) 
slicedFrames = SlicedFrames(level0.fitted.getCamera(camera).product)
slicedRawRamp = level0.raw.getCamera(camera).product
slicedDmcHead = level0.dmc.getCamera(camera).product    
 
# Flag the saturated data in a mask "SATURATION" (and "RAWSATURATION": this 
# exploits the raw ramps downlinked for a single pixel of the data array)
# used cal files: RampSatLimits and SignalSatLimits
# copy=1 makes slicedFrames a fully independent product
slicedFrames = specFlagSaturationFrames(slicedFrames, rawRamp = slicedRawRamp,\
                                        calTree = calTree, copy=1)

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

""" CalBlock doesn't need these lines
# copy the saa meta keyword to the ObservationContext meta HCSS-SCR 19230
obs.meta["solarAspectAngleMean"] = slicedFrames.meta["solarAspectAngleMean"].copy()
obs.meta["solarAspectAngleRms"] = slicedFrames.meta["solarAspectAngleRms"].copy()
"""

# This task extends the Status of Frames with the parameters GRATSCAN, CHOPPER, CHOPPOS
# used cal file: ChopperThrowDescription
slicedFrames = specExtendStatus(slicedFrames, calTree = calTree)

# This task converts the chopper readouts to an angle wrt. focal plane unit and the sky
# and adds this to the status, used cal file: ChopperAngle and ChopperSkyAngle
slicedFrames = convertChopper2Angle(slicedFrames, calTree = calTree)

# This task adds the positions for each pixel (Ra and Dec dataset) 
# used cal files: ArrayInstrument and ModuleArray
slicedFrames = specAssignRaDec(slicedFrames, calTree = calTree)

# This task adds the wavelength for each pixel (Wave dataset), used 
# cal file: WavePolynomes
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
                                                       removeMasked = True)\ # was spgMod = True
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

# Not present at CalBlock + RSRF script
# Update of the observation context
obs = updatePacsObservation(obs, 0.5, [slicedFrames, slicedDmcHead])

# remove some variables (clean-up of memory)
del pp, orbitEphem, slicedDmcHead, slicedFrames, slicedRawRamp, timeCorr, hp
del level0, additionalOutContexts

time_2 = datetime.now()
time = time_2 - time_1

print "After level 0.5: ", time.seconds

"""
0'5 -> 1
"""

# Extract the (previously-reduced and saved) level 0_5 out of the 
# ObservationContext
level0_5 = PacsContext(obs.level0_5)

# extract the frames for your camera
slicedFrames = level0_5.fitted.getCamera(camera).product

"""
What's the point?
"""
# Check that the science frames are not masked out
# checkScienceAvailable(slicedFrames)

# Detect and flag glitches ("GLITCH" mask)
# copy=True makes slicedFrames a fully independent product
# Activate all masks, for all slices, before deglitching
slicedFrames = activateMasks(slicedFrames, String1d([" "]),\
                             exclusive = True, copy = True)
slicedFrames = specFlagGlitchFramesQTest(slicedFrames)

# add quality information to meta data (such as glitch and saturation rate)
slicedFrames = activateMasks(slicedFrames, slicedFrames.get(0).getMaskTypes())

"""
What's the point???
"""
slicedFrames = addQualityInformation(slicedFrames)

# converts the signal level to the smallest capacitance
# used cal file: capacitanceRatios
slicedFrames = convertSignal2StandardCap(slicedFrames, calTree=calTree)

"""
CalBlock + RSRF
Same methods as HIPE script
"""
# Derive detectors' response from calibration block
# used cal files: observedResponse, calSourceFlux
calBlock = selectSlices(slicedFrames, scical="cal").get(0)
csResponseAndDark = specDiffCs(calBlock, calTree = calTree)

"""
Old stuff
"""
# calculate the differential signal of each on-off pair for each chopper cycle
slicedFrames = specDiffChop(slicedFrames, scical = "cal", keepall = False,\ # was scical = sci
                            normalize = False)
"""
CalBlock + RSRF
"""
# Divide by the relative spectral response function 
# Used cal files: rsrfR1, rsrfB2A, rsrfB2B or rsrfB3A
slicedFrames = rsrfCal(slicedFrames, calTree = calTree)

# Divide by the response
# Use intermediate product from specDiffCs : csResponseAndDark
slicedFrames = specRespCal(slicedFrames, csResponseAndDark = csResponseAndDark,\
                           calTree = calTree) 

"""
Old stuff
"""
# convert the Frames to a PacsCube
slicedCubes = specFrames2PacsCube(slicedFrames)        

# compute ra/dec meta keywords
slicedCubes = centerRaDecMetaData(slicedCubes)

# Update of the observation context
obs = updatePacsObservation(obs, 1.0, [slicedFrames, slicedCubes])

# Remove some variables (memory clean-up)
# del slicedFrames, slicedCubes, level0_5 

del slicedFrames, level0_5

time_3 = datetime.now()
time = time_3 - time_2

print "After level 1: ", time.seconds

"""
1 -> 2 Flatfielding?
"""

"""
# Always use the product sink for this script
sink.setUsed(True)

# Extract the (previously-reduced and saved) level 1 out of the
# ObservationContext
level1 = PacsContext(obs.level1)

# extract level1 frames  and cubes for your camera   
slicedCubes = level1.cube.getCamera(camera).product
slicedFrames = level1.fitted.getCamera(camera).product
# Computes the telescope background flux and scales the normalized signal
# with the telescope background flux using asymmetric chopping
slicedFramesCal, background = specRespCalToTelescope(slicedFrames, 
                                                     obs.auxiliary.hk,\
                                                     calTree = calTree, 
                                                     reduceNoise = 1, copy = 1)
# convert the Frames to a PacsCube
slicedCubesCal = specFrames2PacsCube(slicedFramesCal)     
# compute ra/dec meta keywords
slicedCubesCal = centerRaDecMetaData(slicedCubesCal)

# copyCube=True makes slicedCubes a fully independent product
"""
copyCube = True
"""
# Flatfielding for line spectroscopy and short range scans (up to 5 micron)
# only. (See the ipipe scripts and the PDRG for an explanation of the 
# flatfielding tasks.)
#
# For SED and large range spectroscopy, note that flatfielding is done in the
# ipipe scripts. (For line spectroscopy, you should anyway redo the 
# flatfielding so you can check the results)
lineSpec = isLineSpec(slicedCubes)
shortRange = isShortRange(obs)
maskNotFF = False


ffUpsample = getUpsample(obs)
"""
# 1. Flag outliers and rebin
"""
oversample = ?
upsample = ?
"""
waveGrid = wavelengthGrid(slicedCubes, oversample = 2, upsample = 3,\
                          calTree = calTree)
slicedCubes = activateMasks(slicedCubes,\
                            String1d(["GLITCH", "UNCLEANCHOP", "NOISYPIXELS",\
                                      "RAWSATURATION", "SATURATION",\
                                      "GRATMOVE", "BADPIXELS",\
                                      "INVALID"]), exclusive = True,\
                                                   copy = copyCube)
"""
slicedCubesCal = activateMasks(slicedCubesCal,\
                               String1d(["GLITCH", "UNCLEANCHOP",\
                                         "NOISYPIXELS", "RAWSATURATION",\
                                         "SATURATION", "GRATMOVE", "BADPIXELS",\
                                         "INVALID"]), exclusive = True,\
                                                      copy = copyCube)
copyCube = False
"""
slicedCubes = specFlagOutliers(slicedCubes, waveGrid, nSigma = 5, nIter = 1)
"""
slicedCubesCal = specFlagOutliers(slicedCubesCal, waveGrid, nSigma = 5,\
                                  nIter = 1)
"""
slicedCubes = activateMasks(slicedCubes,\
                            String1d(["GLITCH", "UNCLEANCHOP", "NOISYPIXELS",\
                                      "RAWSATURATION", "SATURATION",\
                                      "GRATMOVE", "OUTLIERS", "BADPIXELS",\
                                      "INVALID"]), exclusive = True)
slicedRebinnedCubes = specWaveRebin(slicedCubes, waveGrid)
slicedCubes = selectSlices(slicedCubes, refContext = slicedRebinnedCubes)
"""
slicedCubesCal = selectSlices(slicedCubesCal, refContext = slicedRebinnedCubes)
"""
width = 2.5    
# 217 was the maximum acceptable value?
# 2. mask the line
slicedCubes = maskLines(slicedCubes, slicedRebinnedCubes, calTree = calTree,\
                        widthDetect = width, widthMask = width,\
                        threshold = 10.0, maskType = "INLINE")
"""
slicedCubesCal = maskLines(slicedCubesCal,slicedRebinnedCubes,\
                           calTree = calTree, widthDetect = width,\
                           widthMask = width, threshold = 10.0,\
                           maskType = "INLINE")
"""
# 3. do the flatfielding
slicedCubes = specFlatFieldLine(slicedCubes, calTree = calTree, scaling = 1,\
                                maxrange = [190.,230.], slopeInContinuum = 1,\ # was 55., 190,
                                maxScaling = 2., maskType = "OUTLIERS_FF",\
                                offset = 0)
"""
slicedCubesCal = specFlatFieldLine(slicedCubesCal, calTree = calTree,\
                                   scaling = 1, maxrange = [55.,230.],\
                                   slopeInContinuum = 1, maxScaling = 2.,\
                                   maskType = "OUTLIERS_FF", offset = 0)
"""

# Si desactiva INLINE no se van los datos "buenos"?
# 4. Rename mask OUTLIERS to OUTLIERS_B4FF (specFlagOutliers would refuse to 
# overwrite OUTLIERS) & deactivate mask INLINE
slicedCubes.renameMask("OUTLIERS", "OUTLIERS_B4FF")
slicedCubes = deactivateMasks(slicedCubes,\
                              String1d(["INLINE", "OUTLIERS_B4FF"]))
"""
slicedCubesCal.renameMask("OUTLIERS", "OUTLIERS_B4FF")
slicedCubesCal = deactivateMasks(slicedCubesCal,\
                                 String1d(["INLINE", "OUTLIERS_B4FF"]))
"""
# del ffUpsample, width

del width # was del ffUpsample, width

time_4 = datetime.now()
time = time_4 - time_3

print "After level 1: ", time.seconds

# Building the wavelength grids for each slice
# Used cal file: wavelengthGrid
upsample = getUpsample(obs)
waveGrid = wavelengthGrid(slicedCubes, oversample=2, upsample = upsample,\
                          calTree = calTree)

# Como funciona esto????
# Active masks 
slicedCubes = activateMasks(slicedCubes,\
                            String1d(["GLITCH", "UNCLEANCHOP", "SATURATION",\
                                      "GRATMOVE", "BADFITPIX",\
                                      "BADPIXELS"]), exclusive = True, copy = copyCube)
"""
slicedCubesCal = activateMasks(slicedCubesCal,\
                               String1d(["GLITCH", "UNCLEANCHOP", "SATURATION",\
                                         "GRATMOVE", "BADFITPIX",\
                                         "BADPIXELS"]), exclusive = True, copy = copyCube)
"""
# Flag the remaining outliers (sigma-clipping in wavelength domain), with 
# default parameters here
slicedCubes = specFlagOutliers(slicedCubes, waveGrid)
"""
slicedCubesCal = specFlagOutliers(slicedCubesCal, waveGrid)
"""

# Rebin all cubes on consistent wavelength grids
masksForRebinning = String1d(["OUTOFBAND", "GLITCH", "UNCLEANCHOP",\
                              "SATURATION", "GRATMOVE", "BADFITPIX",\
                              "OUTLIERS", "BADPIXELS"])

# Esta era la mascara adecuada para lo mio?
# if maskNotFF:
masksForRebinning.append("NOTFFED")
slicedCubes = activateMasks(slicedCubes, masksForRebinning, exclusive = True)
slicedRebinnedCubes = specWaveRebin(slicedCubes, waveGrid)

# Only continue if there is at least one slice leftover after red-leak filtering
if slicedRebinnedCubes.refs.size() > 0:

    # Combine the nod-A & nod-B rebinned cubes.
    # All cubes at the same raster position are averaged.
    # This is the final science-grade product for spatially undersampled
    # rasters and single pointings
    slicedRebinnedCubes = specAddNodCubes(slicedRebinnedCubes)  

    # Computes the telescope background flux and scales the normalized signal 
    # with the telescope background flux
    slicedRebinnedCubes, background = specRespCalToTelescope(slicedRebinnedCubes,\
                                                             obs.auxiliary.hk,\
                                                             calTree = calTree)
    
    # compute ra/dec meta keywords
    slicedRebinnedCubes = centerRaDecMetaData(slicedRebinnedCubes)
    
    # convert the cubes to a table 
    slicedTable = pacsSpecCubeToTable(slicedRebinnedCubes)
      
    # Compute equidistant wavelength grid for equidistant regridding
    equidistantWaveGrid = wavelengthGrid(slicedCubes, oversample = 2,\
                                         upsample = upsample,\
                                         calTree = calTree, regularGrid = True,\
                                         fracMinBinSize = 0.35)
    
    # determine mapping algorithm and parameters
    driz, pixelSize, interpolatePixelSize, oversampleSpace, upsampleSpace, pixFrac, source, mapType = determineMappingAlgorithm(slicedRebinnedCubes, camera)
    
    # Mosaic, per wavelength range, all raster pointings into a single cube
    slicedDrizzledCubes = None
    slicedDrizzledEquidistantCubes = None
    slicedInterpolatedCubes = None
    slicedInterpolatedEquidistantCubes = None
    slicedProjectedEquidistantCubes = None
    if driz:
        print "Driz applied"
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
        print "drizzle es: ", drizzle
        slicedDrizzledCubes = centerRaDecMetaData(slicedDrizzledCubes)
        sink.saveWhenMemoryShort(slicedDrizzledCubes)
        slicedDrizzledEquidistantCubes = specRegridWavelength(slicedDrizzledCubes,\
                                                              equidistantWaveGridForDrizzle)
        sink.saveWhenMemoryShort(slicedDrizzledEquidistantCubes)
        slicedProjectedCubes = specProject(slicedRebinnedCubes,\
                                           cubeWithOutputGrid = slicedDrizzledCubes)
        del spaceGrid, waveGridForDrizzle, equidistantWaveGridForDrizzle
        del oversampleWave, upsampleWave
    else:
        slicedProjectedCubes = specProject(slicedRebinnedCubes,\
                                           outputPixelsize=pixelSize)
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
        if isRangeSpec(obs):
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
    obs = updatePacsObservation(obs, 2.0, [slicedRebinnedCubes, # slicedCubesCal were included
    slicedProjectedCubes, slicedDrizzledCubes, slicedTable,
    slicedInterpolatedCubes, spectra1d, slicedDrizzledEquidistantCubes, 
    slicedInterpolatedEquidistantCubes, slicedProjectedEquidistantCubes])
    # remove variables to cleanup memory
    del slicedTable, equidistantWaveGrid, driz, pixelSize, interpolatePixelSize
    del oversampleSpace, upsampleSpace, pixFrac, source, mapType
    del slicedDrizzledCubes, slicedDrizzledEquidistantCubes
    del slicedInterpolatedCubes, slicedInterpolatedEquidistantCubes
    del slicedProjectedCubes, slicedProjectedEquidistantCubes, spectra1d
else:
    LOGGER.warning("No slices left anymore after filtering red-leak and out-of-band slices.")

# Delete some variables (memory clean-up)
del slicedCubes, slicedFrames, slicedFramesCal, background # slicedCubesCal were included
del copyCube, lineSpec, shortRange, maskNotFF, upsample, waveGrid
del masksForRebinning, slicedRebinnedCubes

# restore default sink state
restoreOldSinkState()

time_5 = datetime.now()
time = time_5 - time_4

print "After level 2: ", time.seconds

# Must plot the values? Or save them?
