#  coding = utf-8
# 
#  This file is part of Herschel Common Science System (HCSS).
#  Copyright 2001-2010 Herschel Science Ground Segment Consortium
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

from herschel.pacs.spg.pipeline import *
from herschel.pacs.spg.spec import *
from herschel.pacs.spg.common import *
from herschel.pacs.signal.context import *
from herschel.pacs.cal import GetPacsCalDataTask
from herschel.pacs.spg.common import SlicingRule
from herschel.ia.numeric import *
from herschel.pacs.spg.pipeline.spg_spec_tools import *

#*******************************************************************************
# Preparation
#*******************************************************************************

# SETUP 1: 
#    red or blue camera? This the user has to set before running the script, 
#    using the command e.g.
#       > camera = "red" 
#    the try/except here will set the camera to "blue" if it has not 
# already been defined
try:
    camera
except NameError:
    camera = 'red'

# Extract the (previously-reduced and saved) level 0_5 out of the 
# ObservationContext
level0_5 = PacsContext(obs.level0_5)



# SETUP 2:
# Set up the calibration tree. 
# First check whether calTree already exists, since it could have been filled 
# by the SPG pipeline. If not, then take it from your current HIPE build, and 
# then put it into the ObservationContext so that it is stored there for 
# future reference
try:
    calTree
except NameError:
    calTree = getCalTree(obs=obs)
    obs.calibration = calTree

# extract the frames for your camera
slicedFrames = level0_5.fitted.getCamera(camera).product

# Check that the science frames are not masked out
checkScienceAvailable(slicedFrames)

#
#*******************************************************************************
#         Processing
#*******************************************************************************
#
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
slicedFrames = convertSignal2StandardCap(slicedFrames, calTree = calTree)
 
# New bit
calBlock = selectSlices(slicedFrames,scical="cal").get(0)
csResponseAndDark = specDiffCs(calBlock, calTree = calTree)

# Compute the differential signal of each on-off pair of datapoints, for each 
# chopper cycle. The calibration block is cut out of the slicedFrames, so 
# only the scientific slices remain.
slicedFrames = specDiffChop(slicedFrames, scical = "sci", keepall = False,\
                            normalize = False)
slicedFrames = rsrfCal(slicedFrames, calTree=calTree)

# Divide by the response
# Use intermediate product from specDiffCs : csResponseAndDark
slicedFrames = specRespCal(slicedFrames, csResponseAndDark = csResponseAndDark,\
                           calTree=calTree) 

"""
# Old bit
# calculate the differential signal of each on-off pair for each chopper cycle
slicedFrames = specDiffChop(slicedFrames, scical = "sci", keepall = False,\
                            normalize=True)
#
"""

# convert the Frames to a PacsCube
slicedCubes = specFrames2PacsCube(slicedFrames)        

# compute ra/dec meta keywords
slicedCubes = centerRaDecMetaData(slicedCubes)

# Update of the observation context
obs = updatePacsObservation(obs, 1.0, [slicedFrames, slicedCubes])

slicedCubes_copy = slicedCubes.copy() # Remove
slicedFrames_copy=slicedFrames.copy() # Remove

# Remove some variables (memory clean-up)
del slicedFrames, slicedCubes, level0_5
