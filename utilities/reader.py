#!/usr/bin/python
import csv
from sys import argv
from os import listdir, getcwd

wrong_obs = ['1342245455', '1342245456', '1342188941', '1342251034', 
             '1342220740', '1342189072', '1342245809', '1342193212',
             '1342203453', '1342203454', '1342204124', '1342204125',
             '1342197805', '1342193205', '1342197804', '1342197803',
             '1342193204']



# obs_done = 

obs_ids = [1342186305, 1342186798, 1342186797, 1342187020, 1342188034,
           1342188526, 1342189411, 1342187779, 1342266969, 1342266970,
           1342199407, 1342199420, 1342199415, 1342199238, 1342199748,
           1342199746, 1342189410, 1342206850, 1342266982, 1342266981,
           1342214636, 1342214673, 1342220743, 1342220982, 1342220599,
           1342221384, 1342221386, 1342221382, 1342221362, 1342266976,
           1342221364, 1342222076, 1342222100, 1342222084, 1342222194,
           1342222251, 1342222248, 1342223119, 1342222250, 1342223129,
           1342222765, 1342223104, 1342223124, 1342223106, 1342223102,
           1342223732, 1342223748, 1342223718, 1342223743, 1342223720,
           1342223779, 1342224399, 1342224397, 1342224395, 1342223805,
           1342228534, 1342231427, 1342232601, 1342237582, 1342232561,
           1342239376, 1342245246, 1342247009, 1342246394, 1342247784,
           1342247817, 1342249386, 1342249385, 1342249393, 1342249387,
           1342249392, 1342249390, 1342249391, 1342249384, 1342250904,
           1342265446, 1342265445, 1342265672, 1342265684, 1342266922,
           1342265682, 1342265673, 1342265683, 1342265689, 1342265686,
           1342265674, 1342265676, 1342265681, 1342265675, 1342265685,
           1342265690, 1342265670, 1342265692, 1342265677, 1342265671,
           1342265687, 1342265680, 1342265688, 1342265691, 1342265698,
           1342265697, 1342265700, 1342266978, 1342266979, 1342266974,
           1342265699, 1342264237, 1342266977, 1342266973, 1342266975,
           1342264238, 1342265929, 1342265923, 1342265921, 1342265937,
           1342265952, 1342265928, 1342265934, 1342265924, 1342265938,
           1342265930, 1342265931, 1342265936, 1342265922, 1342265940,
           1342265925, 1342265933, 1342265939, 1342265935, 1342265932,
           1342265927, 1342267182, 1342267177, 1342267178, 1342267185,
           1342267186, 1342267184, 1342267183, 1342267179, 1342267626,
           1342267875, 1342267858, 1342267844, 1342267879, 1342267842,
           1342267881, 1342267843, 1342267859, 1342267874, 1342267870,
           1342267880, 1342267861, 1342267878, 1342267877, 1342267860,
           1342270680, 1342270681, 1342209709, 1342229752, 1342266964,
           1342208907, 1342267869, 1342189612, 1342198300, 1342202589,
           1342203446, 1342208901, 1342208926, 1342209711, 1342209707,
           1342210384, 1342210399, 1342210824, 1342210827, 1342210834,
           1342211537, 1342211693, 1342212220, 1342212600, 1342266968,
           1342212790, 1342213146, 1342213911, 1342213925, 1342214220,
           1342225586, 1342225580, 1342225849, 1342225993, 1342234063,
           1342235692, 1342236271, 1342236272, 1342250999, 1342251177,
           1342251176, 1342252090, 1342252092, 1342253738, 1342254219,
           1342254218, 1342254216, 1342254217, 1342254257, 1342254255,
           1342254256, 1342254275, 1342254274, 1342254280, 1342254298,
           1342254297, 1342254299, 1342254300, 1342254610, 1342254611,
           1342254608, 1342254609, 1342254607, 1342254606, 1342254767,
           1342254620, 1342254616, 1342254617, 1342254618, 1342254619,
           1342254612, 1342254768, 1342254770, 1342254769, 1342254932,
           1342254931, 1342254937, 1342256254, 1342256255, 1342256256,
           1342256248, 1342256766, 1342256763, 1342256477, 1342256784,
           1342256783, 1342256928, 1342257275, 1342257686, 1342257793,
           1342259608, 1342262028, 1342262540, 1342262544, 1342262936,
           1342262945, 1342262958, 1342262967, 1342262981, 1342262976,
           1342263462, 1342263465, 1342263463, 1342263496, 1342266972,
           1342266971]

