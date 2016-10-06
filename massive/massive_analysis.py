from os import getenv, path, mkdir
from time import time
from datetime import datetime
from csv import reader
from string import uppercase
from massive_aux import get_formatted_time, save_exception
from massive_aux import create_dictionary, populate_obs

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

# Load directories
# In our case we assumed that ...
home_dir = getenv("HOME")
working_dir = str(home_dir) + '/hcss/workspace/Red-leak/'
pool_dir = str(working_dir) + 'pools/'
zips_dir = str(pool_dir) + 'zips/'
csv_obs = str(working_dir) + 'obs_ids.csv'

save_obs = False

run_massive():
    start_time = time.time()
    start_time_hr = datetime.datetime.fromtimestamp(start_time)
    start_time_hr = str(start_time_hr)

    if (not path.exists(working_dir)):
        mkdir(working_dir)
    if (not path.exists(pool_dir)):
        mkdir(pool_dir)
    if (not path.exists(zips_dir)):
        mkdir(zips_dir)

    obs_list = populate_obs(csv_obs)

    # Create file for tracking the progress
    trackfilename = working_dir + "RedLeakMultiObs.txt"
    trackfile = open(trackfilename, 'w')
    trackfile.write("Starting process at %s \n" %(get_formatted_time()))
    trackfile.close()

    # Structure holding the final cubes for every pair [obsid,camera]
    observations_dictionary = create_dictionary(obs_list)
    finalCubeList = []

    # TODO try-except raising all the problems to external file
    # Run pipeline over obs
    for i in range(len(obs_list)):
        camera = 'red'

        obs_number = observations_dict.keys()[i]
        observations_dictionary[obs_number] = getObservation(obs_number,
                                                             useHsa=1)

        trackfile = open(trackfilename, 'a')
        trackfile.write("Processing observation " +
                        str(obs_number) + " with camera " + camera +
                        " at " + str(get_formatted_time()) + "\n")
        trackfile.close()

        runPacsSpg(cameraList=[camera],
                   obsIn=observations_dictionary[obs_number])

        name = 'obs_' + str(observations_dict.keys()[i])

        try:
            print "Saving observation: ", obs_number
            saveObservation(observations_dictionary[obs_number],
                            poolLocation=pool_dir, poolName=name)
            print "Observation saved"
        except Exception as e:
            save_exception(e)
            print "An exception was raised during saving process ", e
    
        try:
            print "Exporting observation: ", obs_number
            exportObservation(pool=PoolManager.getPool(obs_number), 
                              urn=obs_number + ":herschel.ia.obs.ObservationContext:0",
                              dirout=pool_dir + "Export/" + obs_number)
        except Exception as e:
            save_exception(e)
            print "An exception was raised during exporting process ", e

        try:
            print "Compressing file for observation: ", obs_number
            compress(inputpath=pool_dir + "Export/" + obs_number,
                     archive=pool_dir + obs_number + ".tgz", compression="TGZ")
        
        except Exception as e:
            save_exception(e)
            print "An exception was raised during compression process", e

        duration = time.time() - actual_time
        duration_m = int(duration/60)
        duration_s = duration - duration_m*60

        camera = 'red'
        trackfile = open(trackfilename, 'a')
        trackfile.write('End ' + obs_number + " " + camera +
                        ' Duration: ' + str(duration_m) + ' m ' +
                    str(duration_s) + ' s ' + '\n')
        trackfile.close()

    duration = time.time() - start_time
    duration_m = int(duration/60)
    duration_s = duration - duration_m*60

    trackfile = open(trackfilename, 'a')
    trackfile.write("END Total Duration: " +
                str(duration_m) + ' m ' + str(duration_s) + ' s ' + "\n")
    trackfile.close()

if __name__ == "__main__":
    run_massive()
