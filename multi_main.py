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

multiObs = 1
save_obs = False

obsids = {}
obsids[1342246381] = "SEDA"
"""
# Line 290

obsids = [1342186305, 1342186798, 1342186797, 1342187020, 1342188034,\
          1342188941, 1342189072, 1342188526, 1342189411, 1342187779,\
          1342199407, 1342199420, 1342199415, 1342199238, 1342199748,\
          1342199746, 1342200158, 1342200155, 1342189410, 1342206850,\
          1342214636, 1342214673, 1342220743, 1342220982, 1342220599,\
          1342221384, 1342221386, 1342220751, 1342221382, 1342221362,\
          1342221364, 1342222076, 1342222100, 1342222084, 1342222194,\
          1342222251, 1342222248, 1342223119, 1342222250, 1342223129,\
          1342222765, 1342223104, 1342223124, 1342223106, 1342223102,\
          1342223732, 1342223748, 1342223718, 1342223743, 1342223720,\
          1342223779, 1342224399, 1342224397, 1342224395, 1342223805,\
          1342228534, 1342231427, 1342232601, 1342237582, 1342232561,\
          1342239376, 1342245246, 1342247009, 1342246394, 1342247784,\
          1342247817, 1342249386, 1342249385, 1342249393, 1342249387,\
          1342249392, 1342249390, 1342249391, 1342249384, 1342250904,\
          1342246641, 1342265446, 1342265445, 1342265672, 1342265684,\
          1342265682, 1342265673, 1342265683, 1342265689, 1342265686,\
          1342265674, 1342265676, 1342265681, 1342265675, 1342265685,\
          1342265690, 1342265670, 1342265692, 1342265677, 1342265671,\
          1342265687, 1342265680, 1342265688, 1342265691, 1342265698,\
          1342265697, 1342264210, 1342264211, 1342265700, 1342264217,\
          1342264204, 1342264203, 1342265699, 1342264200, 1342264218,\
          1342264213, 1342264209, 1342264208, 1342264212, 1342264202,\
          1342264206, 1342264214, 1342264201, 1342264216, 1342264205,\
          1342264207, 1342264215, 1342264220, 1342264219, 1342264237,\
          1342264238, 1342265929, 1342265923, 1342265921, 1342265937,\
          1342265952, 1342265928, 1342265934, 1342265924, 1342265938,\
          1342265930, 1342265931, 1342265936, 1342265922, 1342265940,\
          1342265925, 1342265933, 1342265939, 1342265935, 1342265932,\
          1342265927, 1342267182, 1342267177, 1342267178, 1342267185,\
          1342267186, 1342267184, 1342267183, 1342267179, 1342267626,\
          1342267875, 1342267858, 1342267844, 1342267879, 1342267842,\
          1342267881, 1342267843, 1342267859, 1342267874, 1342267870,\
          1342267880, 1342267861, 1342267878, 1342267877, 1342267860,\
          1342270680, 1342270681, 1342209709, 1342209717, 1342229752,\
          1342208907, 1342267869, 1342189612, 1342198300, 1342202589,\
          1342203446, 1342208901, 1342208926, 1342209711, 1342209707,\
          1342210384, 1342210399, 1342210824, 1342210827, 1342210834,\
          1342211537, 1342211693, 1342211842, 1342212220, 1342212600,\
          1342212790, 1342213146, 1342213911, 1342213925, 1342214220,\
          1342225586, 1342225580, 1342225849, 1342225993, 1342234063,\
          1342235692, 1342236271, 1342236272, 1342250999, 1342251177,\
          1342251176, 1342252090, 1342252092, 1342253738, 1342254219,\
          1342254218, 1342254216, 1342254217, 1342254257, 1342254255,\
          1342254256, 1342254275, 1342254274, 1342254280, 1342254298,\
          1342254297, 1342254299, 1342254300, 1342254610, 1342254611,\
          1342254608, 1342254609, 1342254607, 1342254606, 1342254767,\
          1342254620, 1342254616, 1342254617, 1342254618, 1342254619,\
          1342254612, 1342254768, 1342254770, 1342254769, 1342254932,\
          1342254931, 1342254937, 1342256254, 1342256255, 1342256256,\
          1342256248, 1342256766, 1342256763, 1342256477, 1342256784,\
          1342256783, 1342256928, 1342257275, 1342257686, 1342257793,\
          1342259608, 1342262028, 1342262540, 1342262544, 1342262936,\
          1342262945, 1342262958, 1342262967, 1342262981, 1342262976,\
          1342263462, 1342263465, 1342263463, 1342263496, 1342266972,\
          1342266971, 1342266969, 1342266970, 1342266968, 1342266964,\
          1342266922, 1342266976, 1342266975, 1342266974, 1342266973,\
          1342266977, 1342266978, 1342266979, 1342266982, 1342266981]

# Range 23
obsids = [1342213138, 1342213762, 1342215667, 1342230909, 1342230907,\
          1342230906, 1342230908, 1342238514, 1342238351, 1342239373,\
          1342245393, 1342245646, 1342253746, 1342218568, 1342253747,\
          1342253745, 1342254935, 1342254953, 1342256261, 1342257285,\
          1342257798, 1342259561, 1342262769]
"""

