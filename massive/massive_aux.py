from time import time
from datetime import datetime
from csv import reader
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


def get_formatted_time():
    """ Return formatted time function
    
    @return time_hr: a time string formatted
    """
    time_hr = datetime.fromtimestamp(time())
    time_hr = str(time_hr)

    return time_hr


def save_message(message, mode, file):
    """ save a message to a file

    """
    message_file = open(file, mode)
    message_file.write(message)
    message_file.close()

    return True

def save_exception(exception):
    """ Save expection to file
    
    """
    print exception

    
def create_dictionary(obs_list):
    """ Create dictionary from observations list

    @param obs_list: a list which contains observation ids
    @return obs_dict: a dictionary which contains the observations
    """
    obs_dict = {}
    i, j, k, w = (0, )*4
    
    for i in range(len(obs_list)):
        if j == int(len(list(uppercase))):
            j = 0
            k += 1
        if k == int(len(list(uppercase))):
            k = 0
            w += 1
        obs_dict[obs_list[i]] = 'SED' + list(uppercase)[j] +\
                                list(uppercase)[k] + list(uppercase)[w]
        j += 1
        
    return obs_dict


def populate_obs(obs_file):
    """ Populate list from csv file
    
    @param obs_file: location of csv file to be read
    @return obs_list: a list which contains file observation ids
    """
    obs_list = []
    with open(str(obs_file), 'rb') as f:
        row_reader = reader(f, delimiter=',')
        for row in row_reader:
            obs_list.append(row[1])

    return obs_list
