#This script calculate the relative change in velocty for all particles at two given times. Note, this script only works for the Flash runs that do not lose any particles. 

import h5py
import math
import glob
import numpy as np

#Give path to particle files
files = glob.glob("/scratch/07441/kbhargav/part_file_rot_flame_super/rot_flame_det_hdf5_part_00000[0-8]")
#00[0-5][0-9][0-9][0-9]")
files.sort()

#Getting total number of particles from the first file
p_file = h5py.File(files[0],'r')
dset = p_file['tracer particles']
array1 = np.transpose(dset)
nparticles = array1.shape[1]

#Getting total number of files
nfiles = len(files)

#Creating arrays to store data
time = np.zeros([nparticles,nfiles], dtype = float)
temp = np.zeros([nparticles,nfiles], dtype = float)
dens = np.zeros([nparticles,nfiles], dtype = float)
vel_x = np.zeros([nparticles,nfiles], dtype = float)
vel_y = np.zeros([nparticles,nfiles], dtype = float)
vel = np.zeros([nparticles,nfiles], dtype = float)
rel_change = np.zeros(nparticles)
v1 = np.zeros(nparticles)
v2 = np.zeros(nparticles)

t1 = 3.6e-4
t2 = 1.5e-3

verbose1 = 0
verbose2 = 0

#Reading data from particle files
for f,file in enumerate(files):
    p_file = h5py.File(file,'r')
    dset = p_file['tracer particles']
    array1 = np.transpose(dset)
    array2 = np.asarray(p_file['real scalars'])
    for i in range(nparticles):
        ind = int(array1[11][i]) - 1
        time[ind][f] = float(array2[1][1])
        dens[ind][f] = float(array1[1][i])
        temp[ind][f] = float(array1[12][i])
        vel_x[ind][f] = float(array1[13][i])
        vel_y[ind][f] = float(array1[14][i])
        vel[ind][f] = float(math.sqrt(vel_x[ind][f]**2 \
            + vel_y[ind][f]**2))
        if f == 0:
           dt1 = abs(float(time[ind][f] - t1))
           dt2 = abs(float(time[ind][f] - t2))
        if f != 0:
           dt1_ = abs(float(time[ind][f] - t1))
           dt2_ = abs(float(time[ind][f] - t2))
           if dt1_ > dt1 and verbose1 == 0:
              index1 = f - 1
              verbose1 = 1
           if dt2_ > dt2 and verbose2 == 0:
              index2 = f - 1 
              verbose2 = 1
           dt1 = dt1_
           dt2 = dt2_
p_file.close()


for p in range(nparticles):
    history = "tempdens" + str(p+1) + ".dat"
    with open(history, 'w') as d:
       np.savetxt(d,np.c_[time[p],temp[p],dens[p],vel_x[p],\
          vel_y[p],vel[p]], fmt='%1.5e %1.5e %1.5e %1.5e %1.5e %1.5e')
       d.write('\n')
    v1 = vel[p][index1]
    v2 = vel[p][index2]
    rel_change[p] = abs(v2 - v1)/v2
    with open('deviations.dat','a') as f:
        f.write('%d %e' %(p+1, rel_change[p]))
        f.write('\n')

