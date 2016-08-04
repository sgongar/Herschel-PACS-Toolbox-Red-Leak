import os
import time
import datetime
import csv
import string
import shutil

home_dir = os.getenv("HOME")
working_dir = str(home_dir) + '/hcss/workspace/Red-leak/'
pool_dir = str(working_dir) + 'pools/'
zips_dir = str(pool_dir) + 'zips/'
plot_dir = str(working_dir) + 'plots/'
csv_obs = str(working_dir) + 'obs_ids_1.csv'

obsid = 1342187020
obs_case1 = getObservation(obsid=obsid, poolLocation=str(pool_dir), poolName='test')

obs_case2 = getObservation(obsid=obsid, useHsa = 1)

slicedRC_t1 = obs_case1.level2.red.rcube.product
slicedRC_t2 = obs_case2.level2.blue.rcube.product

# Get the rebinned cubes of each test case
cube_t1 = slicedRC_t1.get(0)
cube_t2 = slicedRC_t2.get(0)

# Central spaxel
spaxX=2
spaxY=2
# Get the wavelengths for each case
wve_t1 = cube_t1.getWave()
wve_t2 = cube_t2.getWave()

flx_t1 = cube_t1.getFlux()[:, spaxX, spaxY]
flx_t2 = cube_t2.getFlux()[:, spaxX, spaxY]

main_plot = PlotXY(titleText="All tests cases")
main_plot.addLayer(LayerXY(wve_t1, flx_t1, line=1,
                           name="no flatfielding selected"))
main_plot.addLayer(LayerXY(wve_t2, flx_t2, line=1,
                           name="flatfielding range selecting range [198, 203]"))
main_plot.legend.visible=1
main_plot.xaxis.tick.gridLines=1
main_plot.yaxis.tick.gridLines=1