sed_obs_A = [1342188037, 1342188040, 1342188427, 1342188428, 1342188430,
             1342188431, 1342188433, 1342188434, 1342189272, 1342189273,
             1342191139, 1342191140, 1342192982, 1342192986, 1342192988,
             1342193214, 1342193215, 1342195633, 1342195634, 1342196687,
             1342196694, 1342196876, 1342196877, 1342197790, 1342197792,
             1342197795, 1342197799, 1342197881, 1342271056, 1342271057,
             1342197888, 1342197889, 1342197890, 1342197891, 1342197894,
             1342197895, 1342197900, 1342197901, 1342197902, 1342197903,
             1342197904, 1342197905, 1342197906, 1342197907, 1342198171,
             1342198174, 1342198176, 1342199146, 1342199234, 1342199235,
             1342199291, 1342199292, 1342199294, 1342199295, 1342199297,
             1342199298, 1342199413, 1342199418, 1342199883, 1342202120,
             1342202121, 1342202588, 1342203054, 1342203055, 1342203056,
             1342203057, 1342203136, 1342203137, 1342203679, 1342270773,
             1342203681, 1342204123, 1342204333, 1342204334, 1342270348,
             1342206866, 1342206867, 1342206868, 1342206869, 1342206871,
             1342206872, 1342206976, 1342206978, 1342206980, 1342206982,
             1342206984, 1342206988, 1342206989, 1342206992, 1342207776,
             1342207805, 1342207808, 1342207810, 1342207820, 1342208868,
             1342208869, 1342208881, 1342208885, 1342208887, 1342208888,
             1342208895, 1342208908, 1342208912, 1342208932, 1342208940,
             1342209393, 1342209732, 1342209736, 1342210398, 1342210652,
             1342210813, 1342210816, 1342211162, 1342211163, 1342211167,
             1342211168, 1342211173, 1342211679, 1342211680, 1342211682,
             1342211683, 1342211685, 1342211686, 1342211696, 1342211707,
             1342211708, 1342211709, 1342211710, 1342211821, 1342211822,
             1342212213, 1342212215, 1342212217, 1342212218, 1342212221,
             1342212231, 1342212243, 1342212245, 1342212247, 1342212249,
             1342212251, 1342212253, 1342212255, 1342212257, 1342212259,
             1342212513, 1342212541, 1342212577, 1342212608, 1342212609,
             1342212784, 1342212785, 1342213286, 1342213917, 1342213922,
             1342214623, 1342214624, 1342214675, 1342214676, 1342215642,
             1342215679, 1342215684, 1342215685, 1342215688, 1342215738,
             1342216166, 1342216175, 1342216181, 1342216183, 1342216214,
             1342216215, 1342216627, 1342216630, 1342216655, 1342217794,
             1342217795, 1342217798, 1342217799, 1342217800, 1342217801,
             1342217820, 1342217843, 1342217847, 1342217942, 1342218755,
             1342218756, 1342219435, 1342220596, 1342220597, 1342220600,
             1342220929, 1342220931, 1342221379, 1342221620, 1342270772,
             1342221621, 1342221624, 1342221625, 1342221626, 1342221627,
             1342221882, 1342223150, 1342223151, 1342223152, 1342223153,
             1342223154, 1342223155, 1342223375, 1342223712, 1342223713,
             1342223808, 1342224001, 1342224002, 1342224003, 1342224004,
             1342224005, 1342224006, 1342225140, 1342225141, 1342225142,
             1342225563, 1342225588, 1342225731, 1342225804, 1342225814,
             1342225815, 1342225817, 1342225818, 1342225820, 1342225821,
             1342225839, 1342225840, 1342225855, 1342226213, 1342227070,
             1342227210, 1342227639, 1342228188, 1342228201, 1342228203,
             1342228248, 1342228414, 1342228472, 1342228475, 1342228520,
             1342228525, 1342228529, 1342228538, 1342229090, 1342229092,
             1342229696, 1342229702, 1342229703, 1342229706, 1342229707,
             1342229708, 1342229709, 1342229711, 1342229719, 1342229737,
             1342229738, 1342229740, 1342229795, 1342229798, 1342229806,
             1342229808, 1342229816, 1342230150, 1342230999, 1342231001,
             1342231004, 1342231275, 1342231276, 1342231295, 1342231296,
             1342231300, 1342231305, 1342231320, 1342231322, 1342231418,
             1342231419, 1342231420, 1342231421, 1342231422, 1342231700,
             1342231701, 1342231723, 1342231956, 1342232279, 1342232298,
             1342232299, 1342232300, 1342232540, 1342232541, 1342232544,
             1342232545, 1342232546, 1342232547, 1342232577, 1342232578,
             1342233445, 1342233469, 1342233470, 1342233471, 1342233716,
             1342234268, 1342234478, 1342234479, 1342234482, 1342234483,
             1342234484, 1342234485, 1342234938, 1342234939, 1342234941,
             1342234942, 1342234944, 1342234945, 1342235646, 1342235647,
             1342235650, 1342235651, 1342235652, 1342235653, 1342235679,
             1342235690, 1342235848, 1342235850, 1342235852, 1342236879,
             1342237482, 1342237483, 1342238354, 1342238355, 1342238357,
             1342238358, 1342238388, 1342238905, 1342238906, 1342238926,
             1342239475, 1342239476, 1342242440, 1342242447, 1342242449,
             1342243110, 1342243504, 1342243516, 1342243517, 1342243869,
             1342243870, 1342244459, 1342244461, 1342244463, 1342244465,
             1342244467, 1342244469, 1342244911, 1342244913, 1342244915,
             1342245222, 1342245223, 1342245229, 1342245244, 1342270346,
             1342245648, 1342245803, 1342245804, 1342245810, 1342269932,
             1342245953, 1342245954, 1342245957, 1342246652, 1342246653,
             1342246656, 1342246657, 1342246658, 1342246659, 1342246788,
             1342246789, 1342246792, 1342246793, 1342246794, 1342246795,
             1342247006, 1342247444, 1342247445, 1342247458, 1342247459,
             1342247461, 1342247462, 1342247464, 1342247465, 1342248358,
             1342248542, 1342248543, 1342248673, 1342248675, 1342248677,
             1342248929, 1342249199, 1342249201, 1342249203, 1342249307,
             1342249308, 1342250306, 1342250307, 1342250310, 1342250311,
             1342250312, 1342250313, 1342250580, 1342250582, 1342250886,
             1342250887, 1342250889, 1342250891, 1342250902, 1342250908,
             1342250909, 1342250910, 1342250991, 1342251033, 1342251351,
             1342251353, 1342251356, 1342251358, 1342251360, 1342251362,
             1342252075, 1342252076, 1342252079, 1342252080, 1342252081,
             1342252082, 1342252084, 1342252086, 1342252262, 1342252263,
             1342252264, 1342252265, 1342252266, 1342252267, 1342252268,
             1342252327, 1342252328, 1342252329, 1342252330, 1342252331,
             1342252332, 1342252333, 1342252334, 1342252335, 1342252345,
             1342252346, 1342254765, 1342254766, 1342255725, 1342255726,
             1342255729, 1342255730, 1342255731, 1342255732, 1342256244,
             1342256245, 1342256778, 1342256780, 1342256782, 1342257209,
             1342257210, 1342257213, 1342257214, 1342257215, 1342257216,
             1342257634, 1342258094, 1342258095, 1342258097, 1342258098,
             1342258100, 1342258101, 1342262002, 1342262003, 1342262542,
             1342262952, 1342262953, 1342262965, 1342262966, 1342262974,
             1342262975, 1342262988, 1342262989, 1342262994, 1342262995,
             1342262998, 1342262999, 1342263472, 1342263930, 1342263931,
             1342265678, 1342267180, 1342267873, 1342268748, 1342268790,
             1342268792, 1342268794, 1342268798, 1342269292, 1342269293,
             1342269296, 1342269297, 1342269298, 1342269299, 1342269304,
             1342269876, 1342269877, 1342269911, 1342269913, 1342269915,
             1342269917, 1342269919]


