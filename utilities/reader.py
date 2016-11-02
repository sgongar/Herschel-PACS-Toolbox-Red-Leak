#!/usr/bin/python
import csv
from sys import argv
from os import listdir, getenv
from time import time
from reader_aux import obs_ids, sed_obs_A, obs_23


def look_for_characteristics():
    """

    """
    first_time = time()
    observations_dict = {}

    for i in range(len(obs_ids)):
        observations_dict[str(obs_ids[i])] = 'obs_ids'
    for j in range(len(sed_obs_A)):
        observations_dict[str(sed_obs_A[j])] = 'sed_obs'
    for k in range(len(obs_23)):
        observations_dict[str(obs_23[k])] = 'obs_23'

    observations_to_check = observations_dict.keys()

    for i in range(len(observations_to_check)):
        obs = getObservation(observations_to_check[i], useHsa=1)

        if str(obs.meta['obsMode'].value) == 'Mapping':
            if 'Range' in str(obs.meta['observingMode']):
                if 'Unchopped' in str(obs.meta['observingMode']):
                    if 'SED' in str(obs.meta['rangeSPOT'].value):
                        pass
                    else:
                        print "unchopped range mapping", observations_to_check[i]
                        break

                if 'Chopped' in str(obs.meta['observingMode']):
                    if 'SED' in str(obs.meta['rangeSPOT'].value):
                        pass
                    else:
                        print "chopnod range mapping", observations_to_check[i]

        if str(obs.meta['obsMode'].value) == 'Pointed':
            if 'Range' in str(obs.meta['observingMode']):
                if 'Unchopped' in str(obs.meta['observingMode']):
                    if 'SED' in str(obs.meta['rangeSPOT'].value):
                        pass
                    else:
                        print "unchopped range pointed", observations_to_check[i]

                if 'Chopped' in str(obs.meta['observingMode']):
                    if 'SED' in str(obs.meta['rangeSPOT'].value):
                        pass
                    else:
                        print "chopnod range pointed", observations_to_check[i]

        if str(obs.quality.meta['state'].value) != 'PENDING':
            list_wrong.append(observations_to_check[i])
            list_errors.append(str(obs.quality.meta['state'].value))

    file_right = open(working_dir + '/obs_right.csv', 'wt')
    try:
        writer = csv.writer(file_right)
        for j in range(len(list_right)):
            writer.writerow(('right', list_right[j]))
    finally:
        file_right.close()

    file_wrong = open(working_dir + '/obs_wrong.csv', 'wt')
    try:
        writer = csv.writer(file_wrong)
        for k in range(len(list_wrong)):
            writer.writerow(('wrong', list_wrong[k]))
    finally:
        file_wrong.close()

    last_time = time()
    total_time = str(last_time - first_time)
    print "Process takes %S s to be completed", total_time


def look_for_range(working_dir):
    """

    @param working_dir: string pointing working directory
    """
    first_time = time()
    print "Starting checking process at", str(first_time)

    observations_dict = {}
    list_right = []
    list_wrong = []

    for i in range(len(obs_ids)):
        observations_dict[str(obs_ids[i])] = 'obs_ids'
    for j in range(len(sed_obs_A)):
        observations_dict[str(sed_obs_A[j])] = 'sed_obs'
    for k in range(len(obs_23)):
        observations_dict[str(obs_23[k])] = 'obs_23'

    observations_to_check = observations_dict.keys()

    for i in range(len(observations_to_check)):
        # Check if there is data in our study's range
        print "Checking ", observations_to_check[i]
        obs = getObservation(observations_to_check[i], useHsa=1)
        j = 1
        ok = False
        while True:
            try:
                high = obs.meta['rangeHigh' + str(j)].value
                if (int(high) - 190) > 0:
                    ok = True
                j = j + 1
            except:
                break

        if ok is True:
            list_right.append(observations_to_check[i])
        elif ok is not True:
            list_wrong.append(observations_to_check[i])
        else:
            raise Exception

    file_right = open(working_dir + '/obs_right.csv', 'wt')
    try:
        writer = csv.writer(file_right)
        for j in range(len(list_right)):
            writer.writerow(('right', list_right[j]))
    finally:
        file_right.close()

    file_wrong = open(working_dir + '/obs_wrong.csv', 'wt')
    try:
        writer = csv.writer(file_wrong)
        for k in range(len(list_wrong)):
            writer.writerow(('wrong', list_wrong[k]))
    finally:
        file_wrong.close()

    last_time = time()
    total_time = str(last_time - first_time)
    print "Process takes %S s to be completed", total_time

    return True


