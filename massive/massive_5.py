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

home_dir = os.getenv("HOME")
# home_dir = '/home2/sgongora'
working_dir = str(home_dir) + '/hcss/workspace/Red_Leak/'
pool_dir = str(working_dir) + 'pools/'
tars_dir = str(pool_dir) + 'tars/'
plot_dir = str(working_dir) + 'plots/'
csv_obs = str(working_dir) + 'obs_ids/obs_ids_5.csv'

save_obs = False

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
"""
list_obs_tars = []
list_obs_tars = os.listdir(tars_dir)
new_list_obs_tars = []
final_list_obs_tars = []
obs_incomplete = []
to_append_list = []
obs_list_to_compress = []

for i in range(len(obs_list)):
    for j in range(len(list_obs_tars)):
        if 'obs_' + obs_list[i] == list_obs_tars[j][:-14]:
            to_append_list.append(list_obs_tars[j])

print to_append_list

# to append list son los analisis que ya tengo hechos
# ahora tengo que ver dentro de ellos cuales son los que terminan en bz2
for i in range(len(to_append_list)):
    if to_append_list[i][28:] == '.bz2':
        print "compressed"
    else:
        obs_list_to_compress.append(to_append_list[i])
        
        print to_append_list[i]
        shutil.make_archive(tars_dir + to_append_list[i], 'bztar',
                            tars_dir + to_append_list[i][:-4])
        
        shutil.rmtree(home_dir + '/.hcss/lstore/' + str(observations_dict.keys()[i]))
        shutil.rmtree(str(pool_dir) + str(pool_name) + '_HSAStruct')

# obs_list_to_compress son las que tengo que comprimir
print len(obs_list_to_compress)
print obs_list_to_compress

for i in range(len(list_obs_tars)):
    new_list_obs_tars.append(list_obs_tars[i][4:])

for i in range(len(new_list_obs_tars)):
    final_list_obs_tars.append(new_list_obs_tars[i][:-14])
"""
to_remove_list = []

"""
for i in range(len(obs_list)):
    for j in range(len(final_list_obs_tars)):
        if obs_list[i] == final_list_obs_tars[j]:
            to_remove_list.append(obs_list[i])
"""

