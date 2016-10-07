from os import getenv, path, mkdir
from time import time
from string import uppercase

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


# Load directories
# In our case we assumed that ...
home_dir = str(getenv("HOME"))
working_dir = home_dir + '/hcss/workspace/Red_Leak/'
pool_dir = working_dir + 'pools/'
obs_dir = working_dir + 'obs_ids/'
trackfilename = working_dir + "RedLeakMultiObs.txt"
massive_aux = working_dir + "massive/massive_aux.py"

save_obs = False
enable_log = False # useful?

def run_massive(csv_file):
    """
    
    @param csv_file: observations csv file to be analysed
    @return True: return True if everything goes alright 
    """
    if (not path.exists(working_dir)):
        mkdir(working_dir)
    if (not path.exists(pool_dir)):
        mkdir(pool_dir)

    # Create file for tracking the progress
    save_message("Starting process at %s \n" %(get_formatted_time()), 
                 'w', trackfilename)

    obs_list = populate_obs(obs_dir + csv_file)
    observations_dict = create_dictionary(obs_list)
    finalCubeList = []
    
    start_total_time = time()
    # TODO try-except raising all the problems to external file
    # Run pipeline over obs
    for i in range(len(obs_list)):
        start_obs_time = time()
        camera = 'red'

        obs_number = observations_dict.keys()[i]
        observations_dict[obs_number] = getObservation(obs_number, useHsa=1)

        save_message("Processing observation " + str(obs_number) +\
                     " with " + camera + " camera " + " at " +\
                     str(get_formatted_time()) + "\n", 'a', trackfilename)

        runPacsSpg(cameraList=[camera], obsIn=observations_dict[obs_number])

        try:
            print 'Saving observation: ', obs_number
            saveObservation(observations_dict[obs_number],
                            poolLocation=pool_dir, poolName=obs_number)
            print 'Observation saved'
        except Exception as e:
            save_exception(e)
            print 'An exception was raised during saving process ', e
    
        try:
            print 'Exporting observation: ', obs_number
            exportObservation(pool=PoolManager.getPool(obs_number), 
                              urn='urn:' + obs_number +\
                                  ':herschel.ia.obs.ObservationContext:0',
                              dirout=pool_dir + "Export/" + obs_number)
        except Exception as e:
            save_exception(e)
            print 'An exception was raised during exporting process ', e

        try:
            print 'Compressing file for observation: ', obs_number
            compress(inputpath=pool_dir + "Export/" + obs_number,
                     archive=pool_dir + obs_number + ".tgz", compression="TGZ")
        
        except Exception as e:
            save_exception(e)
            print 'An exception was raised during compression process', e

        duration = time() - start_obs_time
        duration_m = int(duration/60)
        duration_s = duration - duration_m*60

        camera = 'red'
        save_message('End ' + obs_number + " " + camera + ' Duration: ' +\
                     str(duration_m) + ' m ' + str(duration_s) + ' s ' +\
                     '\n', 'a', trackfilename)

    duration = time() - start_total_time
    duration_m = int(duration/60)
    duration_s = duration - duration_m*60

    save_message('END Total Duration: ' + str(duration_m) + ' m ' +\
                 str(duration_s) + ' s ' +'\n', 'a', trackfilename)

    return True


if __name__ == "__main__":
    execfile(massive_aux)
    try:
        csv_file = raw_input("Enter csv file (default: obs_ids.csv):")
        if csv_file == '':
            csv_file = 'obs_ids.csv'
        run_massive(csv_file)
    except Exception as e:
        save_exception(e)
        print 'An exception was raised'