obs_23 = [1342213138, 1342213762, 1342215667, 1342230909, 1342230907,
          1342230906, 1342230908, 1342238514, 1342259561, 1342262769,
          1342245393, 1342245646, 1342253746, 1342218568, 1342253747,
          1342253745, 1342254935, 1342254953, 1342256261, 1342257285,
          1342257798]


def look():
    from time import time
    first_time = time()
    observations_dict = {}

    for i in range(len(obs_ids)):
        observations_dict[str(obs_ids[i])] = 'obs_ids'
    """  
    for j in range(len(sed_obs_A)):
        observations_dict[str(sed_obs_A[j])] = 'sed_obs'
    """
    for k in range(len(obs_23)):
        observations_dict[str(obs_23[k])] = 'obs_23'

    observations_to_check = observations_dict.keys()
   
    print "para mirar tengo ", len(observations_to_check)

    print len(observations_to_check)*2
  
    list_mapping = []

    # datos = obs.meta['rangeLow2'].value

    for i in range(len(observations_to_check)):
        # print "Checking ", observations_to_check[i]
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
        """
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
        """
"""
# HIPE> print sed_obs_b.meta['observingMode'].value
        
        
        if str(obs.quality.meta['state'].value) != 'PENDING':
            list_wrong.append(observations_to_check[i])
            list_errors.append(str(obs.quality.meta['state'].value))
    print list_wrong
    print list_errors


    for i in range(len(observations_to_check)):
        print "Checking ", observations_to_check[i]
        obs = getObservation(observations_to_check[i], useHsa=1)
        j = 1
        ok = False
        while True:
            try:
                high = obs.meta['rangeHigh'+ str(j)].value
                if (int(high) - 190)> 0:
                    ok = True
                j = j + 1
            except:
                break

        if ok is True:
            list_right.append(observations_to_check[i])
            # print "ok is: ", ok
            # print len(list_right)
        elif os is not True:
            list_wrong.append(observations_to_check[i])
            # print "ok is: ", ok
            # print len(list_wrong)
        else:
            raise Exception

    file_right = open('/home/sgongora/hcss/workspace/Red_Leak/obs_right.csv', 'wt')
    try:
        writer = csv.writer(file_right)
        for j in range(len(list_right)):
            # print list_right[i]
            writer.writerow(('right', list_right[j]))
    finally:
        file_right.close()

    file_wrong = open('/home/sgongora/hcss/workspace/Red_Leak/obs_wrong.csv', 'wt')
    try:
        writer = csv.writer(file_wrong)
        for k in range(len(list_wrong)):
            # print list_wrong[i]
            writer.writerow(('wrong', list_wrong[k]))
    finally:
        file_wrong.close()    

    print "mala lista es ", len(list_wrong)
  
    # finish at
    last_time = time()

    print last_time-first_time
"""
def file_writer(file_name, list_to_save, list_number):
    """ write a defined number of csv files
    
    @param file_name:
    @param list_name:
    @param list_to_save:
    @return True: if everything goes alright
    """
    

    if list_to_save == 'all':
        obs_done = []
        index_obs = []
      
        j = 0
        i = 0
        full_obs = obs_ids + sed_obs_A + obs_23


        for i in range(len(obs_raw)):
            if obs_raw[i][-11:] != '_struct.tgz':
                obs_done.append(int(obs_raw[i][:-4]))
                
        print len(obs_done)
        print len(full_obs)
        # print obs_done
        # print full_obs
        for i in range(len(obs_done)):
            # print obs_done[i]
            if obs_done[i] in full_obs:
                full_obs.remove(obs_done[i])
        print len(full_obs)

        size = len(full_obs)/int(list_number)
        # dividir en cachso
        list_obs = [full_obs[i:i+size] for i in range(0, len(full_obs), size)]
        print len(list_obs)
        for i in range(len(list_obs)):
            print len(list_obs[i])
            f = open(file_name + '_' + str(i) + '.csv', 'wt')
            try:
                writer = csv.writer(f)
                # print len(list_obs[i])
                # print list_obs[i]
                for j in range(len(list_obs[i])):
                    # print list_obs[i][j]
                    writer.writerow(('all', list_obs[i][j]))
            finally:
                f.close()
    else:
        f = open(file_name, 'wt')
        try:
            writer = csv.writer(f)
            for i in range(len(list_to_save)):
                writer.writerow((list_name, list_to_save[i]))
        finally:
            f.close()
    
    return True