print len(obs_list)
analysed_list = ['1342204332', '1342204333', '1342204334', '1342206870', '1342206991', '1342208926', '1342208931', '1342208932', '1342211678', '1342212512', '1342212513', '1342220930', '1342220931', '1342221362', '1342225820', '1342225821', '1342225822', '1342227210', '1342228415', '1342228537', '1342228538', '1342229752', '1342231274', '1342231702', '1342238904', '1342238905', '1342238906', '1342244464', '1342244468', '1342244469', '1342250904', '1342250907', '1342252080', '1342252081', '1342252082', '1342252085', '1342252090', '1342252092', '1342253738', '1342254274', '1342254275', '1342268797', '1342268798', '1342270639', '1342188432', '1342206871', '1342206872', '1342206990', '1342206992', '1342211679', '1342211681', '1342216215', '1342218754', '1342218755', '1342218756', '1342225838', '1342227209', '1342231700', '1342231701', '1342231703', '1342244465', '1342244466', '1342250908', '1342250909', '1342252083', '1342252084', '1342252086', '1342269414', '1342188430', '1342188431', '1342188433', '1342206866', '1342206867', '1342206988', '1342211680', '1342211683', '1342216213', '1342216214', '1342233445', '1342233446', '1342233447', '1342238354', '1342238355', '1342238356', '1342244467', '1342246651', '1342246652', '1342250580', '1342250581', '1342250902', '1342250903', '1342252076', '1342252077', '1342252078', '1342252079', '1342258096', '1342258097', '1342271055', '1342271056', '1342271057', '1342211682', '1342206987', '1342211684', '1342211685', '1342238357', '1342238358', '1342250582', '1342258098', '1342258099', '1342188434', '1342212531', '1342258093', '1342206869', '1342229089', '1342239689', '1342206868', '1342258094', '1342211686', '1342225840', '1342231957', '1342244458', '1342258095', '1342206850', '1342206989', '1342216216', '1342218757', '1342225839', '1342231275', '1342231276', '1342231956', '1342233697', '1342238351', '1342244459', '1342244460', '1342244461', '1342244462', '1342265942', '1342199415', '1342206984', '1342267869', '1342244463', '1342262974', '1342233696', '1342262976', '1342265923', '1342206983', '1342250579', '1342262975', '1342267861', '1342206986', '1342233473', '1342262972', '1342265922', '1342267626', '1342206864', '1342206865', '1342206980', '1342206982', '1342217796', '1342217797', '1342217798', '1342225730', '1342229092', '1342235651', '1342235652', '1342238926', '1342254300', '1342258100', '1342258101', '1342262973', '1342262981', '1342262986', '1342265924', '1342265925', '1342265927', '1342265929', '1342267870', '1342267874', '1342267875', '1342267878', '1342268638', '1342269297', '1342269920', '1342192805', '1342212541', '1342217793', '1342217799', '1342231296', '1342262987', '1342262988', '1342262989', '1342265685', '1342265688', '1342265928', '1342267877', '1342267879', '1342267880', '1342267881', '1342269295', '1342269296', '1342206981', '1342212783', '1342233471', '1342238927', '1342252351', '1342252353', '1342252354', '1342254256', '1342254257', '1342254937', '1342264238', '1342265687', '1342188034', '1342217794', '1342235650', '1342246789', '1342252352', '1342254255', '1342254935', '1342265921', '1342217795', '1342245455', '1342252355', '1342254931', '1342254932', '1342264237', '1342269294', '1342229093', '1342246788', '1342254297', '1342262952', '1342265691', '1342269299', '1342193216', '1342262953', '1342263471', '1342265690', '1342211842', '1342245456', '1342252270', '1342262958', '1342265692', '1342269298', '1342231295', '1342246787', '1342262950', '1342267842', '1342267843', '1342269293', '1342193217', '1342211696', '1342246792', '1342246793', '1342262951', '1342267844', '1342269291', '1342269292', '1342208907', '1342232561', '1342233472', '1342246795', '1342252265', '1342252266', '1342254606', '1342212785', '1342233470', '1342245222', '1342268729', '1342199420', '1342209717', '1342252263', '1342193214', '1342252264', '1342254609', '1342228201', '1342247817', '1342250007', '1342263472', '1342197790', '1342199298', '1342211820', '1342211821', '1342211822', '1342217800', '1342217801', '1342221626', '1342221627', '1342231305', '1342234937', '1342234939', '1342245957', '1342259561', '1342188040', '1342199746', '1342208894', '1342208895', '1342208901', '1342211705', '1342211706', '1342211708', '1342221621', '1342221622', '1342221623', '1342221624', '1342221625', '1342231302', '1342231304', '1342231422', '1342234938', '1342245956', '1342247457', '1342247458', '1342247459', '1342247537', '1342248309', '1342251358', '1342251359', '1342251360', '1342252328', '1342254607', '1342254608', '1342269932', '1342188037', '1342211707', '1342221620', '1342225849', '1342231303', '1342247465', '1342251176', '1342251177', '1342252326', '1342252329', '1342265683', '1342265684', '1342265686', '1342265934', '1342211693', '1342239757', '1342240149', '1342248357', '1342248675', '1342252327', '1342257275', '1342257793', '1342263473', '1342265445', '1342265446', '1342265675', '1342265680', '1342265697', '1342265698', '1342265933', '1342265935', '1342265936', '1342265937', '1342265938', '1342269458', '1342188038', '1342188039', '1342199748', '1342211709', '1342216167', '1342221386', '1342223375', '1342231300', '1342231421', '1342242448', '1342248676', '1342249203', '1342251357', '1342254280', '1342256245', '1342257213', '1342257214', '1342263474', '1342265670', '1342265671', '1342265677', '1342265681', '1342265689', '1342265930', '1342265939', '1342265952', '1342267858', '1342267859', '1342267872', '1342196694', '1342196695', '1342213911', '1342219435', '1342223124', '1342227069', '1342231420', '1342242449', '1342247463', '1342247784', '1342248673', '1342257215', '1342257216', '1342262967', '1342265699', '1342267873', '1342208881', '1342216166', '1342223720', '1342223808', '1342225580', '1342231319', '1342231427', '1342242444', '1342249202', '1342250305', '1342257210', '1342257211', '1342257212', '1342265700', '1342265940', '1342267179', '1342267835', '1342187020', '1342208888', '1342209711', '1342212243', '1342212244', '1342212246', '1342222084', '1342223129', '1342237582', '1342242445', '1342247464', '1342248674', '1342256243', '1342256244', '1342263496', '1342265932', '1342266922', '1342267177', '1342267178', '1342267184', '1342267185', '1342269933', '1342208889', '1342209709', '1342211710', '1342212245', '1342212247', '1342212248', '1342225586', '1342242446', '1342247461', '1342247780', '1342249200', '1342249201', '1342257208', '1342262541', '1342262542', '1342267183', '1342267186', '1342203446', '1342208886', '1342208887', '1342209735', '1342212249', '1342230907', '1342242440', '1342242447', '1342247462', '1342250307', '1342252074', '1342252075', '1342257209', '1342267860', '1342209707', '1342209736', '1342223805', '1342248672', '1342252350', '1342241478', '1342208884', '1342231318', '1342209731', '1342252348', '1342210652', '1342217848', '1342223150', '1342230906', '1342234063', '1342242441', '1342248929', '1342251356', '1342252342', '1342252349', '1342256255', '1342263481', '1342266978', '1342266979', '1342188941', '1342210813', '1342210814', '1342213925', '1342215668', '1342217944', '1342220743', '1342223151', '1342223152', '1342225993', '1342234061', '1342240150', '1342240151', '1342246389', '1342248928', '1342252343', '1342255731', '1342256254', '1342202589', '1342210815', '1342210816', '1342217846', '1342223153', '1342224000', '1342224395', '1342229792', '1342231745', '1342231746', '1342239720', '1342239764', '1342247009', '1342247443', '1342247444', '1342250886', '1342252340', '1342254620', '1342255730', '1342256248', '1342262936', '1342266972', '1342187779', '1342208885', '1342209732', '1342212604', '1342212607', '1342212608', '1342214220', '1342217847', '1342222248', '1342222765', '1342223154', '1342223155', '1342224001', '1342228187', '1342229795', '1342231741', '1342231742', '1342231747', '1342235672', '1342239721', '1342239763', '1342246794', '1342250885', '1342250887', '1342252341', '1342252346', '1342252347', '1342256763', '1342256766', '1342262996', '1342262997', '1342208882', '1342210384', '1342211161', '1342211162', '1342212251', '1342212600', '1342212609', '1342220596', '1342220597', '1342220982', '1342224002', '1342224003', '1342224397', '1342225589', '1342228188', '1342229794', '1342230908', '1342230909', '1342231743', '1342231744', '1342236880', '1342246790', '1342246791', '1342247460', '1342250306', '1342250309', '1342252267', '1342252344', '1342254765', '1342254766', '1342262998', '1342262999', '1342263483', '1342269305', '1342188426', '1342206977', '1342210824', '1342210827', '1342211163', '1342212250', '1342212253', '1342213921', '1342221882', '1342221883', '1342224399', '1342225588', '1342225804', '1342229711', '1342231740', '1342232279', '1342240165', '1342240166', '1342246390', '1342246658', '1342250308', '1342252268', '1342252345', '1342254617', '1342254764', '1342263462', '1342263463', '1342263484', '1342266970', '1342266973', '1342269304', '1342270681', '1342193215', '1342195634', '1342211166', '1342212252', '1342212254', '1342212255', '1342220595', '1342225803', '1342229798', '1342232278', '1342246657', '1342246659', '1342254218', '1342254219', '1342254616', '1342255732', '1342263465', '1342266971', '1342266976', '1342266977', '1342268730', '1342270680', '1342189072', '1342206976', '1342210397', '1342211168', '1342213922', '1342223147', '1342223148', '1342225140', '1342225141', '1342227774', '1342232290', '1342232291', '1342232293', '1342240163', '1342240164', '1342246654', '1342249307', '1342249308', '1342254299', '1342254618', '1342254619', '1342257634', '1342262993', '1342262994', '1342266974', '1342266975', '1342193212', '1342195633', '1342212213', '1342212257', '1342216084', '1342220928', '1342223149', '1342225142', '1342225143', '1342225560', '1342229704', '1342229705', '1342229797', '1342232292', '1342234944', '1342246653', '1342249306', '1342251350', '1342251351', '1342254217', '1342254298', '1342256477', '1342256780', '1342256928', '1342262995', '1342268778', '1342206979', '1342211167', '1342212576', '1342213146', '1342221619', '1342229702', '1342229703', '1342234942', '1342234943', '1342234945', '1342246557', '1342246656', '1342251034', '1342251353', '1342254216', '1342254610', '1342254611', '1342254612', '1342256781', '1342270010', '1342208912', '1342210398', '1342210399', '1342212212', '1342220600', '1342225563', '1342229823', '1342234269', '1342251033', '1342251352', '1342256782', '1342270771', '1342270772', '1342198300', '1342212215', '1342212256', '1342220601', '1342225564', '1342229709', '1342234940', '1342234941', '1342235692', '1342251355', '1342252262', '1342254770', '1342262028', '1342269355', '1342186797', '1342186798', '1342210834', '1342212214', '1342212259', '1342220741', '1342224004', '1342224005', '1342229708', '1342247005', '1342262001', '1342262945', '1342266981', '1342212220', '1342212258', '1342229707', '1342234268', '1342234485', '1342245393', '1342247445', '1342254768', '1342254769', '1342262002', '1342263929', '1342266982', '1342195632', '1342212577', '1342221379', '1342229706', '1342234483', '1342234484', '1342248358', '1342252339', '1342254767', '1342256784', '1342262540', '1342262544', '1342263931', '1342270773', '1342188429', '1342206978', '1342211537', '1342212216', '1342212217', '1342212219', '1342224006', '1342225731', '1342230150', '1342230151', '1342234481', '1342234482', '1342246655', '1342248677', '1342255728', '1342265931', '1342269918', '1342196686', '1342196687', '1342212218', '1342212260', '1342188427', '1342211173', '1342217819', '1342197890', '1342214636', '1342234480', '1342236272', '1342252337', '1342255727', '1342269917', '1342236271', '1342255726', '1342199238', '1342225139', '1342269916', '1342211695', '1342252338', '1342262992', '1342220751', '1342225799', '1342250999', '1342255725', '1342212542', '1342221364', '1342240167', '1342255729', '1342269915', '1342189612', '1342212784', '1342222100', '1342223711', '1342231323', '1342251362', '1342223712', '1342252331', '1342212790', '1342223102', '1342251361', '1342223998', '1342252332', '1342256256', '1342213917', '1342223104', '1342223713', '1342223743', '1342256778', '1342223999', '1342250888', '1342213918', '1342256779', '1342215667', '1342223106', '1342225815', '1342250889', '1342269919', '1342220740', '1342249386', '1342249387', '1342252330', '1342262963', '1342225814', '1342231320', '1342249385', '1342252335', '1342255724', '1342262964', '1342266969', '1342269877', '1342192975', '1342212231', '1342221380', '1342225817', '1342238730', '1342252333', '1342252336', '1342262965', '1342262966', '1342211174', '1342225816', '1342239741', '1342252334', '1342256783', '1342266968', '1342269876', '1342199407', '1342217820', '1342199234', '1342231322', '1342269875', '1342212230', '1342225818', '1342239724', '1342250917', '1342198170', '1342213286', '1342217842', '1342262003', '1342212221', '1342213287', '1342241265', '1342241266', '1342242631', '1342246394', '1342249384', '1342266964', '1342268748', '1342269914', '1342217843', '1342223748', '1342242632', '1342267182', '1342213683', '1342241269', '1342265673', '1342269913', '1342217942', '1342235850', '1342241268', '1342250910', '1342265672', '1342265674', '1342220929', '1342235691', '1342241267', '1342231416', '1342265679', '1342235690', '1342228534', '1342231415', '1342235849', '1342198171', '1342237480', '1342241270', '1342245246', '1342265676', '1342189410', '1342231414', '1342235848', '1342198174', '1342221384', '1342222076', '1342235649', '1342241708', '1342269516', '1342231413', '1342235648', '1342250912', '1342259608', '1342213138', '1342235647', '1342269912', '1342235646', '1342250911', '1342257285', '1342197897', '1342235645', '1342263930', '1342189271', '1342250891', '1342197898', '1342235680', '1342250990', '1342189272', '1342250890', '1342197899', '1342257686', '1342265678', '1342189273', '1342250991', '1342268789', '1342197805', '1342193205', '1342269911', '1342197804', '1342197803', '1342197802', '1342268791', '1342189411', '1342193204', '1342196877', '1342197889', '1342196876', '1342268790', '1342197800', '1342197888', '1342196875', '1342197887', '1342268751', '1342197886', '1342191140', '1342197885', '1342218568', '1342268794', '1342197884', '1342197883', '1342268793', '1342197881', '1342257798', '1342268792', '1342238514', '1342186305', '1342270348', '1342256261', '1342188526', '1342262769', '1342267180', '1342270345', '1342245646', '1342267181', '1342197900', '1342197901', '1342197902', '1342197903', '1342270344', '1342197904', '1342270347', '1342197905', '1342191138', '1342253747', '1342192986', '1342197906', '1342192985', '1342197907', '1342253745', '1342192988', '1342253746', '1342191139', '1342192987', '1342192982', '1342192981', '1342239373', '1342197799', '1342197795', '1342197794', '1342213762', '1342254953', '1342197793', '1342197792', '1342197791', '1342199233', '1342225819', '1342231739', '1342231419', '1342270346', '1342199235', '1342231738', '1342234479', '1342235679', '1342216181', '1342231418', '1342232541', '1342206975', '1342231417', '1342231699', '1342203137', '1342228475', '1342232540', '1342216183', '1342232584', '1342235854', '1342199883', '1342228530', '1342237481', '1342203050', '1342199884', '1342235853', '1342203051', '1342216182', '1342232301', '1342228473', '1342232543', '1342237482', '1342202120', '1342232576', '1342235852', '1342237483', '1342203056', '1342228474', '1342229715', '1342235653', '1342232300', '1342238375', '1342207820', '1342226212', '1342232542', '1342238359', '1342204123', '1342229701', '1342232575', '1342207807', '1342229737', '1342234477', '1342203057', '1342215738', '1342203453', '1342216629', '1342228414', '1342229714', '1342207808', '1342204124', '1342203135', '1342215737', '1342229719', '1342203454', '1342207819', '1342216628', '1342226213', '1342216627', '1342235851', '1342228527', '1342216174', '1342204125', '1342207805', '1342228528', '1342203136', '1342203052', '1342215683', '1342225855', '1342203053', '1342207806', '1342216178', '1342202122', '1342208868', '1342228525', '1342208869', '1342225856', '1342203054', '1342202121', '1342216175', '1342207809', '1342203055', '1342238388', '1342215687', '1342204122', '1342228529', '1342199290', '1342199291', '1342227639', '1342199292', '1342216655', '1342199293', '1342199294', '1342199295', '1342214675', '1342199296', '1342199297', '1342215642', '1342215686', '1342216654', '1342215641', '1342215685', '1342215684', '1342216630']

