# coding = utf-8
# specflatfielding range
# range = [55.0, 203.0]

print "Processing normal case"
    
# Always use the product sink for this script
sink.setUsed(True)

# Extract the (previously-reduced and saved) level 1 out of the \
# ObservationContext
level1 = PacsContext(obs.level1)

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


# extract level1 frames  and cubes for your camera   
slicedCubes = level1.cube.getCamera(camera).product
slicedFrames = level1.fitted.getCamera(camera).product

# convert the Frames to a PacsCube
# slicedCubesCal = specFrames2PacsCube(slicedFramesCal)     
# compute ra/dec meta keywords
# slicedCubesCal = centerRaDecMetaData(slicedCubesCal)
#
# ******************************************************************************
#         Processing
# ******************************************************************************   
#
copyCube = True

# Flatfielding for line spectroscopy and short range scans (up to 5 micron) 
# only (See the ipipe scripts and the PDRG for an explanation of the 
# flatfielding tasks.)
#
# For SED and large range spectroscopy, note that flatfielding is done in the 
# ipipe scripts.
#
lineSpec = isLineSpec(slicedCubes)
shortRange = isShortRange(obs)
maskNotFF = False
if lineSpec or shortRange:
    ffUpsample = getUpsample(obs)
        
    # 1. Flag outliers and rebin
    waveGrid=wavelengthGrid(slicedCubes, oversample=2, upsample=ffUpsample,
                            calTree=calTree)
    slicedCubes = activateMasks(slicedCubes,
                                String1d(["GLITCH", "UNCLEANCHOP",
                                          "NOISYPIXELS", "RAWSATURATION",
                                          "SATURATION","GRATMOVE",
                                          "BADPIXELS", 
                                          "INVALID"]), exclusive=True,
                                                       copy=copyCube)
    copyCube = False
    slicedCubes = specFlagOutliers(slicedCubes, waveGrid, nSigma=5, nIter=1)

    slicedCubes = activateMasks(slicedCubes,
                                String1d(["GLITCH", "UNCLEANCHOP",
                                          "NOISYPIXELS", "RAWSATURATION",
                                          "SATURATION", "GRATMOVE",
                                          "OUTLIERS", "BADPIXELS",
                                          "INVALID"]), exclusive=True)
    slicedRebinnedCubes = specWaveRebin(slicedCubes, waveGrid)
    slicedCubes = selectSlices(slicedCubes,
                               refContext=slicedRebinnedCubes)
    width = 2.5
    if isRangeSpec(obs):
        width = 1.5
        
    # 2. mask the line
    slicedCubes = maskLines(slicedCubes,slicedRebinnedCubes, calTree=calTree,
                            widthDetect=width, widthMask=width,
                            threshold=10.0, maskType="INLINE")
    # 3. do the flatfielding
    slicedCubes = specFlatFieldLine(slicedCubes, calTree=calTree, scaling=1,
                                    maxrange=[55.0, 203.0],
                                    slopeInContinuum=1, maxScaling=2.,
                                    maskType="OUTLIERS_FF", offset=0)
    # 4. Rename mask OUTLIERS to OUTLIERS_B4FF (specFlagOutliers would refuse 
    #    to overwrite OUTLIERS) & deactivate mask INLINE
    slicedCubes.renameMask("OUTLIERS", "OUTLIERS_B4FF")
    slicedCubes = deactivateMasks(slicedCubes,
                                  String1d(["INLINE", "OUTLIERS_B4FF"]))
    del width
elif isRangeSpec(obs):
    slicedFrames = specFlatFieldRange(slicedFrames, useSplinesModel=True,
                                      excludeLeaks=False,
                                      selectedRange=[55.0, 220.0], 
                                      calTree=calTree, copy = copyCube)
    copyCube = False
    maskNotFF = True
    slicedCubes = specFrames2PacsCube(slicedFrames)
    # slicedCubesCal = specFrames2PacsCube(slicedFramesCal)
    slicedCubes = centerRaDecMetaData(slicedCubes)
    #  slicedCubesCal = centerRaDecMetaData(slicedCubesCal)

# Building the wavelength grids for each slice
# Used cal file: wavelengthGrid
ffUpsample = getUpsample(obs)
waveGrid=wavelengthGrid(slicedCubes, oversample=2, upsample=ffUpsample, 
                        calTree=calTree)
# Active masks 

slicedCubes = activateMasks(slicedCubes,
                            String1d(["GLITCH", "UNCLEANCHOP",
                                      "SATURATION", "GRATMOVE", "BADFITPIX",
                                      "BADPIXELS"]), exclusive = True,
                                                     copy = copyCube)
# Flag the remaining outliers (sigma-clipping in wavelength domain), with 
# default parameters here
slicedCubes = specFlagOutliers(slicedCubes, waveGrid)
# slicedCubesCal = specFlagOutliers(slicedCubesCal, waveGrid)

# Rebin all cubes on consistent wavelength grids
masksForRebinning = String1d(["OUTOFBAND", "GLITCH", "UNCLEANCHOP",
                              "SATURATION", "GRATMOVE", "BADFITPIX",
                              "OUTLIERS", "BADPIXELS"])
#if maskNotFF:
masksForRebinning.append("NOTFFED")
slicedCubes = activateMasks(slicedCubes, masksForRebinning, exclusive = True)
slicedRebinnedCubes = specWaveRebin(slicedCubes, waveGrid)

