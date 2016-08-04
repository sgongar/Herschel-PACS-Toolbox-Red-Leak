import os
import csv

home_dir = os.getenv("HOME")
working_dir = str(home_dir) + '/hcss/workspace/Red-leak/'
pool_dir = str(working_dir) + 'pools/'
zips_dir = str(pool_dir) + 'zips/'
plot_dir = str(working_dir) + 'plots/'
csv_obs = str(working_dir) + 'obs_ids_1.csv'

obs_list = []
with open(str(csv_obs), 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        obs_list.append(row[1])

list_obs_zips = []
list_obs_zips = os.listdir(zips_dir)
new_list_obs_zips = []
final_list_obs_zips = []

for i in range(len(list_obs_zips)):
    new_list_obs_zips.append(list_obs_zips[i][4:])

for i in range(len(new_list_obs_zips)):
    final_list_obs_zips.append(new_list_obs_zips[i][:-4])


print len(obs_list)

to_remove_list = []

for i in range(len(obs_list)):
    for j in range(len(final_list_obs_zips)):
        if obs_list[i] == final_list_obs_zips[j]:
            to_remove_list.append(obs_list[i])

# print to_remove_list

for i in range(len(to_remove_list)):
    obs_list.remove(to_remove_list[i])

print len(obs_list)


print obs_list