for i in range(len(obs_list)):
    for j in range(len(analysed_list)):
        if obs_list[i] == analysed_list[j]:
            to_remove_list.append(analysed_list[j])

print len(to_remove_list)

for i in range(len(to_remove_list)):
    obs_list.remove(to_remove_list[i])

print len(obs_list)

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
observations_processed = {}
finalCubeList = []


print observations_dict
# Run pipeline over obs
for i in range(len(obs_list)):
    # camera='camera'
    # Next, get the data
    pool_name = 'obs_' + str(observations_dict.keys()[i])
    observations_dictionary["obs_{0}".format(observations_dict.keys()[i])] = getObservation(observations_dict.keys()[i],
                                                                                            useHsa=1)

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
        runPacsSpg(obsIn=observations_dictionary["obs_{0}".format(observations_dict.keys()[i])], cameraList=['red'])
        poolName = 'obs_' + str(observations_dict.keys()[i])
    except:
        obs_incomplete.append(observations_dict.keys()[i])
        poolName = 'obs_incomplete' + str(observations_dict.keys()[i])

    try:
        tag=poolName
        saveProduct(product=obs, pool=str(observations_dict.keys()[i]), tag=tag)
    except:
        print "Obs %s not saved" %(str(observations_dict.keys()[i]))


    dataPool = LocalStoreFactory.getStore(LocalStoreContext(str(observations_dict.keys()[i])))
    storage = ProductStorage(dataPool)
    urn = storage.getUrnFromTag(tag)
    exportObservation(pool=PoolManager.getPool(str(observations_dict.keys()[i])), urn=urn, 
                      dirout = pool_dir + pool_name + '_HSAStruct', warn=False)
    
    try:
        shutil.make_archive(pool_dir + 'tars/' + pool_name + '_HSAStruct', 'tar',
                            home_dir + '/.hcss/lstore/' + str(observations_dict.keys()[i]))

        shutil.rmtree(home_dir + '/.hcss/lstore/' + str(observations_dict.keys()[i]))
        shutil.rmtree(str(pool_dir) + str(pool_name) + '_HSAStruct')
    
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
