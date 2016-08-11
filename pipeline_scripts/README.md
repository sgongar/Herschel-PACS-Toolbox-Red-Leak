### Working in progress

#### Final pipeline scripts 
These scripts are the final versions for pipeline process.

Are locate at: 

`~/.hcss.d/repository/modules/hcss/pacs_spg_pipeline/<HIPE.VERSION>/herschel/pacs/spg/pipeline/ipipe/spec/`
##### L05_Frames.py
 - No changes were applied to this pipeline section.

##### L1_ChopNod.py
- Calibration schema was changed to TBN to RSRF calibration. The following lines are erase.
```python
# calculate the differential signal of each on-off pair for each chopper cycle
slicedFrames = specDiffChop(slicedFrames, scical = "sci", keepall = False, normalize=True)
```
- The old lines are replaced for these new ones.
```python
csResponseAndDark = specDiffCs(calBlock, calTree=calTree)
#
#
# Compute the differential signal of each on-off pair of datapoints, for each 
# chopper cycle. The calibration block is cut out of the slicedFrames, so 
# only the scientific slices remain.
slicedFrames = specDiffChop(slicedFrames, scical="sci", keepall=False,\
			                            normalize=False)
slicedFrames = rsrfCal(slicedFrames, calTree=calTree)
#
#
# Divide by the response
# Use intermediate product from specDiffCs : csResponseAndDark
slicedFrames = specRespCal(slicedFrames, csResponseAndDark = csResponseAndDark,
			                     calTree=calTree) 
```
##### L2_ChopNod.py
 - These lines have been removed from the original one. They are not longer necessaries.
```python
slicedFramesCal, background = specRespCalToTelescope(slicedFrames, obs.auxiliary.hk,
                                                     calTree = calTree, reduceNoise=1,
                                                     copy=1)
slicedCubesCal = specFrames2PacsCube(slicedFramesCal)
slicedCubesCal = centerRaDecMetaData(slicedCubesCal)
slicedCubesCal = activateMasks(slicedCubesCal,
                               String1d(["GLITCH","UNCLEANCHOP","NOISYPIXELS",
                                         "RAWSATURATION","SATURATION",
                                         "GRATMOVE", "BADPIXELS",
                                         "INVALID"]), exclusive = True, copy = copyCube)
slicedCubesCal = specFlagOutliers(slicedCubesCal, waveGrid, nSigma=5, nIter=1)
slicedCubesCal = selectSlices(slicedCubesCal,refContext=slicedRebinnedCubes)
slicedCubesCal = maskLines(slicedCubesCal,slicedRebinnedCubes, calTree = calTree, 
                           widthDetect=width, widthMask=width, threshold=10.0,
                           maskType="INLINE")
slicedCubesCal = specFlatFieldLine(slicedCubesCal, calTree = calTree, scaling=1,
                                   maxrange=[55.,190.], slopeInContinuum=1,
                                   maxScaling=2., maskType="OUTLIERS_FF", offset=0)
slicedFramesCal = specFlatFieldRange(slicedFramesCal,useSplinesModel=True,
                                     excludeLeaks=True, calTree=calTree, copy=copyCube)
slicedCubesCal.renameMask("OUTLIERS", "OUTLIERS_B4FF")
slicedCubesCal = deactivateMasks(slicedCubesCal, String1d(["INLINE", "OUTLIERS_B4FF"]))
slicedCubesCal = activateMasks(slicedCubesCal,
                               String1d(["GLITCH","UNCLEANCHOP","SATURATION",
                                         "GRATMOVE","BADFITPIX",
                                         "BADPIXELS"]), exclusive=True, copy=copyCube)
slicedCubesCal = specFlagOutliers(slicedCubesCal, waveGrid)
slicedCubesCal = selectSlices(slicedCubesCal,refContext=slicedRebinnedCubes)
slicedRebinnedCubes, background = specRespCalToTelescope(slicedRebinnedCubes,
                                                         obs.auxiliary.hk, calTree=calTree)
```
 - Minor changes have been made to the following two lines. In the first one the range limitation was remove, excludeLeaks was set to False in the second line, allowing now the leaked ranges calculation.
```python
slicedCubes = specFlatFieldLine(slicedCubes, calTree = calTree, scaling=1, slopeInContinuum=1,
                                maxScaling=2., maskType="OUTLIERS_FF", offset=0)
slicedFrames = specFlatFieldRange(slicedFrames,useSplinesModel=True, excludeLeaks=False,
                                  calTree=calTree, copy=copyCube)
```
 - Since there is no more SlicedCubesCal all the references in the script should be removed.
```python
slicedDrizzledCubes = drizzle(slicedCubes, wavelengthGrid=waveGridForDrizzle, spatialGrid=spaceGrid)[0]
obs = updatePacsObservation(obs, 2.0, [slicedRebinnedCubes, slicedProjectedCubes, slicedDrizzledCubes, 
	                                     slicedTable, slicedInterpolatedCubes, spectra1d, 
	                                     slicedDrizzledEquidistantCubes, 
	                                     slicedInterpolatedEquidistantCubes,
	                                     slicedProjectedEquidistantCubes])
del slicedCubes, slicedFrames, \
copyCube, lineSpec, shortRange, maskNotFF, upsample, waveGrid, masksForRebinning, slicedRebinnedCubes
```
##### L2_Unchopped.py
 - excludeLeaks should be set to False instead True. The calibration schema will remain in the same way.
```python
slicedFrames = specFlatFieldRange(slicedFrames,useSplinesModel=True, excludeLeaks=False,
                                  calTree = calTree, copy = copyCube)
```
