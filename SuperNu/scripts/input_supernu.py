import numpy as np
import maxmin as mm

Np = 9994  #Number of trajectories/particles we want to map
tmass = 2.740524572011647076E+33 #Total mass of the system
mass = tmass/9994 # Mass of one particle

data = np.zeros([51, Np], dtype = float) #This array will store velocities and abundances for all Np particles

f = open('final_vel.dat','r')
for i in range(Np):
      line = f.readline()
      lst = line.split()
      data[0][i] = float(lst[0]) # Reading v_r for all Np particles
      data[1][i] = float(lst[1]) # Reading v_z for all Np particles
f.close()

f = open('abundance.dat','r')
#f.readline()
for i in range(Np):
    line = f.readline()
    lst = line.split()
    #print(lst)
    for j in range(49):
        data[j+2][i] = float(lst[j]) #Reading 30 abundances for all Np particles
f.close()


arr = []
arr = mm.maxmin('final_vel.dat') #This will find the max and min velocities that will fix the range for x and y axes of the mesh

vr_max = arr[0]
vz_max = arr[1]
vz_min = arr[2]

x = np.linspace(0, vr_max, 33)
#y = np.linspace(vz_min, vz_max, 65) 
y = np.linspace(-(vz_max), vz_max, 65) #To make mesh symmetric

f = open('input.str','w')
f.write('# 2D cylindrical LDEN hot envelope model')
f.write('\n')
f.write('# 32 64 1 54 49')
f.write('\n')
f.write('#'+'\t' +'x_left'+'\t\t'+'x_right'+'\t\t\t'+'y_left'+'\t\t'+'y_right'+'\t\t\t'+'mass'+\
'\t\t'+'H'+'\t\t\t'+'He'+'\t\t\t'+'Li'+'\t\t\t'+'Be'+'\t\t\t'+'B'+'\t\t\t'+'C'+'\t\t\t\t'+'N'+\
'\t\t\t\t'+'O'+'\t\t\t'+'F'+'\t\t\t'+'Ne'+'\t\t\t'+'Na'+'\t\t\t'+'Mg'+'\t\t\t'+'Al'+\
'\t\t\t\t'+'Si'+'\t\t\t'+'P'+'\t\t\t'+'S'+'\t\t\t'+'Cl'+'\t\t\t'+'Ar'+'\t\t\t'+'K'+'\t\t\t\t'+\
'Ca'+'\t\t\t\t'+'Sc'+'\t\t\t'+'Ti'+'\t\t\t'+'V'+'\t\t\t'+'Cr'+'\t\t\t'+'Mn'+'\t\t\t\t'+'Fe'\
+'\t\t\t'+ 'Co'+'\t\t\t'+'Ni'+'\t\t\t'+'Cu'+'\t\t\t'+'Zn'+'\t\t\t'+'Ga'+'\t\t\t'+'Ge'+'\t\t\t'+ 'As'+ '\t\t\t' +\
'Se'+'\t\t\t\t' + 'Br' + '\t\t\t'+ 'Kr' + '\t\t\t' + 'Rb' + '\t\t\t' + 'Sr' +'\t\t\t' + 'Y' + '\t\t\t' + 'Zr' + \
'\t\t\t' + 'Nb' +'\t\t\t' + 'Mo' +'\t\t\t' +'Tc' + '\t\t\t' +'Ni56'+'\t\t\t'+'Co56'+\
'\t\t\t'+'Fe52'+'\t\t\t'+'Mn52'+'\t\t\t'+'Cr48'+'\t\t\t'+'V48')
f.write('\n')

for i in range(64):
    y_left = y[i]
    y_right = y[i+1]
    for j in range(32):
       smass = 0 #Resetting sum of mass for every new cell
       sabund = np.zeros([1,49], dtype = float) #Resetting sum of abundances for every cell
       x_left = x[j]
       x_right = x[j+1]
       count = 0 # Keeps track of no of particle in each velocity bin.
       for k in range(Np):
            if(data[0][k] >= x_left and data[0][k] < x_right) and (data[1][k] >= y_left and data[1][k] < y_right): #Checking if particle fits the range of cell
               smass += mass #Mass of cell will increase with addition of a particle
               count += 1
               for l in range(49):
                  sabund[0][l] += data[l+2][k]
       if(count != 0):
            sabund = sabund / count 
       f.write('%e %e %e %e %e' %(x_left, x_right, y_left, y_right,smass))
       np.savetxt(f, sabund, fmt =' %1.5e')
f.close()
