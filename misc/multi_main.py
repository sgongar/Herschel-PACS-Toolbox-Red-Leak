#  coding = utf-8
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

import os
import time
import datetime
import shutil
import csv
import string
import thread

home_dir = os.getenv("HOME")
working_dir = str(home_dir) + '/hcss/workspace/Red-leak/'
pool_dir = str(working_dir) + 'pools/'
plot_dir = str(working_dir) + 'plots/'
csv_obs = str(working_dir) + 'obs_ids.csv'

save_obs = False

# Only for test reasons, change obsids for observations_dict_test
obsids = {}
obsids[1342186305] = "SEDA"
obsids[1342186798] = "SEDB"

start_time = time.time()
start_time_hr = datetime.datetime.fromtimestamp(start_time)
start_time_hr = str(start_time_hr)

if (not os.path.exists(working_dir)):
    os.mkdir(working_dir)
if (not os.path.exists(pool_dir)):
    os.mkdir(pool_dir)
if (not os.path.exists(plot_dir)):
    os.mkdir(plot_dir)

# Populate list from csv file
obs_list = []
with open(str(csv_obs), 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        obs_list.append(row[1])

# Create dictionary from list
observations_dict_test = {}
i = 0
j = 0
k = 0
w = 0
for i in range(len(obs_list)):
    if j == int(len(list(string.uppercase))):
        j = 0
        k = k + 1

    if k == int(len(list(string.uppercase))):
        k = 0
        w = w + 1

    observations_dict_test[obs_list[i]] = 'SED' +\
                                          str(list(string.uppercase)[j]) +\
                                          str(list(string.uppercase)[k]) +\
                                          str(list(string.uppercase)[w])
    j = j + 1

# Create file for tracking the progress
trackfilename = working_dir + "RedLeakMultiObs.txt"
trackfile = open(trackfilename, 'w')

trackfile.write("Starting process at %s \n" %(start_time_hr))
trackfile.close()

# Structure holding the final cubes for every pair [obsid,camera]
observations_dict = {}
finalCubeList = []

# Run pipeline over obs
for i in range(len(obsids.keys())):
    camera = 'red'
    # Next, get the data
    observations_dict["obs_{0}".format(obsids.keys()[i])] = getObservation(obsids.keys()[i],
                                                                           useHsa = 1)

    obs = getObservation(obsids.keys()[i], useHsa = 1)

    # print outs to keep you up to date with progress
    actual_time = time.time()
    actual_time_hr = datetime.datetime.fromtimestamp(actual_time)
    actual_time_hr = str(actual_time_hr)
    
    trackfile = open(trackfilename, 'a')
    trackfile.write("Processing observation " + str(obsids.keys()[i]) +
                    " with camera " + camera + " at " + str(actual_time_hr) +
                    "\n")
    trackfile.close()

    runPacsSpg(cameraList=[camera],
               obsIn=observations_dict["obs_{0}".format(obsids.keys()[i])])
    
    name = 'obs_' + str(obsid)
    saveObservation(observations_dict["obs_{0}".format(obsids.keys()[i])],
                    poolLocation = pool_dir, poolName = name)

    duration = time.time() - actual_time
    duration_m = int(duration/60)
    duration_s = duration - duration_m*60

    trackfile = open(trackfilename, 'a')
    trackfile.write('End ' + str(obsids.keys()[i]) + " " + camera +
                    ' Duration: ' + str(duration_m) + ' m ' +
                    str(duration_s) + ' s ' + '\n')
    trackfile.close()

    """
    # if there is a previous version upgrade version
    version='v4'
    obsid=1342246381
    sey=str(obsid) + "_case1"
    obs_case1=getObservation(obsid=obsid, poolLocation=str(pool_dir), 
                             poolName=sey)
    sey=str(obsid) + "_case2"
    obs_case2=getObservation(obsid=obsid, poolLocation=str(pool_dir),
                             poolName=sey)
    sey=str(obsid) + "_case3"
    obs_case3=getObservation(obsid=obsid, poolLocation=str(pool_dir),
                             poolName=sey)
    sey=str(obsid) + "_case4"
    obs_case4=getObservation(obsid=obsid, poolLocation=str(pool_dir),
                             poolName=sey)
    sey=str(obsid) + "_case5"
    obs_case5=getObservation(obsid=obsid, poolLocation=str(pool_dir),
                             poolName=sey)
    sey=str(obsid) + "_case6"
    obs_case6=getObservation(obsid=obsid, poolLocation=str(pool_dir),
                             poolName=sey)

    slicedRC_t1 = obs_case1.level2.red.rcube.product
    slicedRC_t2 = obs_case2.level2.red.rcube.product
    slicedRC_t3 = obs_case3.level2.red.rcube.product
    slicedRC_t4 = obs_case4.level2.red.rcube.product
    slicedRC_t5 = obs_case5.level2.red.rcube.product
    slicedRC_t6 = obs_case6.level2.red.rcube.product

    # Get the rebinned cubes of each test case
    cube_t1 = slicedRC_t1.get(0)
    cube_t2 = slicedRC_t2.get(0)
    cube_t3 = slicedRC_t3.get(0)
    cube_t4 = slicedRC_t4.get(0)
    cube_t5 = slicedRC_t5.get(0)
    cube_t6 = slicedRC_t6.get(0)

    # Central spaxel
    spaxX=2
    spaxY=2
    # Get the wavelengths for each case
    wve_t1 = cube_t1.getWave()
    wve_t2 = cube_t2.getWave()
    wve_t3 = cube_t3.getWave()
    wve_t4 = cube_t4.getWave()
    wve_t5 = cube_t5.getWave()
    wve_t6 = cube_t6.getWave()
    flx_t1 = cube_t1.getFlux()[:, spaxX, spaxY]
    flx_t2 = cube_t2.getFlux()[:, spaxX, spaxY]
    flx_t3 = cube_t3.getFlux()[:, spaxX, spaxY]
    flx_t4 = cube_t4.getFlux()[:, spaxX, spaxY]
    flx_t5 = cube_t5.getFlux()[:, spaxX, spaxY]
    flx_t6 = cube_t6.getFlux()[:, spaxX, spaxY]

    # Main plot of all test cases
    main_plot = PlotXY(titleText="All tests cases")
    main_plot.addLayer(LayerXY(wve_t1, flx_t1, line=1,
                               name="no flatfielding selected",
                               xrange=[150, 205]))
    main_plot.addLayer(LayerXY(wve_t2, flx_t2, line=1,
                               name="flatfielding range selecting range [198, 203]"))
    main_plot.addLayer(LayerXY(wve_t3, flx_t3, line=1,
                               name="flatfielding line selecting range [198, 203]"))
    main_plot.addLayer(LayerXY(wve_t4, flx_t4, line=1,
                               name="flatfielding line selecting range [199, 201]"))
    main_plot.addLayer(LayerXY(wve_t5, flx_t5, line=1,
                               name="flatfielding line selecting range [161, 163]"))
    main_plot.addLayer(LayerXY(wve_t6, flx_t6, line=1, 
                               name="flatfielding range whole range [55, 220]"))
    main_plot.legend.visible=1
    main_plot.xaxis.tick.gridLines=1
    main_plot.yaxis.tick.gridLines=1
    main_plot.saveAsPNG(str(plot_dir) + "FFComparison_" + str(obsid) +
                        "_200um_" + str(version) + ".png")

    # No flatfielding against flatfielding range selecting range [198, 203]
    test_plot_1 = PlotXY(titleText="NoFF vs. FFRangeSelecting [198, 203]")
    test_plot_1.addLayer(LayerXY(wve_t1, flx_t1, line=1,
                                 name="no flatfielding selected",
                                 xrange=[196,205]))
    test_plot_1.addLayer(LayerXY(wve_t2, flx_t2, line=1,
                                 name="flatfielding range selecting range [198, 203]"))
    test_plot_1.legend.visible=1
    test_plot_1.xaxis.tick.gridLines=1
    test_plot_1.yaxis.tick.gridLines=1
    test_plot_1.saveAsPNG(str(plot_dir) + "NoFF_vs_FFRangeSelect[198_203]_" +
                          str(obsid) + "_200um_" + str(version) + ".png")

    # No flatfielding against flatfielding line selecting range [198, 203]
    test_plot_2 = PlotXY(titleText="NoFF vs. FFLineSelecting [198, 203]")
    test_plot_2.addLayer(LayerXY(wve_t1, flx_t1, line=1,
                                 name="no flatfielding selected",
                                 xrange=[196, 205]))
    test_plot_2.addLayer(LayerXY(wve_t3, flx_t3, line=1,
                                 name="flatfielding line selecting range [198, 203]"))
    test_plot_2.legend.visible=1
    test_plot_2.xaxis.tick.gridLines=1
    test_plot_2.yaxis.tick.gridLines=1
    test_plot_2.saveAsPNG(str(plot_dir) + "NoFF_vs_FFLineSelect[198_203]_" +
                          str(obsid) + "_200um_" + str(version) + ".png")

    # No flatfielding against flatfielding line selecting range [199, 201]
    test_plot_3 = PlotXY(titleText="NoFF vs. FFLineSelectingRange [199, 201]")
    test_plot_3.addLayer(LayerXY(wve_t1, flx_t1, line=1,
                                 name="no flatfielding selected",
                                 xrange=[196, 205]))
    test_plot_3.addLayer(LayerXY(wve_t4, flx_t4, line=1,
                                 name="flatfielding line selecting range [199, 201]"))
    test_plot_3.legend.visible=1
    test_plot_3.xaxis.tick.gridLines=1
    test_plot_3.yaxis.tick.gridLines=1
    test_plot_3.saveAsPNG(str(plot_dir) + "NoFF_vs_FFLineSelect[199_201]_" +
                          str(obsid) + "_200um_" + str(version) + ".png")

    # No flatfielding against flatfielding range whole range
    test_plot_4 = PlotXY(titleText="NoFF vs. FFRangeWholeRange [55, 220]")
    test_plot_4.addLayer(LayerXY(wve_t1, flx_t1, line=1,
                                 name="no flatfielding selected",
                                 xrange=[196, 205]))
    test_plot_4.addLayer(LayerXY(wve_t6, flx_t6, line=1, 
                                 name="flatfielding range whole range [55, 220]"))
    test_plot_4.legend.visible=1
    test_plot_4.xaxis.tick.gridLines=1
    test_plot_4.yaxis.tick.gridLines=1
    test_plot_4.saveAsPNG(str(plot_dir) + "NoFF_vs_FFRangeSelect[55_220]_" +
                          str(obsid) + "_200um_" + str(version) + ".png")

    # Flatfielding range selecting [198, 203] against flatfielding line selecting [198, 203]
    test_plot_5 = PlotXY(titleText="FFRangeSelecting [198, 203] vs. FFLineSelecting [198, 203]")
    test_plot_5.addLayer(LayerXY(wve_t2, flx_t2, line=1,
                                 name="flatfielding range selecting range [198, 203]",
                                 xrange=[196, 205]))
    test_plot_5.addLayer(LayerXY(wve_t3, flx_t3, line=1,
                                 name="flatfielding line selecting range [198, 203]"))
    test_plot_5.legend.visible=1
    test_plot_5.xaxis.tick.gridLines=1
    test_plot_5.yaxis.tick.gridLines=1
    test_plot_5.saveAsPNG(str(plot_dir) + 
                          "FFRangeSelect[198_203]_vs_FFLineSelect[198_203]_" +
                          str(obsid) + "_200um_" + str(version) + "v3.png")

    # Flatfielding range selecting [198, 203] against flatfielding line selecting range [199, 201]
    test_plot_6 = PlotXY(titleText = "FFRangeSelecting [198, 203] vs. FFLineSelecting [199, 201]")
    test_plot_6.addLayer(LayerXY(wve_t2, flx_t2, line=1,
                                 name="flatfielding range selecting range [198, 203]",
                                 xrange=[196, 205]))
    test_plot_6.addLayer(LayerXY(wve_t4, flx_t4, line=1,
                                 name="flatfielding line selecting range [199, 201]"))
    test_plot_6.legend.visible=1
    test_plot_6.xaxis.tick.gridLines=1
    test_plot_6.yaxis.tick.gridLines=1
    test_plot_6.saveAsPNG(str(plot_dir) +
                          "FFRangeSelect[198_203]_vs_FFLineSelect[199_201]_" +
                          str(obsid) + "_200um_" + str(version) + ".png")

    # Flatfielding range selecting [198, 203] against flatfielnding range selecting [55, 220]
    test_plot_7 = PlotXY(titleText="FFRangeSelecting [198, 203] vs. FFRangeSelecting [55, 220]")
    test_plot_7.addLayer(LayerXY(wve_t2, flx_t2, line=1,
                                name="flatfielding range selecting range [198, 203]", 
                                xrange=[196, 205]))
    test_plot_7.addLayer(LayerXY(wve_t6, flx_t6, line=1, 
                                 name="flatfielding range whole range [55, 220]"))
    test_plot_7.legend.visible=1
    test_plot_7.xaxis.tick.gridLines=1
    test_plot_7.yaxis.tick.gridLines=1
    test_plot_7.saveAsPNG(str(plot_dir) +
                          "FFRangeSelect[198_203]_vs_FFRangeSelect[55_220]_" +
                          str(obsid) + "_200um_" + str(version) + ".png")

    # Flatfielding line selecting [198, 203] against flatfielding line selecting [199, 201]
    test_plot_8 = PlotXY(titleText="FFLineSelecting [198, 203] against FFLineSelecting[199, 201]")
    test_plot_8.addLayer(LayerXY(wve_t3, flx_t3, line=1,
                                 name="flatfielding line selecting range [198, 203]",
                                 xrange=[196, 205]))
    test_plot_8.addLayer(LayerXY(wve_t4, flx_t4, line=1,
                                 name="flatfielding line selecting range [199, 201]"))
    test_plot_8.legend.visible=1
    test_plot_8.xaxis.tick.gridLines=1
    test_plot_8.yaxis.tick.gridLines=1
    test_plot_8.saveAsPNG(str(plot_dir) +
                          "FFLineSelect[198_203]_vs_FFLineSelect[199_201]_" +
                          str(obsid) + "_200um_" + str(version) + ".png")

    # Main plot of all test cases
    test_plot_9 = PlotXY(titleText="FFLineSelecting [198, 203] against FFRangeSelecting [55, 220]")
    test_plot_9.addLayer(LayerXY(wve_t3, flx_t3, line=1,
                                 name="flatfielding line selecting range [198, 203]",
                                 xrange=[196, 205]))
    test_plot_9.addLayer(LayerXY(wve_t6, flx_t6, line=1, 
                                 name="flatfielding range whole range [55, 220]"))
    test_plot_9.legend.visible=1
    test_plot_9.xaxis.tick.gridLines=1
    test_plot_9.yaxis.tick.gridLines=1
    test_plot_9.saveAsPNG(str(plot_dir) +
                          "FFLineSelect[198_203]_vs_FFRangeSelect[55_220]_" +
                          str(obsid) + "_200um_" + str(version) + ".png")

    test_plot_10 = PlotXY(titleText="FFLineSelecting [199, 201] against FFRangeSelecting [55, 220]")
    test_plot_10.addLayer(LayerXY(wve_t4, flx_t4, line=1,
                                  name="flatfielding line selecting range [199, 201]",
                                  xrange=[196, 205]))
    test_plot_10.addLayer(LayerXY(wve_t6, flx_t6, line=1, 
                                  name="flatfielding range whole range [55, 220]"))
    test_plot_10.legend.visible=1
    test_plot_10.xaxis.tick.gridLines=1
    test_plot_10.yaxis.tick.gridLines=1
    test_plot_10.saveAsPNG(str(plot_dir) +
                           "FFLineSelect[199_201]_vs_FFRangeSelect[55_220]_" +
                           str(obsid) + "_200um_" + str(version) + ".png")

    test_plot_11 = PlotXY(titleText="FFLineSelecting [161, 163] against FFRangeSelecting [55, 220]")
    test_plot_11.addLayer(LayerXY(wve_t5, flx_t5, line=1,
                                  name="flatfielding line selecting range [161, 163]",
                                  xrange=[196, 205]))
    test_plot_11.addLayer(LayerXY(wve_t6, flx_t6, line=1, 
                                  name="flatfielding range whole range [55, 220]"))
    test_plot_11.legend.visible=1
    test_plot_11.xaxis.tick.gridLines=1
    test_plot_11.yaxis.tick.gridLines=1
    test_plot_11.saveAsPNG(str(plot_dir) +
                           "FFLineSelect[161_163]_vs_FFRangeSelect[55_220]_" +
                           str(obsid) + "_200um_" + str(version) + ".png")

    # As Katrina requested
    test_plot_11 = PlotXY(titleText = "All tests cases without no FF test - Test range")
    test_plot_11.addLayer(LayerXY(wve_t2, flx_t2, line=1,
                                  name="flatfielding range selecting range [198, 203]",
                                  xrange=[196, 205]))
    test_plot_11.addLayer(LayerXY(wve_t3, flx_t3, line=1,
                                  name="flatfielding line selecting range [198, 203]"))
    test_plot_11.addLayer(LayerXY(wve_t6, flx_t6, line=1, 
                                  name="flatfielding range whole range [55, 220]"))
    test_plot_11.legend.visible=1
    test_plot_11.xaxis.tick.gridLines=1
    test_plot_11.yaxis.tick.gridLines=1
    test_plot_11.saveAsPNG(str(plot_dir) + "FFComparison_Katrina_" + str(obsid) +
                           "_200um_" + str(version) + ".png")

    desviation_list=Double1d()
    if (len(flx_t2) == len(flx_t3)):
        for i in range(len(flx_t2)):
            result = flx_t3[i] - flx_t2[i]
            desviation_list.append(result)

    test_plot_12 = PlotXY(titleText = "Flatfielding line minus flatfielding range")
    test_plot_12.addLayer(LayerXY(wve_t3, desviation_list, line=1,
                                  name="Desviation"))
    test_plot_12.legend.visible=1
    test_plot_12.xaxis.tick.gridLines=1
    test_plot_12.yaxis.tick.gridLines=1
    test_plot_11.saveAsPNG(str(plot_dir) + "FFComparison_Katrina_" + str(obsid) +
                           "_200um_v3.png")

    # Main plot of all test cases
    test_plot_13 = PlotXY(titleText="Flatfielding methods [199-201] wavelength")
    test_plot_13.addLayer(LayerXY(wve_t2, flx_t2, line=1,
                                  name="flatfielding range selecting range [198, 203]",
                                  xrange=[199, 201]))
    test_plot_13.addLayer(LayerXY(wve_t3, flx_t3, line=1,
                                  name="flatfielding line selecting range [198, 203]"))
    test_plot_13.addLayer(LayerXY(wve_t6, flx_t6, line=1, 
                                  name="flatfielding range whole range [55, 220]"))
    test_plot_13.legend.visible=1
    test_plot_13.xaxis.tick.gridLines=1
    test_plot_13.yaxis.tick.gridLines=1
    test_plot_13.ytitle='Flux [Jy]'
    test_plot_13.xtitle='Wavelength [um]'

    test_plot_13.saveAsPNG(str(plot_dir) + "FFComparison_" + str(obsid) +
                           "_200um_" + str(version) = ".png")
    """

duration = time.time() - start_time
duration_m = int(duration/60)
duration_s = duration - duration_m*60

trackfile = open(trackfilename, 'a')
trackfile.write("END Total Duration: " +
                str(duration_m) + ' m ' + str(duration_s) + ' s ' + "\n")
trackfile.close()