def file_checker_against_problems():
    """
    
    @ param 
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
    """
    for i in range(len(obs_ids)):
        observations_dict[str(obs_ids[i])] = 'obs_ids'
    """
    for j in range(len(sed_obs)):
        observations_dict[str(sed_obs[j])] = 'sed_obs'
    """
    for k in range(len(obs_23)):
        observations_dict[str(obs_23[k])] = 'obs_23'
    """

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

    print observations_to_check    
    print len(observations_to_check)


def file_checker_against_done():
    """

    """
    files_list = listdir('/data/pools')

    for i in range(len(files_list)):
        if len(files_list[i]) == 28:
            files_list[i] = files_list[i][4:-14]
        elif len(files_list[i]) == 24:
            files_list[i] = files_list[i][:-14]
        else:
            print files_list[i]
            # raise Exception
    
    observations_dict = {}
    for i in range(len(obs_ids)):
        observations_dict[str(obs_ids[i])] = 'obs_ids'
    for j in range(len(sed_obs)):
        observations_dict[str(sed_obs[j])] = 'sed_obs'
    for k in range(len(obs_23)):
        observations_dict[str(obs_23[k])] = 'obs_23'

    observations_to_check = observations_dict.keys()
    for w in range(len(files_list)):
        observations_to_check.remove(files_list[w])

    print observations_to_check

    """
    file_writer('obs_ids_to_check.csv', 'unknown',
                observations_to_check, 10)
    """

def count_obs():
    """

    """
    print "Observations above 190: ", len(obs_ids)
    print "SED observations: ", len(sed_obs)
    print "Range 23 observations: ", len(obs_23)
    print " "
    print "Total observations to be analysed: ", (len(obs_ids) + len(sed_obs) + len(obs_23))
    print "Observations correctly analysed: ", len(listdir('/data/pools'))


if __name__ == "__main__":
    try:
        if argv[1] == '-writer':
            file_name = argv[2]
            list_to_save = argv[3]
            list_number = argv[4]
            file_writer(file_name, list_to_save, list_number)
        elif argv[1] == '-checker_problems':
            file_checker_against_problems()
        elif argv[1] == '-checker_done':
            file_checker_against_done()
        elif argv[1] == '-count':
            count_obs()
        elif argv[1] == '-look':
            look()
        else:
            print "Wrong option"
    except Exception as e:
        # print e
        look()

