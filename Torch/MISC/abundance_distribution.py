###This script can be used to plot the pos_x and pos_y and then 
###scheme the particles by their abundances distribution.

import numpy as np
import matplotlib.pyplot as plt
import glob as glob


plt.style.use('dark_background')

# to read the pos_ and pos_y
with open('/work/07258/aalshafi/stampede2/pipeline/data_Nir_Kha/testtime.dat', 'r') as f:
    lines = f.readlines()
    size=len(lines)
    x = [float(line.split()[0]) for line in lines] # will read the column one
    y = [float(line.split()[1]) for line in lines] # will read the column two
    s=[3] # the size of the particle on the plot
    
x = np.array(x)
#print(x)


y= np.array(y)
color_array=[]

c12_app= [] #empty list to stor the c12
o16_app= [] #empty list to stor the o16
si28_app= [] #empty list to stor the si28
#print(size)
# to read the abundances and shade the particles 
for p in range(size):
    f='/work/07258/aalshafi/stampede2/pipeline/Torch/final_abundances/out_'+str(p+1)+'_final.dat'
    file=open(f, 'r')
    abundance=file.readlines()
    #print('file', file)
    # To append the atom. baryon, and mass fraction to empty lists
    atom_number=[] # to append the atomic number from the abundance files
    baryon_number=[] # to append the baryon number from the abundance files
    mass_fraction=[] # to append the mass fraction from the abundance files
    # this loop to read the columns from the abundance files
    for w in abundance:
        line = w.split()
        atom_number.append(int(line[0]))
        baryon_number.append(int(line[1]))
        mass_fraction.append(float(line[2]))
        
    
    #print ('ato', atom_number)
    #print ('bar', baryon_number)
    #print ('mass', mass_fraction)
    #print ('isotope', isotope_symbols)
    
    # to calssfiy the baryon number to empity lists according to the colors that we want
    green_app= 0
    blue_app= 0
    red_app= 0
    white_app= 0

    for j in range (229):      # 229 is the number of the line in every abundance file
        #The white color represents 56Ni, and the green, blue, and red colors in 
        #the figure represent isotopes with A <= 16, intermediate-mass isotopes with 16 < A <= 40, 
        #and iron-peak isotopes for all A > 40 (except 56Ni) respectively
        if(baryon_number[j] <= 16):
            green_app += mass_fraction[j]
        elif (baryon_number[j] > 16 and baryon_number[j] <= 40):
            blue_app += mass_fraction[j]
        elif (baryon_number[j] > 40 and (atom_number[j] != 28 or baryon_number[j] != 56)):
            red_app += mass_fraction[j]
        else:
            white_app = mass_fraction[j]
    
    # To find the max abundances for C12, O16, and Si28
    for k in range (229):
        if (baryon_number[k] == 12 and atom_number[k] == 6):
            c12_app.append(mass_fraction[k])
        elif (baryon_number[k] == 16 and atom_number[k] == 8):
            o16_app.append(mass_fraction[k])
        elif (baryon_number[k] == 28 and atom_number[k] == 14):
            si28_app.append(mass_fraction[k])
       
        
    #print('green_app', green_app)
    #print('blue_app', blue_app)
    #print('red_app', red_app)
    #print('white_app', white_app)
    #print ('c12_app', c12_app)
    #print ('o16_app', o16_app)
    #print ('si28_app', si28_app)

    color_max = np.zeros(4)

    color_max[0] = green_app
    color_max[1] = blue_app
    color_max[2] = red_app
    color_max[3] = white_app
    #print('green', color_max[0])
    #print('blue', color_max[1])
    #print('red', color_max[2])
    #print('white', color_max[3])
    
    # Max value
    color_ind = np.argmax(color_max)
    #print('color_ind', color_ind)
    res_max_c12 = max(float(sub) for sub in c12_app)
    res_max_o16 = max(float(sub) for sub in o16_app) 
    res_max_si28 = max(float(sub) for sub in si28_app) 


    if color_ind == 0:
        color_array.append('g')
    elif color_ind == 1:
        color_array.append('b')
    elif color_ind == 2:
        color_array.append('r')
    else:
        color_array.append('w')
        

color_array= np.array(color_array, dtype=object)
#print('color_array', color_array)



print('max_c12', res_max_c12)
print('max_o16', res_max_o16)
print('max_si28', res_max_si28)
plt.figure(figsize=(10,20))
plt.xlabel('r(cm)', fontsize=18)
plt.ylabel('z(cm)', fontsize=18)
plt.title('last time step 1.9 s', fontsize=18)
plt.xlim(0, 13e9)
plt.ylim(-13e9, 13e9)
plt.scatter(x, y, s, c= color_array)
plt.savefig('afteredit')
