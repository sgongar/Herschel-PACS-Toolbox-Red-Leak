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
def get_formatted_time():
    """ Return formatted time function
    """
    time_hr = datetime.datetime.fromtimestamp(time())
    time_hr = str(time_hr)

    return time_hr


def save_exception(exception):
    """ Save expection to file
    """
    print exception

    
def create_dictionary(obs_list):
    """ Create dictionary from observations list
    
    """
    observations_dict = {}
    i = 0
    j = 0
    k = 0
    w = 0
    for i in range(len(obs_list)):
        if j == int(len(list(uppercase))):
            j = 0
            k = k + 1

        if k == int(len(list(uppercase))):
            k = 0
            w = w + 1

        obs_dict[obs_list[i]] = 'SED' +
                                list(uppercase)[j] +
                                list(uppercase)[k] +
                                list(uppercase)[w]
        j = j + 1
        
    return obs_dict