start_time = time.time()
start_time_hr = datetime.datetime.fromtimestamp(start_time)
start_time_hr = str(start_time_hr)

home_dir = os.getenv("HOME")
working_dir = str(home_dir) + '/hcss/workspace/Red-leak/'
pool_dir = str(working_dir) + 'pools/'
plot_dir = str(working_dir) + 'plots/'

if (not os.path.exists(working_dir)):
    os.mkdir(working_dir)
if (not os.path.exists(pool_dir)):
    os.mkdir(pool_dir)
if (not os.path.exists(plot_dir)):
    os.mkdir(plot_dir)

# Create file for tracking the progress
trackfilename = working_dir + "RedLeakMultiObs.txt"
trackfile = open(trackfilename, 'w')

trackfile.write("Starting process at %s \n" %(start_time_hr))
trackfile.close()

# Structure holding the final cubes for every pair [obsid,camera]
finalCubeList = []
observations_dict = {}

# Run pipeline over obs
for i in range(len(obsids.keys())):
    camera = 'red'
    # Next, get the data
    observations_dict["obs_{0}".format(obsids.keys()[i])]= getObservation(obsids.keys()[i],
                                                                          useHsa = 1)
    # print outs to keep you up to date with progress
    actual_time = time.time()
    actual_time_hr = datetime.datetime.fromtimestamp(actual_time)
    actual_time_hr = str(actual_time_hr)
    
    trackfile = open(trackfilename, 'a')
    trackfile.write("Processing observation " + str(obsids.keys()[i]) +
                    " with camera " + camera + " at " + str(actual_time_hr) +
                    "\n")
    trackfile.close()
    """
    runPacsPSG
    saveObser
    """
    execfile(str(working_dir) + 'L05_Frames.py')
    execfile(str(working_dir) + 'L1_ChopNod.py')
    execfile(str(working_dir) + 'L2_ChopNod.py')
 
    duration = time.time() - actual_time
    duration_m = int(duration/60)
    duration_s = duration - duration_m*60

    trackfile = open(trackfilename, 'a')
    trackfile.write('End ' + str(obsids.keys()[i]) + " " + camera +
                    ' Duration: ' + str(duration_m) + ' m ' +
                    str(duration_s) + ' s ' + '\n')
    trackfile.close()

    version='v4'
    obsid=1342246381
    if int(obsids.keys()[i]) is int(obsid):
        print "Everything is cool"
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
    sey=str(obsid) + "_casen"
    obs_casen=getObservation(obsid=obsid, poolLocation=str(pool_dir),
                             poolName=sey)

    slicedRC_t1 = obs_case1.level2.red.rcube.product
    slicedRC_t2 = obs_case2.level2.red.rcube.product
    slicedRC_t3 = obs_case3.level2.red.rcube.product
    slicedRC_t4 = obs_case4.level2.red.rcube.product
    slicedRC_n = obs_casen.level2.red.rcube.product

    # Get the rebinned cubes of each test case
    cube_t1 = slicedRC_t1.get(0)
    cube_t2 = slicedRC_t2.get(0)
    cube_t3 = slicedRC_t3.get(0)
    cube_t4 = slicedRC_t4.get(0)
    cube_n = slicedRC_n.get(0)

    # Central spaxel
    spaxX=2
    spaxY=2
    # Get the wavelengths for each case
    wve_t1 = cube_t1.getWave()
    wve_t2 = cube_t2.getWave()
    wve_t3 = cube_t3.getWave()
    wve_t4 = cube_t4.getWave()
    wve_n = cube_n.getWave()
    flx_t1 = cube_t1.getFlux()[:, spaxX, spaxY]
    flx_t2 = cube_t2.getFlux()[:, spaxX, spaxY]
    flx_t3 = cube_t3.getFlux()[:, spaxX, spaxY]
    flx_t4 = cube_t4.getFlux()[:, spaxX, spaxY]
    flx_n = cube_n.getFlux()[:, spaxX, spaxY]

    # Main plot of all test cases
    main_plot = PlotXY(titleText="All tests cases")
    main_plot.addLayer(LayerXY(wve_t1, flx_t1, line=1,
                               name="no flatfielding selected",
                               xrange=[196, 205]))
    main_plot.addLayer(LayerXY(wve_t2, flx_t2, line=1,
                               name="flatfielding range selecting range [198, 203]"))
    main_plot.addLayer(LayerXY(wve_t3, flx_t3, line=1,
                               name="flatfielding line selecting range [198, 203]"))
    main_plot.addLayer(LayerXY(wve_t4, flx_t4, line=1,
                               name="flatfielding line selecting range [199, 201]"))
    main_plot.addLayer(LayerXY(wve_n, flx_n, line=1, 
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
    test_plot_4.addLayer(LayerXY(wve_n, flx_n, line=1, 
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
    test_plot_7.addLayer(LayerXY(wve_n, flx_n, line=1, 
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
    test_plot_9.addLayer(LayerXY(wve_n, flx_n, line=1, 
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
    test_plot_10.addLayer(LayerXY(wve_n, flx_n, line=1, 
                                  name="flatfielding range whole range [55, 220]"))
    test_plot_10.legend.visible=1
    test_plot_10.xaxis.tick.gridLines=1
    test_plot_10.yaxis.tick.gridLines=1
    test_plot_10.saveAsPNG(str(plot_dir) +
                           "FFLineSelect[199_201]_vs_FFRangeSelect[55_220]_" +
                           str(obsid) + "_200um_" + str(version) + ".png")

    # As Katrina requested
    test_plot_11 = PlotXY(titleText = "All tests cases without no FF test - Test range")
    test_plot_11.addLayer(LayerXY(wve_t2, flx_t2, line=1,
                                  name="flatfielding range selecting range [198, 203]",
                                  xrange=[196, 205]))
    test_plot_11.addLayer(LayerXY(wve_t3, flx_t3, line=1,
                                  name="flatfielding line selecting range [198, 203]"))
    test_plot_11.addLayer(LayerXY(wve_n, flx_n, line=1, 
                                  name="flatfielding range whole range [55, 220]"))
    test_plot_11.legend.visible=1
    test_plot_11.xaxis.tick.gridLines=1
    test_plot_11.yaxis.tick.gridLines=1
    test_plot_11.saveAsPNG(str(plot_dir) + "FFComparison_Katrina_" + str(obsid) +
                           "_200um_" + str(version) + ".png")

    """
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
    test_plot_13.addLayer(LayerXY(wve_n, flx_n, line=1, 
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
