#  coding = utf-8
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
from herschel.pacs.spg.spec import *
from herschel.pacs.cal import *
from herschel.ia.numeric import *
from herschel.ia.jconsole import *
from herschel.pacs.spg.pipeline import *  


#*******************************************************************************
# Get data
#*******************************************************************************
#if ((not locals().has_key('multiObs')) or (not multiObs)):
#    obsid = 1342250905

obsid = 1342246381

# Next, get the data
useHsa = 1
obs = getObservation(obsid, verbose = True, useHsa = useHsa,\
                     poolLocation = None, poolName = None)


#*******************************************************************************
# Preparation
#*******************************************************************************
#
#-------------------------------------------------------------------------------
# SETUP 1: 
#    red or blue camera? This the user has to set before running the script, 
#    using the command e.g.
#       > camera = "blue" 
#    the try/except here will set the camera to "blue" if it has not already
#    been defined
try:
    camera
except NameError:
    camera = 'red'

# Checks for a particular type of anomaly (H_SC-70 DECMEC) and adds a quality
# flag if found.
# (This refers to a loss of data, and if this quality flag became set while the 
# SPG was running on your data, then your data would have gone through an extra 
# quality control.) 
# If the anomaly is present, then a Meta Data entry "qflag_DMANOG4L_p" will be 
# added to obs, and a flag is added to the "quality" of obs.
obs = checkForAnomaly70(obs)

# filter meta keywords and update descriptions
modifyMetaData(obs)

# add extra meta data 
pacsEnhanceMetaData(obs)
    
# copy the metadata from the ObservationContext to the level0 product
pacsPropagateMetaKeywords(obs,'0', obs.level0)

# Extract the level0 from the ObservationContext 
level0 = PacsContext(obs.level0)
level0 = level0.updateContextType()
obs.level0 = level0

# Extract the pointing product
pp = obs.auxiliary.pointing

# Extract the orbit ephemeris information
orbitEphem = obs.auxiliary.orbitEphemeris

# Extract Time Correlation which is used to convert in addUtc
timeCorr = obs.auxiliary.timeCorrelation


#-------------------------------------------------------------------------------------------
# SETUP 2:
# Set up the calibration tree. 
# First check whether calTree already exists, since it could have been filled 
# by the SPG pipeline 
# If not, then take it from your current HIPE build, and then put it into the 
# ObservationContext so that it is stored there for future reference
try:
    calTree
except NameError:
    calTree = getCalTree(obs = obs)
    obs.calibration = calTree

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


# ******************************************************************************
#         Processing
# ******************************************************************************
# 
# Flag the saturated data in a mask "SATURATION" (and "RAWSATURATION": this 
# exploits the raw ramps downlinked for a single pixel of the data array)
# used cal files: RampSatLimits and SignalSatLimits
# copy=1 makes slicedFrames a fully independent product
slicedFrames = specFlagSaturationFrames(slicedFrames, rawRamp = slicedRawRamp,
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
slicedFrames = specAddInstantPointing(slicedFrames, pp, calTree = calTree,
                                      orbitEphem = orbitEphem,
                                      horizonsProduct = hp)    
#copy the saa meta keyword to the ObservationContext meta HCSS-SCR 19230
obs.meta["solarAspectAngleMean"] = slicedFrames.meta["solarAspectAngleMean"].copy()
obs.meta["solarAspectAngleRms"] = slicedFrames.meta["solarAspectAngleRms"].copy()

# If SSO, move SSO target to a fixed position in sky. This is needed for 
# mapping SSOs.
if (isSolarSystemObject(obs)):
    slicedFrames = correctRaDec4Sso (slicedFrames, orbitEphem = orbitEphem,
                                     horizonsProduct = hp, linear = 0)

# This task extends the Status of Frames with the parameters GRATSCAN, CHOPPER,
# CHOPPOS used cal file: ChopperThrowDescription
slicedFrames = specExtendStatus(slicedFrames, calTree = calTree)
#
# This task converts the chopper readouts to an angle wrt. focal plane unit and 
# the sky and adds this to the status, used cal file: ChopperAngle and
# ChopperSkyAngle
slicedFrames = convertChopper2Angle(slicedFrames, calTree = calTree)

# This task adds the positions for each pixel (Ra and Dec dataset) 
# used cal files: ArrayInstrument and ModuleArray
slicedFrames = specAssignRaDec(slicedFrames, calTree = calTree)

# This task adds the wavelength for each pixel (Wave dataset), used cal file: 
# WavePolynomes
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
obs = updatePacsObservation(obs, 0.5, [slicedFrames, slicedDmcHead])

# remove some variables (clean-up of memory)
del pp, orbitEphem, slicedDmcHead, slicedFrames, slicedRawRamp, timeCorr, hp
del level0, additionalOutContexts