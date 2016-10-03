import time
import shutil
import os

home_dir = os.getenv("HOME")
working_dir = str(home_dir) + '/hcss/workspace/Red_Leak/'
pool_dir = str(working_dir) + 'pools/'

# Regular export, regular tar.gz compression
time_1 = time.time()
exportObservation(pool=PoolManager.getPool('1342199235'), 
                  urn="urn:1342199235:herschel.ia.obs.ObservationContext:0",
                  dirout="/home/sgongora/hcss/workspace/Red_Leak/pools/Export414880784329918512DIR/1342199235")
compress(inputpath="/home/sgongora/hcss/workspace/Red_Leak/pools/Export414880784329918512DIR/1342199235",
         archive="/home/sgongora/hcss/workspace/Red_Leak/pools/1342199235_1.tgz", compression="TGZ")
time_2 = time.time()
final_time_tgz_hipe = time_2 - time_1


# Regular export, regular tar compression
time_3 = time.time()
exportObservation(pool=PoolManager.getPool('1342199235'),
                  urn="urn:1342199235:herschel.ia.obs.ObservationContext:0",
                  dirout="/home/sgongora/hcss/workspace/Red_Leak/pools/Export299327940458401311DIR/1342199235")
compress(inputpath="/home/sgongora/hcss/workspace/Red_Leak/pools/Export299327940458401311DIR/1342199235",
         archive="/home/sgongora/hcss/workspace/Red_Leak/pools/1342199235_2.tar", compression="TAR")
time_4 = time.time()
final_time_tar_hipe = time_4 - time_3


# Regular export, shutil tar.gz compression
time_5 = time.time()
exportObservation(pool=PoolManager.getPool('1342199235'),
                  urn="urn:1342199235:herschel.ia.obs.ObservationContext:0",
                  dirout="/home/sgongora/hcss/workspace/Red_Leak/pools/1342199235_3");
shutil.make_archive(pool_dir + '1342199325_3', 'gztar',
                    pool_dir, '1342199235_3')
time_6 = time.time()
final_time_tgz_shutil = time_6 - time_5


# Regular export, shutil tar compression
time_7 = time.time()
exportObservation(pool=PoolManager.getPool('1342199235'),
                  urn="urn:1342199235:herschel.ia.obs.ObservationContext:0",
                  dirout="/home/sgongora/hcss/workspace/Red_Leak/pools/1342199235_4");
shutil.make_archive(pool_dir + '1342199325_4', 'tar',
                    pool_dir, '1342199235_4')
time_8 = time.time()
final_time_tar_shutil = time_8 - time_7

print "final time with tgz compression: ", final_time_tgz_hipe
print "final time with tar format: ", final_time_tar_hipe
print "final time with export and python tgz: ", final_time_tgz_shutil
print "final time with export and python tar: ", final_time_tar_shutil
