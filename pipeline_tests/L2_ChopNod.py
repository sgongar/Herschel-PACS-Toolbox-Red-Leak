#  coding = utf-8
# 
#  This file is part of Herschel Common Science System (HCSS).
#  Copyright 2001-2011 Herschel Science Ground Segment Consortium
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
from herschel.pacs.signal.context import *
from herschel.pacs.cal import GetPacsCalDataTask
from herschel.pacs.spg.spec import *
from herschel.ia.numeric import *
from herschel.pacs.spg.pipeline import *  
from herschel.pacs.spg.pipeline.ProductSinkHandling import *
from herschel.pacs.spg.pipeline.spg_spec_tools import *

first_case = str(working_dir) + 'case_noFF.py'
second_case = str(working_dir) + 'case_FFRange_Sel.py'
third_case = str(working_dir) + 'case_FFLine_198_203.py'
fourth_case = str(working_dir) + 'case_FFLine_199_201.py'
fifth_case = str(working_dir) + 'case_FFLine_161_163.py'
six_case = str(working_dir) + 'case_FFRange_All.py'

camera = 'red'
    
# Always use the product sink for this script
sink.setUsed(True)

# Extract the (previously-reduced and saved) level 1 out of the 
# ObservationContext
level1 = PacsContext(obs.level1)

# SETUP 2:
# Set up the calibration tree. 
# First check whether calTree already exists, since it could have been filled 
# by the SPG pipeline 
# If not, then take it from your current HIPE build, and then put it into the 
# ObservationContext so that it is stored there for future reference
try:
    calTree
except NameError:
    calTree = getCalTree(obs=obs)
    obs.calibration = calTree

# extract level1 frames  and cubes for your camera
slicedCubes = level1.cube.getCamera(camera).product
slicedFrames = level1.fitted.getCamera(camera).product

#*******************************************************************************
#         Processing
#*******************************************************************************
copyCube = True

# Flatfielding for line spectroscopy and short range scans (up to 5 micron) only
# (See the ipipe scripts and the PDRG for an explanation of the flatfielding
# tasks.)

# For SED and large range spectroscopy, note that flatfielding is done in the 
# ipipe scripts. (For line spectroscopy, you should anyway redo the 
# flatfielding so you can check the results)

lineSpec = isLineSpec(slicedCubes)
shortRange = isShortRange(obs)
maskNotFF = False

# Four cases
# - Withouth flatfielding
# - Using specFlatfieldRange maxRange=[198.0, 203.0] with excludeLeak = False
# - Using specFlatfieldLine maxRange=[198.0, 203]
# - Using specFlatfieldLine maxRange=[199.0, 201]
# - Using specFlatfieldRange all the range with excludeLeak = False

# First case
first_case_start = time.time()
slicedCubes = slicedCubes_copy.copy()
slicedFrames = slicedFrames_copy.copy()
execfile(str(first_case))
name = str(obsid) + "_case1"
saveObservation(obs, poolLocation = pool_dir, poolName = name)

test_time = time.time() - first_case_start
test_time_m = int(test_time/60)
test_time_s = int(test_time - test_time_m*60)
 
trackfile = open(trackfilename, 'a')
trackfile.write('End first case ' + str(obsids.keys()[i]) + " " + camera +
                ' Duration: ' + str(test_time_m) + ' m ' + str(test_time_s) + 
                ' s ' + '\n')
trackfile.close()

# Second case
second_case_start = time.time()
slicedCubes = slicedCubes_copy.copy()
slicedFrames = slicedFrames_copy.copy()
execfile(str(second_case))
name = str(obsid) + "_case2"
saveObservation(obs, poolLocation = pool_dir, poolName = name)

test_time = time.time() - second_case_start
test_time_m = int(test_time/60)
test_time_s = int(test_time - test_time_m*60)
 
trackfile = open(trackfilename, 'a')
trackfile.write('End second case ' + str(obsids.keys()[i]) + " " + camera +
                ' Duration: ' + str(test_time_m) + ' m ' + str(test_time_s) + 
                ' s ' + '\n')
trackfile.close()

# Third case
third_case_start = time.time()

slicedCubes = slicedCubes_copy.copy()
slicedFrames = slicedFrames_copy.copy()
execfile(str(third_case))
name = str(obsid) + "_case3"
saveObservation(obs, poolLocation = pool_dir, poolName = name)

test_time = time.time() - third_case_start
test_time_m = int(test_time/60)
test_time_s = int(test_time - test_time_m*60)
 
trackfile = open(trackfilename, 'a')
trackfile.write('End third case ' + str(obsids.keys()[i]) + " " + camera +
                ' Duration: ' + str(test_time_m) + ' m ' + str(test_time_s) + 
                ' s ' + '\n')
trackfile.close()

# Fourth case
fourth_case_start = time.time()

slicedCubes = slicedCubes_copy.copy()
slicedFrames = slicedFrames_copy.copy()
execfile(str(fourth_case))
name = str(obsid) + "_case4"
saveObservation(obs, poolLocation = pool_dir, poolName = name)

test_time = time.time() - fourth_case_start
test_time_m = int(test_time/60)
test_time_s = int(test_time - test_time_m*60)
 
trackfile = open(trackfilename, 'a')
trackfile.write('End fourth case ' + str(obsids.keys()[i]) + " " + camera +
                ' Duration: ' + str(test_time_m) + ' m ' + str(test_time_s) + 
                ' s ' + '\n')
trackfile.close()

# Fifth case
fifth_case_start = time.time()

slicedCubes = slicedCubes_copy.copy()
slicedFrames = slicedFrames_copy.copy()
execfile(str(fifth_case))
name = str(obsid) + "_case5"
saveObservation(obs, poolLocation = pool_dir, poolName = name)

test_time = time.time() - fifth_case_start
test_time_m = int(test_time/60)
test_time_s = int(test_time - test_time_m*60)
 
trackfile = open(trackfilename, 'a')
trackfile.write('End fifth case ' + str(obsids.keys()[i]) + " " + camera +
                ' Duration: ' + str(test_time_m) + ' m ' + str(test_time_s) + 
                ' s ' + '\n')
trackfile.close()

# Six case
six_case_start = time.time()
slicedCubes = slicedCubes_copy.copy()
slicedFrames = slicedFrames_copy.copy()
execfile(str(six_case))
name = str(obsid) + "_case6"
saveObservation(obs, poolLocation = pool_dir, poolName = name)

test_time = time.time() - six_case_start
test_time_m = int(test_time/60)
test_time_s = int(test_time - test_time_m*60)
 
trackfile = open(trackfilename, 'a')
trackfile.write('End normal case ' + str(obsids.keys()[i]) + " " + camera +
                ' Duration: ' + str(test_time_m) + ' m ' + str(test_time_s) + 
                ' s ' + '\n')
trackfile.close()
