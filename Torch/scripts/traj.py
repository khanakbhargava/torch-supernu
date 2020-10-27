## This is a generalized script that can also create trajectories for models that lose particles

import h5py
import glob

files = glob.glob("/scratch/07441/kbhargav/hot_en_traj/particle_data_rot_hot_envelope/rot_flame_det_4km_hdf5_part_0[0-1][0-9][0-9][0-9][0-9]")
files.sort()

#print(len(files))

time = []
temp = []
dens = []

indices = []

file = h5py.File(files[18316],"r")
row1, column1 = file["tracer particles"].shape
for j in range(row1):
    indices.append(int(file["tracer particles"][j][11]))

#print(row1,column1)
#print(indices)

for i in range(len(files)):
    time.append({0:"Time%s"%(i)})
    temp.append({0:"Temp%s"%(i)})
    dens.append({0:"Density%s"%(i)})
    file = h5py.File(files[i],"r")
    row, column = file["tracer particles"].shape
    for j in range(row):
         ptag = int(file["tracer particles"][j][11])
         if (ptag in indices):
              time[i].update({ptag : str(file["real scalars"][1][1])})
              temp[i].update({ptag : str(file["tracer particles"][j][12])})
              dens[i].update({ptag : str(file["tracer particles"][j][1])})

#print(str(time[0][indices[i]]))

#for i in range(len(files)):
#for ptag  in indices:
#    ptag = indices[j]
#    history = "tempdens" + str(ptag) + ".dat"
#    print(history)
#    with open(history,'a') as f: 
         #for j in range(len(files)):
         #     !time1 = float(time[j][ptag])
         #     !temp1 = float(temp[j][ptag])
         #     !dens1 = float(dens[j][ptag])
#         f.write('%e %e %e' %(time[i][ptag], temp[i][ptag], dens[i][ptag]))
#         f.write('\n')

for ptag in indices:
    history = "tempdens" + str(ptag) + ".dat"
    with open(history, 'w') as f:
         for i in range(len(files)):
              #f.write(str(time[i][ptag]) + '\t\t\t' + str(temp[i][ptag]) + '\t\t\t' + str(dens[i][ptag]))
              time1 = float(time[i][ptag])
              temp1 = float(temp[i][ptag])
              dens1 = float(dens[i][ptag])
              #f.write('%s %s %s' %(time[i][ptag], temp[i][ptag], dens[i][ptag]))
              f.write('%e %e %e' %(time1, temp1, dens1))
              f.write('\n')
