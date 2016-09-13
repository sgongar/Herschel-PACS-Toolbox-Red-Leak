##  coding = utf-8
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
import sys

home_dir = os.getenv("HOME")
working_dir = str(home_dir) + '/hcss/workspace/Red_Leak/'
pool_dir = str(working_dir) + 'pools/'
csv_obs = str(working_dir) + 'obs_ids/obs_ids_tocheck_6.csv'
trackfilename = working_dir + 'red_leak_issues.txt'
trackcsvfilename = working_dir + 'red_leak_csv_issues_6.csv'

obs_complete = []
obs_incomplete = []

save_obs = False


def save_observation(obs, pool_name, tag_name):
    print "dentro de save_observation"
    try:
        saveProduct(product=obs, pool=str(pool_name),
                    tag=tag_name)
        print "Product %s saved" %(str(tag_name))
    except:
        print "Product %s not saved" %(str(tag_name))
    
    try:
        dataPool = LocalStoreFactory.getStore(LocalStoreContext(str(pool_name)))
        storage = ProductStorage(dataPool)
        urn = storage.getUrnFromTag(tag_name)
        exportObservation(pool=PoolManager.getPool(str(pool_name), 
                                                   urn=urn,
                                                   dirout = pool_dir + pool_name + '_HSAStruct',
                                                   warn=False))
    except:
        print "Error exporting observation"
    
    try:
        shutil.make_archive(pool_dir + 'tars/' + pool_name + '_HSAStruct', 'tar',
                            home_dir + '/.hcss/lstore/' + str(pool_name))

        shutil.rmtree(home_dir + '/.hcss/lstore/' + str(pool_name))
        shutil.rmtree(str(pool_dir) + str(pool_name) + '_HSAStruct')
        print "Compression of observation %s done" %(str(pool_name))
    except:
        print "Compression of observation %s coulnd't be possible" %(str(pool_name))
    

def check_available_levels():
    level = obs.meta['obsState'].value
    return level


def check_aor_label():
    label = obs.meta['aorLabel'].value
    return label


def read_csv_file():
    obs_csv_list = []
    errors_csv_list = []
    levels_csv_list = []
    labels_csv_list = []

    if not os.path.isfile(trackcsvfilename):
        trackfile = open(trackcsvfilename, 'w')
        trackfile.close()

    with open(str(trackcsvfilename), 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:       
            obs_csv_list.append(row[0])
            errors_csv_list.append(row[1])
            levels_csv_list.append(row[2])
            labels_csv_list.append(row[3])
    
    print "csv file readed"
    return obs_csv_list, errors_csv_list, levels_csv_list, labels_csv_list


def write_csv_file(obs_csv_list, errors_csv_list, levels_csv_list, labels_csv_list):
    try:
        os.remove(trackcsvfilename)
    except:
        print "old csv file not removed"

    rows = zip(obs_csv_list, errors_csv_list, levels_csv_list, labels_csv_list)
    with open(trackcsvfilename, 'wb') as g:
        writer = csv.writer(g, delimiter=',')
        for row in rows:
            writer.writerow(row)

    print "csv file wrote"


if (not os.path.exists(working_dir)):
    os.mkdir(working_dir)
if (not os.path.exists(pool_dir)):
    os.mkdir(pool_dir)

# Populate list from csv file
obs_list = []
with open(str(csv_obs), 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        obs_list.append(row[1])

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


observations_dictionary = {}

# Run pipeline over obs
for i in range(len(obs_list)):
    observations_dictionary["obs_{0}".format(observations_dict.keys()[i])] = getObservation(observations_dict.keys()[i],
                                                                                            useHsa=1)
    try:
        runPacsSpg(obsIn=observations_dictionary["obs_{0}".format(observations_dict.keys()[i])],
                                                                  cameraList=['red'])
        poolName = 'obs_' + str(observations_dict.keys()[i])
        save_observation(obs, str(observations_dict.keys()[i]), poolName)
        e = 'without_error'
        print "observation right"
    except:
        e = sys.exc_info()[0]
        pass
    else:
        print "cualquier otro"
        e = 'without_error'

    level = check_available_levels()
    label = check_aor_label()

    obs_csv_list, errors_csv_list, levels_csv_list, labels_csv_list = read_csv_file()
     
    obs_csv_list.append(str(observations_dict.keys()[i]))
    errors_csv_list.append(str(e))
    levels_csv_list.append(str(level))
    labels_csv_list.append(str(label))

    write_csv_file(obs_csv_list, errors_csv_list, levels_csv_list, labels_csv_list)