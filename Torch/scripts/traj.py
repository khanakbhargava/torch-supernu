import h5py
import glob
import numpy as np

#Give path to particle files
files = glob.glob("/home/kbhargava/ddt_off_imp_files_stampede_noperturbation/ddt_off_hdf5_part_*")
files.sort()

indices = []
miss = []
print(len(files))

file = h5py.File(files[-1],"r")
print(file)
row1, column1 = file["tracer particles"].shape
for j in range(row1):
	indices.append(int(file["tracer particles"][j][11]))
	
for j in range(9997):	
	if (j+1) in indices:
		continue
	else:
		miss.append(j+1)

print('Got the missing indices', miss)

print('indices len:',len(indices))
nfiles = len(files)
nparticles = 9997

print('Creating arrays to store data')
time = np.zeros([nparticles,nfiles], dtype = float)
temp = np.zeros([nparticles,nfiles], dtype = float)
dens = np.zeros([nparticles,nfiles], dtype = float)

print('#Reading data from particle files')
for f,file in enumerate(files):
	p_file = h5py.File(file,'r')
	dset = p_file['tracer particles']
	array1 = np.transpose(dset)
	array2 = np.asarray(p_file['real scalars'])
	column2 = array1.shape[1]
#	print(column2)
	for i in range(column2):
		ind = int(array1[11][i])
		if (ind in miss):
			continue
		else:
			time[ind-1][f] = float(array2[1][1])
			dens[ind-1][f] = float(array1[1][i])
			temp[ind-1][f] = float(array1[12][i])
	#print('Finished reading' + str(f+1) + 'file')
	p_file.close()

print('Creating .dat trajectory files for Torch')

for p in indices:
	history = "tempdens" + str(p) + ".dat"
	np.savetxt(history,np.c_[time[p-1],temp[p-1],dens[p-1]], fmt='%1.5e')