def file_writer(file_name, list_to_save, list_number, pools_dir):
    """ write a defined number of csv files

    @param file_name: output file name
    @param list_to_save: list to be saved in csv files
    @param list_number: number of lists to be created
    @param pools_dir: string pointing pool's directory
    @return True: if everything goes alright
    """

    if list_to_save == 'all':
        obs_done = []

        j = 0
        i = 0
        full_obs = obs_ids + sed_obs_A + obs_23

        # Obtiene una lista con los ficheros existentes
        # estos tienen que estar en el siguiente buscador
        obs_raw = listdir(pools_dir)

        for i in range(len(obs_raw)):
            if obs_raw[i][-11:] != '_struct.tgz':
                obs_done.append(int(obs_raw[i][:-4]))

        for i in range(len(obs_done)):
            # print obs_done[i]
            if obs_done[i] in full_obs:
                full_obs.remove(obs_done[i])

        size = len(full_obs) / int(list_number)
        # Split full_obs in a list of lists
        list_obs = [full_obs[i:i + size] for i in range(0, len(full_obs),
                                                        size)]

        for i in range(len(list_obs)):
            print len(list_obs[i])
            f = open(file_name + '_' + str(i) + '.csv', 'wt')
            try:
                writer = csv.writer(f)
                for j in range(len(list_obs[i])):
                    writer.writerow(('all', list_obs[i][j]))
            finally:
                f.close()
    else:
        print list_to_save + '_' + file_name
        if list_to_save == 'obs_23':
            list_obs = obs_23
        elif list_to_save == 'obs_ids':
            list_obs = obs_ids
        elif list_to_save == 'sed_obs_A':
            list_obs = sed_obs_A
        else:
            raise Exception

        f = open(list_to_save + '_' + file_name + '.csv', 'wt')
        try:
            writer = csv.writer(f)
            for i in range(len(list_obs)):
                writer.writerow((list_to_save, list_obs[i]))
        finally:
            f.close()

    return True


def file_checker_against_problems():
    """

    @param
    @return True: if everything goes alright
    """
    files_list = listdir('/data/pools')

    for i in range(len(files_list)):
        if len(files_list[i]) == 28:
            files_list[i] = files_list[i][4:-14]
        elif len(files_list[i]) == 24:
            files_list[i] = files_list[i][:-14]
        else:
            raise Exception

    observations_dict = {}

    for i in range(len(obs_ids)):
        observations_dict[str(obs_ids[i])] = 'obs_ids'
    for j in range(len(sed_obs_A)):
        observations_dict[str(sed_obs_A[j])] = 'sed_obs'
    for k in range(len(obs_23)):
        observations_dict[str(obs_23[k])] = 'obs_23'

    observations_to_check = observations_dict.keys()
    for w in range(len(files_list)):
        observations_to_check.remove(files_list[w])

    observations_failed = []
    with open('red_leak_csv_issues_wrong.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            observations_failed.append(row[0])

    for x in range(len(observations_failed)):
        observations_to_check.remove(observations_failed[x])

    return True


def file_checker_against_done(pools_dir):
    """

    @param pools_dir: string pointing pool's directory
    @return True: if everything goes alright
    """

    for i in range(len(pools_dir)):
        """
        if len(pools_dir[i]) == 28:
            files_list[i] = files_list[i][4:-14]
        elif len(files_list[i]) == 24:
            files_list[i] = files_list[i][:-14]
        else:
            print files_list[i]
            # raise Exception
        """

    observations_dict = {}
    for i in range(len(obs_ids)):
        observations_dict[str(obs_ids[i])] = 'obs_ids'
    for j in range(len(sed_obs_A)):
        observations_dict[str(sed_obs_A[j])] = 'sed_obs'
    for k in range(len(obs_23)):
        observations_dict[str(obs_23[k])] = 'obs_23'

    observations_to_check = observations_dict.keys()
    for w in range(len(files_list)):
        observations_to_check.remove(files_list[w])

    print observations_to_check


    file_writer('obs_ids_to_check.csv', 'unknown',
                observations_to_check, 10)


def count_obs(pools_dir):
    """

    @param pools_dir: string pointing pool's directory
    @return True: if everything goes alright
    """
    print "Observations above 190: ", len(obs_ids)
    print "SED observations: ", len(sed_obs_A)
    print "Range 23 observations: ", len(obs_23)
    print " "
    print "Total observations to be analysed: ", (len(obs_ids) +
                                                  len(sed_obs_A) + len(obs_23))
    print "Observations correctly analysed: ", len(listdir(pools_dir))

    return True


if __name__ == "__main__":
    home_dir = str(getenv("HOME"))
    working_dir = home_dir + '/hcss/workspace/Red_Leak/'
    pools_dir = '/data/pools/tgz/'

    try:
        if argv[1] == '-writer':
            file_name = argv[2]
            list_to_save = argv[3]
            list_number = argv[4]
            file_writer(file_name, list_to_save, list_number, pools_dir)
        elif argv[1] == '-checker_problems':
            file_checker_against_problems()
        elif argv[1] == '-checker_done':
            file_checker_against_done()
        elif argv[1] == '-count':
            count_obs()
        elif argv[1] == '-look_for_range':
            look_for_range(working_dir)
        else:
            print "Wrong option"
    except Exception as e:
        # Excepcion creada para correr en HIPE
        # look_for_range(working_dir)
        print e

