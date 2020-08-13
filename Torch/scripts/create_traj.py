import numpy as np
import h5py

nfiles = 4839
nparticles = 10002  # Can you get this from the first data file without
                    #  hardcoding it?

time = np.zeros([nparticles,nfiles], dtype = float)
temp = np.zeros([nparticles,nfiles], dtype = float)
dens = np.zeros([nparticles,nfiles], dtype = float)

#rtf Instead of doing a loop, why not do a glob? This will both simplify
#   the code. Further, I can envision cases where a glob will work
#   and this code will not -- for example, if one has only every N
#   files for a quick analysis

for f in range(nfiles):
    if(f <10):
        part = "pure_det_hdf5_part_00000" + str(f)
    elif(f >= 10) and (f<= 99):
        part = "pure_det_hdf5_part_0000" + str(f)
    elif(f >= 100) and (f<= 999):
        part = "pure_det_hdf5_part_000" + str(f)
    elif(f >= 1000):
        part = "pure_det_hdf5_part_00" + str(f)
    p_file = h5py.File(part,'r')
    dset = p_file['tracer particles']
    array1 = np.transpose(dset)
    #dset = p_file['real scalars']
    #array2 = dset[()]
    array2 = np.asarray(p_file['real scalars'])
    for i in range(nparticles):
        ind = int(array1[11][i]) - 1
#rtf Need some comments here to clarify precisely how you are 
#     extracting the data.
        time[ind][f] = float(array2[1][1])
        dens[ind][f] = float(array1[1][i])
        temp[ind][f] = float(array1[12][i])
    print("Reading file " + part + "has completed...")
    p_file.close()

# Don't we need velocity information for SuperNu?

for p in range(nparticles):
    history = "tempdens" + str(p+1) + ".dat"
    np.savetxt(history,np.c_[time[p],temp[p],dens[p]], fmt='%1.5e')
    print("History for particle # "+str(p+1)+" written...")
