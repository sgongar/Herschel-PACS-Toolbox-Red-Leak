from os import getenv, path, mkdir
from time import time
from string import uppercase
from shutil import rmtree

obs_ok = ['1342199235', '1342211842', '1342220751', '1342231295', '1342238351',
          '1342239373', '1342246641', '1342209717', '1342220931', '1342225820',
          '1342225821', '1342228538', '1342229752', '1342250904', '1342238905',
          '1342238906', '1342252090', '1342252092', '1342253738', '1342254274',
          '1342254275', '1342208926', '1342212512']

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
trackfilename = working_dir + "RedLeakMultiObs_4.txt"
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
    for i in range(len(obs_ok)):
        if obs_ok[i] in obs_list:
            obs_list.remove(obs_ok[i])

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

        """
        try:
            rmtree(pool_dir + "Export/" + obs_number)
        except Exception as e:
            save_exception(e)
            print 'An exception was raised while removing struct dir', e

        try:
            rmtree(pool_dir + obs_number)
        except Exception as e:
            save_exception(e)
            print 'An exception was raised while removing standard dir', e
        """
    duration = time() - start_total_time
    duration_m = int(duration/60)
    duration_s = duration - duration_m*60

    save_message('END Total Duration: ' + str(duration_m) + ' m ' +\
                 str(duration_s) + ' s ' +'\n', 'a', trackfilename)

    return True


if __name__ == "__main__":
    # Loads external functions
    execfile(massive_aux)
    # Runs the massive function, asks for a csv file name
    try:
        csv_file = raw_input("Enter csv file (default: obs_ids.csv):")
        if csv_file == '':
            csv_file = 'obs_ids.csv'
        run_massive(csv_file)
    except Exception as e:
        save_exception(e)
        print 'An exception was raised'
