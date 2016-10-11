# 
#  This file is part of Herschel Common Science System (HCSS).
#  Copyright 2001-2013 Herschel Science Ground Segment Consortium
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
# Some tools used in several spectrometer SPG scripts
#
# Author: Jeroen de Jong
#

from java.util.logging import Logger, Level
from herschel.ia.pal import ListContext
from herschel.pacs.signal import ProductUtil
from herschel.pacs.spg.common.util import PacsProcessingException
from herschel.pacs.signal import RangeDescription

LOGGER = Logger.getLogger("herschel.pacs.spg.pipeline.spg_spec_tools")
       
# Computes the average ra/dec from the rebinned cubes of a level-2 product
# and puts this into the observation context meta data
def extractRaDecToObs(obs):
    context = obs.level2


    subcontext = ListContext()
    # for camera in ['red', 'blue']:
    for camera in ['red']:
        rcube = context.getCamera(camera).rcube
        if rcube.available:
            subcontext.refs.add(rcube.productRef)

    # tamanio = subcontext.getAllRefs().size()
    ProductUtil.averageRaDec(subcontext)
    
    # print context
    
    context.meta.set("ra", subcontext.meta["ra"])
    context.meta.set("dec", subcontext.meta["dec"])
    obs.meta["ra"].value = subcontext.meta["ra"].value
    obs.meta["dec"].value = subcontext.meta["dec"].value
    
# #
# Project the cube(s), at the same time mosaic together pointings of a raster
# #
# Before you proceed with the scientific analysis, you will need to make a choice
# based on the nature of your object (extended or not), the type of observation
# that was performed (pointed or raster mapping), and its spatial sampling
# (oversampled or not). In the SPG we offer a choice of 2 output spaxel sizes:
# 3arcsec, for oversampled rasters, and 0.5 otherwise. See the PACS Data Reduction Guide
# for more information.
def determineMappingAlgorithm(product, camera):
    driz = False
    pixelSize = 1.5
    interpolatePixelSize = 3.0
    oversampleSpace = 3
    upsampleSpace = 2
    pixFrac = 0.6
    mapType = "point"
    
    meta = product.meta
    source = meta['source'].value
    
    # Determine mapping type for extended sources
    if source != "point":
        mapType = "tiled"
        try:
            lineStep = meta["lineStep"].value
            pointStep = meta["pointStep"].value
            numLines = meta['numRasterLines'].value
            numPoints = meta['numRasterCol'].value            
            minSteps = min(numLines, numPoints)
            stepSize = max(lineStep, pointStep)
            if camera == 'blue':
                if stepSize <= 16 and stepSize > 3 and minSteps >= 3:
                    mapType = "nyquist"
                elif stepSize <= 3  and minSteps >= 3:
                    mapType = "oversampled"
                    pixFrac = 0.3
            else:
                if stepSize <= 24 and stepSize > 4.5  and minSteps >= 2:
                    mapType = "nyquist"
                elif stepSize <= 4.5 and minSteps >= 2:
                    mapType = "oversampled"
                    pixFrac = 0.3
        except:
            LOGGER.warning("No/incomplete mapping keywords found. Assuming point source.")
            mapType = "point"
            source = "point"
    LOGGER.info("mapping type: " + mapType)
    
    # Determine pixelsize for specProject
    if mapType == "oversampled" or mapType == "nyquist":
        pixelSize = 3.0
    elif mapType == 'point':
        pixelSize = 0.5
        
    # Determine whether to drizzle
    if meta.containsKey('cusMode') and meta['cusMode'].value == 'PacsLineSpec': 
        if (mapType == "nyquist" or mapType == "oversampled"):
            driz = True
            LOGGER.info("Do drizzle for camera " + camera)
#     except:
#         print "WARNING: could not determine source type."
    return driz, pixelSize, interpolatePixelSize, oversampleSpace, upsampleSpace, pixFrac, source, mapType

# Check that the science frames have not been masked out
def checkScienceAvailable(slicedFrames):
    if slicedFrames.numberOfScienceSlices==0:
        raise PacsProcessingException("All science Frames have been masked with OUTOFBAND. Cannot continue with processing.")
        

#
# Does product belong to a line spectroscopy observation?
#
def isLineSpec(product):
    return product.meta.containsKey('cusMode') and product.meta['cusMode'].value=='PacsLineSpec'

#
# Does product belong to a range spectroscopy observation?
#
def isRangeSpec(product):
    return product.meta.containsKey('cusMode') and product.meta['cusMode'].value=='PacsRangeSpec'

    
#
#  Is this a range spectroscopy observation with ranges of less than 5 micron?
# 
def isShortRange(obs):
    if isRangeSpec(obs):
        if obs.meta.containsKey("rangeSPOT"):
            rangeKeyw = obs.meta["rangeSPOT"].value
            rangeDescs = RangeDescription.getRanges(rangeKeyw,True)
            for desc in rangeDescs:
                LOGGER.fine("Checking range "+desc.name)
                rangeWidth = desc.maxWave-desc.minWave
                if rangeWidth<=5.0:
                    LOGGER.fine("Short range: width = "+str(rangeWidth))
                    return True
        else:
            raise Exception("No rangeSPOT keyword found. Cannot check for short ranges.")
    return False

def isHighDensity(obs):
    return obs.meta.containsKey('density') and obs.meta['density'].value=='high'
    
# Determine from which level to start
def determineLevel(obs):
    useLevel = 2.0
    levelx = None
    if obs.level2 is None:
        raise Exception("No level 2/2.5 data available in observation context")
    if obs.level2_5 is not None:
        useLevel = 2.5
        levelx = obs.level2_5  
    else:
        levelx = obs.level2
    return useLevel, levelx
    
# get the correct upsample 
def getUpsample(obs):
    upsample = 2
    if isLineSpec(obs) or (isRangeSpec(obs) and isHighDensity(obs)):
        upsample = 4
    return upsample

