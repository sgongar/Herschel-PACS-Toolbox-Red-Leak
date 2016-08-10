home_dir = os.getenv("HOME")
working_dir = str(home_dir) + '/hcss/workspace/Red-Leak/'
pool_dir = str(working_dir) + 'pools/'

# /home/sgongar/hcss/workspace/Red-leak/pools/obs_1342186305

obsid = 1342246381
obs = getObservation(obsid, useHsa=1)
# replace product with MapContext
runPacsSpg(obsIn=obs)

poolName='1342246381_obsContext'
# pool_dir='/home/epuga/PACS/PACS_HPDPs/redLeak/'
tag=poolName
# First we save the level2 in a standard pool structure
saveProduct(product=obs, pool=poolName, poolLocation=pool_dir, tag=tag)
saveObservation(obs, poolName=poolName, poolLocation=pool_dir)
#better to have a tag

# Then we export it with the HSA hierarchichal structure
# This is a mix of John Cook CJ style (without Metaquery) and HIFI style:
dataPool = LocalStoreFactory.getStore(LocalStoreContext(poolName, pool_dir))
storage = ProductStorage(dataPool)
urn = storage.getUrnFromTag(tag)

#the only thing one can export in an HSA hierarchichal structure is a complete obsContext
exportObservation(pool=PoolManager.getPool(poolName), urn=urn, dirout=pool_dir+poolName+'_HSAStruct', warn=True)
#exportObservation(pool=PoolManager.getPool(poolName), dirout=pool_dir+poolName+'_HSAStruct', warn=True)