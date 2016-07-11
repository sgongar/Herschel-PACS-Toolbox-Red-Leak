#  coding = utf-8

print "Processing first case\n"

lineSpec = isLineSpec(slicedCubes)
shortRange = isShortRange(obs)

if lineSpec or shortRange:
    print "not doing flatfielding"
elif isRangeSpec(obs):
    slicedCubes = specFrames2PacsCube(slicedFrames)
    slicedCubes = centerRaDecMetaData(slicedCubes)

# Building the wavelength grids for each slice
# Used cal file: wavelengthGrid
upsample = getUpsample(obs)
waveGrid = wavelengthGrid(slicedCubes, oversample=2, upsample=upsample,
                          calTree=calTree)

# Active masks 
slicedCubes = activateMasks(slicedCubes,
                            String1d(["GLITCH", "UNCLEANCHOP", "SATURATION", 
                                      "GRATMOVE", "BADFITPIX",
                                      "BADPIXELS"]), exclusive=True, 
                                                     copy=copyCube)

# Flag the remaining outliers (sigma-clipping in wavelength domain), 
# with default parameters here
slicedCubes = specFlagOutliers(slicedCubes, waveGrid)

# Rebin all cubes on consistent wavelength grids
masksForRebinning = String1d(["OUTOFBAND", "GLITCH", "UNCLEANCHOP", 
                              "SATURATION", "GRATMOVE", "BADFITPIX", 
                              "OUTLIERS", "BADPIXELS"])
masksForRebinning.append("NOTFFED")

slicedCubes = activateMasks(slicedCubes, masksForRebinning, exclusive=True)
slicedRebinnedCubes = specWaveRebin(slicedCubes, waveGrid)

print slicedRebinnedCubes.refs.size()

# Only continue if there is at least one slice leftover after red-leak filtering
if slicedRebinnedCubes.refs.size() > 0:
    # Select only the slices in the PACS cube which are also in the rebinned cube
    slicedCubes = selectSlices(slicedCubes, refContext=slicedRebinnedCubes)

    # Combine the nod-A & nod-B rebinned cubes.
    # All cubes at the same raster position are averaged.
    # This is the final science-grade product for spatially undersampled 
    # rasters and single pointings
    slicedRebinnedCubes = specAddNodCubes(slicedRebinnedCubes)  

    # Computes the telescope background flux and scales the normalized signal 
    # with the telescope background flux
    # slicedRebinnedCubes, background = specRespCalToTelescope(slicedRebinnedCubes, obs.auxiliary.hk, calTree = calTree)
    
    # compute ra/dec meta keywords
    slicedRebinnedCubes = centerRaDecMetaData(slicedRebinnedCubes)
    
    # convert the cubes to a table 
    slicedTable = pacsSpecCubeToTable(slicedRebinnedCubes)
      
    # Compute equidistant wavelength grid for equidistant regridding
    equidistantWaveGrid = wavelengthGrid(slicedCubes, oversample=2,
                                         upsample=upsample, calTree=calTree,
                                         regularGrid=True,
                                         fracMinBinSize=0.35)
    
    # determine mapping algorithm and parameters
    driz, pixelSize, interpolatePixelSize, oversampleSpace, upsampleSpace, pixFrac, source, mapType = determineMappingAlgorithm(slicedRebinnedCubes, camera)
    
    # Mosaic, per wavelength range, all raster pointings into a single cube
    slicedDrizzledCubes=None
    slicedDrizzledEquidistantCubes=None
    slicedInterpolatedCubes=None
    slicedInterpolatedEquidistantCubes=None
    slicedProjectedEquidistantCubes=None

    if driz:
        oversampleWave=2
        upsampleWave=upsample
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
        spaceGrid = spatialGrid(slicedCubes,
                                wavelengthGrid=waveGridForDrizzle,
                                oversample=oversampleSpace,
                                upsample=upsampleSpace, pixfrac=pixFrac, 
                                calTree=calTree)
        slicedDrizzledCubes = drizzle(slicedCubes, 
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
        if (mapType == "nyquist" or mapType == "oversampled"):
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
            c1_1st, c9_1st, c129_1st = extractCentralSpectrum(slicedRebinnedCubes,
                                                              smoothing='filter',
                                                              width=50,
                                                              preFilterWidth=15,
                                                              calTree=calTree)
        else:
            c1_1st, c9_1st, c129_1st = extractCentralSpectrum(slicedRebinnedCubes,
                                                              smoothing='median',
                                                              calTree=calTree)
        spectra1d = fillPacsCentralSpectra(slicedRebinnedCubes, 
                                           ptSrcSpec=c1_1st,
                                           ptSrc3x3Spec=c9_1st)
        # del c1_1st, c9_1st, c129_1st
        
    # update the level 2 of the ObservationContext 

    slicedRebinnedCubes.meta.set("sanitycheck",StringParameter("test1"))
    obs = updatePacsObservation(obs, 2.0, [slicedCubes, slicedRebinnedCubes, slicedProjectedCubes, slicedDrizzledCubes, 
    slicedTable, slicedInterpolatedCubes, spectra1d, slicedDrizzledEquidistantCubes, slicedInterpolatedEquidistantCubes,
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
del slicedFrames, lineSpec, shortRange
del maskNotFF, upsample, waveGrid, masksForRebinning, slicedRebinnedCubes

# restore default sink state
restoreOldSinkState()
