### This script will get final velocities of tracer particles from FLASH particle data and save them in a new file 'flash.dat'

import numpy as np
import h5py

nfiles = 1
nparticles = 10002

velx = np.zeros([nparticles,nfiles], dtype = float)
vely = np.zeros([nparticles,nfiles], dtype = float)
temp = np.zeros([nparticles,nfiles], dtype = float)

#Give name of the last particle file that reppresents the final time

part = "pure_det_hdf5_part_004838"
p_file = h5py.File(part,'r')
dset = p_file['tracer particles']
array1 = np.transpose(dset)
for i in range(nparticles):
    ind = int(array1[11][i]) - 1
    velx[ind][f] = float(array1[13][i])
    vely[ind][f] = float(array1[14][i])
    temp[ind][f] = float(array1[12][i])
    print("Reading file " + part + "has completed...")
p_file.close()

for p in range(nparticles):
    np.savetxt("flash.dat" ,np.c_[velx[p],vely[p],temp[p]], fmt='%1.5e')
