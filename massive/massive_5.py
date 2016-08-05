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
import csv
import string
import shutil

home_dir = os.getenv("HOME")
working_dir = str(home_dir) + '/hcss/workspace/Red-leak/'
pool_dir = str(working_dir) + 'pools/'
tars_dir = str(pool_dir) + 'tars/'
plot_dir = str(working_dir) + 'plots/'
csv_obs = str(working_dir) + 'obs_ids/obs_ids_5.csv'

save_obs = True

start_time = time.time()
start_time_hr = datetime.datetime.fromtimestamp(start_time)
start_time_hr = str(start_time_hr)

if (not os.path.exists(working_dir)):
    os.mkdir(working_dir)
if (not os.path.exists(pool_dir)):
    os.mkdir(pool_dir)
if (not os.path.exists(tars_dir)):
    os.mkdir(tars_dir)
if (not os.path.exists(plot_dir)):
    os.mkdir(plot_dir)

# Populate list from csv file
obs_list = []
with open(str(csv_obs), 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        obs_list.append(row[1])

list_obs_tars = []
list_obs_tars = os.listdir(tars_dir)
new_list_obs_tars = []
final_list_obs_tars = []
obs_incomplete = []

for i in range(len(list_obs_tars)):
    new_list_obs_tars.append(list_obs_tars[i][4:])

for i in range(len(new_list_obs_tars)):
    final_list_obs_tars.append(new_list_obs_tars[i][:-4])

to_remove_list = []

for i in range(len(obs_list)):
    for j in range(len(final_list_obs_tars)):
        if obs_list[i] == final_list_obs_tars[j]:
            to_remove_list.append(obs_list[i])

for i in range(len(to_remove_list)):
    obs_list.remove(to_remove_list[i])

# Create dictionary from list
observations_dict = {}
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

    observations_dict[obs_list[i]] = 'SED' +\
                                     str(list(string.uppercase)[j]) +\
                                     str(list(string.uppercase)[k]) +\
                                     str(list(string.uppercase)[w])
    j = j + 1

# Create file for tracking the progress
trackfilename = working_dir + "RedLeakMultiObs_5.txt"
trackfile = open(trackfilename, 'w')
trackfile.write("Starting process at %s - Machine 5\n" %(start_time_hr))
trackfile.close()

# Structure holding the final cubes for every pair [obsid,camera]
observations_dictionary = {}
finalCubeList = []

# Run pipeline over obs
for i in range(len(obs_list)):
    # camera='camera'
    # Next, get the data
    observations_dictionary["obs_{0}".format(observations_dict.keys()[i])] = getObservation(observations_dict.keys()[i],
                                                                                            useHsa = 1)

    # print outs to keep you up to date with progress
    actual_time = time.time()
    actual_time_hr = datetime.datetime.fromtimestamp(actual_time)
    actual_time_hr = str(actual_time_hr)
    
    trackfile = open(trackfilename, 'a')
    trackfile.write("Processing observation " + str(observations_dict.keys()[i]) +
                    " at " + str(actual_time_hr) +
                    "\n")
    trackfile.close()

    try:
        runPacsSpg(obsIn=observations_dictionary["obs_{0}".format(observations_dict.keys()[i])])
        name = 'obs_' + str(observations_dict.keys()[i])
        saveObservation(observations_dictionary["obs_{0}".format(observations_dict.keys()[i])],
                        poolLocation=pool_dir, poolName=name)
    except:
        obs_incomplete.append(observations_dict.keys()[i])
        name = 'obs_incomplete' + str(observations_dict.keys()[i])
        saveObservation(observations_dictionary["obs_{0}".format(observations_dict.keys()[i])],
                        poolLocation=pool_dir, poolName=name)    


    try:
#        shutil.make_archive(str(pool_dir) + 'tars/' + str(name), 'tar',
        shutil.make_archive(str(pool_dir) + str(name), 'tar',
                            str(pool_dir) + str(name))
        shutil.rmtree(str(pool_dir) + str(name))
    except:
        print "Compression of observation %s coulnd't be possible" %(str(observations_dict.keys()[i]))

    duration = time.time() - actual_time
    duration_m = int(duration/60)
    duration_s = duration - duration_m*60

    camera='red'
    trackfile = open(trackfilename, 'a')
    trackfile.write('End ' + str(observations_dict.keys()[i]) + " " + camera +
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
