### This script will convert isotope abundances from Torch to chemical abundances and write to a new file 'abundance.dat'.
### By: Sudarshan Neopane

import numpy as np
    
atomic_number = [] # Array stores the atomic numbers
baryon_number = [] # Array to store baryon number
mass_fraction = [] # Arrya to store mass fraction
isotope_array = [] # 2D array with indices of isotopes grouped together
baryon_number_array = [] # 2D array with baryon number grouped together
mass_fraction_array = [] # 2D array with mass fraction grouped together
all_mass_fraction = np.zeros(30) # output from the function (mass fractions)

nfiles = 100

fin = open('abundance.dat'.'w')

for f in range(nfiles):
    filename = 'out_' + str(f+1) + '_final.dat'
    file = open(filename,"r") # Open teh file
    file_length = file.readlines() #Array of lines in file

    for line in file_length: # Loop over all the lines
        lst = line.split() # Split each line into a list
        atomic_number.append(int(lst[0])) # Storing Values
        baryon_number.append(int(lst[1])) # '' ''
        mass_fraction.append(float(lst[2])) # '' ''

    file.close() # Close the file

    atomic_number = np.array(atomic_number) # Convert to numoy array
                
    for i in range(32):
        array = np.where(atomic_number == i+1) # Find the elements with specific atomic number
        isotope_array.append(array[0]) # Genertaing a 2D list
        
    isotope_array = np.array(isotope_array, dtype = object) # Convert to numpy array


    # Remove proton from the array list
    # isotope_array[0] = isotope_array[0][:-1]
    # print(isotope_array[0])

    for a in range(32): # Specifies the atomic number of element
        empty_baryon = [] # List to store Baryon number array for paticular element
        empty_fraction = [] # List yo store mass fraction array for paticular element
        
        for b in isotope_array[a]:
            empty_baryon.append(baryon_number[b]) 
            empty_fraction.append(mass_fraction[b])
            
        baryon_number_array.append(np.array(empty_baryon)) # 2D list being created
        mass_fraction_array.append(np.array(empty_fraction)) # 2D list being created

    baryon_number_array = np.array(baryon_number_array, dtype = object) # Convert to numpy array
    mass_fraction_array = np.array(mass_fraction_array, dtype = object) # Convert to numpy array

    #########################################################################################
    for j in range(28):    # JUst need first 28 elemnets
        all_mass_fraction[j] = (sum(baryon_number_array[j]*\
                                    mass_fraction_array[j]))\
                                /sum(baryon_number_array[j])
            
            
    ##########################################################################################  
    # Store Ni 56 and Co 56 in the array
    all_mass_fraction[28] = mass_fraction_array[27][0]
    all_mass_fraction[29] = mass_fraction_array[26][1]
    fin.write(all_mass_fraction)

fin.close()
