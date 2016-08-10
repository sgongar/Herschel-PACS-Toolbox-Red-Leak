home_dir = os.getenv("HOME")
working_dir = str(home_dir) + '/hcss/workspace/Red-Leak/'
pool_dir = str(working_dir) + 'pools/'

obsid = 1342246381
obs = getObservation(obsid, useHsa=1)
# replace product with MapContext
runPacsSpg(obsIn=obs, cameraList=['red'])

poolName='1342246381_obsContext'

tag=poolName
saveProduct(product=obs, pool=poolName, poolLocation=pool_dir, tag=tag)
# saveObservation(obs, poolName=poolName, poolLocation=pool_dir)

# Then we export it with the HSA hierarchichal structure
# This is a mix of John Cook CJ style (without Metaquery) and HIFI style:
dataPool = LocalStoreFactory.getStore(LocalStoreContext(poolName, pool_dir))
storage = ProductStorage(dataPool)
urn = storage.getUrnFromTag(tag)

# the only thing one can export in an HSA hierarchichal structure is a complete obsContext
exportObservation(pool=PoolManager.getPool(poolName), urn=urn, dirout=pool_dir+poolName+'_HSAStruct', warn=True)