# Only continue if there is at least one slice leftover after red-leak filtering
if slicedRebinnedCubes.refs.size() > 0:

    # Select only the slices in the PACS cube which are also in the rebinned cube
    slicedCubes = selectSlices(slicedCubes, refContext=slicedRebinnedCubes)

    # Combine the nod-A & nod-B rebinned cubes.
    # All cubes at the same raster position are averaged.
    # This is the final science-grade product for spatially undersampled rasters
    # and single pointings
    slicedRebinnedCubes = specAddNodCubes(slicedRebinnedCubes)  

    # compute ra/dec meta keywords
    slicedRebinnedCubes = centerRaDecMetaData(slicedRebinnedCubes)
    
    # convert the cubes to a table 
    slicedTable = pacsSpecCubeToTable(slicedRebinnedCubes)
      
    # Compute equidistant wavelength grid for equidistant regridding
    equidistantWaveGrid = wavelengthGrid(slicedCubes, oversample=2, 
                                         upsample=ffUpsample, calTree=calTree,
                                         regularGrid = True,
                                         fracMinBinSize = 0.35)
    
    # determine mapping algorithm and parameters
    driz, pixelSize, interpolatePixelSize, oversampleSpace, upsampleSpace, pixFrac, source, mapType = determineMappingAlgorithm(slicedRebinnedCubes,camera)
    
    # Mosaic, per wavelength range, all raster pointings into a single cube
    slicedDrizzledCubes = None
    slicedDrizzledEquidistantCubes = None
    slicedInterpolatedCubes = None
    slicedInterpolatedEquidistantCubes = None
    slicedProjectedEquidistantCubes = None
    if driz:
        oversampleWave = 2
        upsampleWave = ffUpsample
        waveGridForDrizzle = wavelengthGrid(slicedCubes,
                                            oversample=oversampleWave,
                                            upsample=upsampleWave,
                                            calTree=calTree)
        equidistantWaveGridForDrizzle = wavelengthGrid(slicedCubes,
                                                      oversample=oversampleWave, 
                                                      upsample=upsampleWave, 
                                                      calTree=calTree,
                                                      regularGrid=True,
                                                      fracMinBinSize=0.35)
        spaceGrid = spatialGrid(slicedCubes, wavelengthGrid=waveGridForDrizzle,
                                oversample=oversampleSpace,
                                upsample=upsampleSpace, pixfrac=pixFrac,
                                calTree=calTree)
        slicedDrizzledCubes = drizzle(slicedCubesCal,
                                      wavelengthGrid=waveGridForDrizzle,
                                      spatialGrid=spaceGrid)[0]
        slicedDrizzledCubes = centerRaDecMetaData(slicedDrizzledCubes)
        sink.saveWhenMemoryShort(slicedDrizzledCubes)
        slicedDrizzledEquidistantCubes = specRegridWavelength(slicedDrizzledCubes,
                                                              equidistantWaveGridForDrizzle)
        sink.saveWhenMemoryShort(slicedDrizzledEquidistantCubes)
        slicedProjectedCubes = specProject(slicedRebinnedCubes,
                                           cubeWithOutputGrid=slicedDrizzledCubes)
        del spaceGrid, waveGridForDrizzle, equidistantWaveGridForDrizzle
        del oversampleWave, upsampleWave
    else:
        slicedProjectedCubes = specProject(slicedRebinnedCubes,
                                           outputPixelsize=pixelSize)
        if mapType != "oversampled":
            slicedInterpolatedCubes = specInterpolate(slicedRebinnedCubes,
                                                      outputPixelsize=interpolatePixelSize)
            slicedInterpolatedCubes = centerRaDecMetaData(slicedInterpolatedCubes)
        if (mapType=="nyquist" or mapType=="oversampled"):
            slicedProjectedEquidistantCubes = specRegridWavelength(slicedProjectedCubes,
                                                                   equidistantWaveGrid)
        else:
            slicedInterpolatedEquidistantCubes = specRegridWavelength(slicedInterpolatedCubes,
                                                                      equidistantWaveGrid)
    
    slicedProjectedCubes = centerRaDecMetaData(slicedProjectedCubes)
    sink.saveWhenMemoryShort(slicedProjectedCubes)
    
    # do a pointsource extraction for the pointed observations only
    spectra1d = None
    if source=='point':
        if isRangeSpec(obs):
            c1_nth, c9_nth, c129_nth = extractCentralSpectrum(slicedRebinnedCubes,
                                                              smoothing='filter',
                                                              width=50,
                                                              preFilterWidth=15,
                                                              calTree=calTree)
        else:
            c1_nth, c9_nth, c129_nth = extractCentralSpectrum(slicedRebinnedCubes,
                                                              smoothing='median',
                                                              calTree=calTree)
        spectra1d = fillPacsCentralSpectra(slicedRebinnedCubes, 
                                           ptSrcSpec=c1_nth,
                                           ptSrc3x3Spec=c9_nth)
        del c1_nth, c9_nth, c129_nth
        
    # update the level 2 of the ObservationContext 
    obs = updatePacsObservation(obs, 2.0, [slicedRebinnedCubes, 
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
del slicedCubes, slicedFrames
del copyCube, lineSpec, shortRange, maskNotFF, waveGrid # was upsample
del masksForRebinning, slicedRebinnedCubes

# restore default sink state
restoreOldSinkState()