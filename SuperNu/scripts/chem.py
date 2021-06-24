### This script will convert isotope abundances from Torch to chemical abundances and write to a new file 'abundance.dat'.
### By: Sudarshan Neopane

import numpy as np
    
nfiles = 1 #No. of total particles to be mapped

nelements = 32 # No. of elements to be included

nisotopes = 6 # No. of isotopes to be included

fin = open('abundance.dat','ab')

for f in range(nfiles):
    filename = 'out_' + str(f+1) + '_final.dat'
    file = open(filename,"r") # Open the file
    file_length = file.readlines() #Array of lines in file

    atomic_number = [] # Array stores the atomic numbers
    baryon_number = [] # Array to store baryon number
    mass_fraction = [] # Arrya to store mass fraction
    isotope_array = [] # 2D array with indices of isotopes grouped together
    atomic_number_array = []
    baryon_number_array = [] # 2D array with baryon number grouped together
    mass_fraction_array = [] # 2D array with mass fraction grouped together
    all_mass_fraction = np.zeros(int(nelements + nisotopes)) # output from the function (mass fractions)


    for line in file_length: # Loop over all the lines
        lst = line.split() # Split each line into a list
        atomic_number.append(int(lst[0])) # Storing Values
        baryon_number.append(int(lst[1])) # '' ''
        mass_fraction.append(float(lst[2])) # '' ''

    file.close() # Close the file

    atomic_number = np.array(atomic_number) # Convert to numoy array
                
    for i in range(nelements):
        array = np.where(atomic_number == i+1) # Find the elements with specific atomic number
        isotope_array.append(array[0]) # Genertaing a 2D list
        
    isotope_array = np.array(isotope_array, dtype = object) # Convert to numpy array


    # Remove proton from the array list
    # isotope_array[0] = isotope_array[0][:-1]
    # print(isotope_array[0])

    for a in range(nelements): # Specifies the atomic number of element
        empty_atomic = []
        empty_baryon = [] # List to store Baryon number array for paticular element
        empty_fraction = [] # List yo store mass fraction array for paticular element
        
        for b in isotope_array[a]:
            empty_atomic.append(atomic_number[b])
            empty_baryon.append(baryon_number[b]) 
            empty_fraction.append(mass_fraction[b])
            
        atomic_number_array.append(np.array(empty_atomic))    
        baryon_number_array.append(np.array(empty_baryon)) # 2D list being created
        mass_fraction_array.append(np.array(empty_fraction)) # 2D list being created
        
    atomic_number_array = np.array(atomic_number_array, dtype = object)
    baryon_number_array = np.array(baryon_number_array, dtype = object) # Convert to numpy array
    mass_fraction_array = np.array(mass_fraction_array, dtype = object) # Convert to numpy array

    #########################################################################################
    for j in range(nelements):    # Storing all the 32 elements
        #all_mass_fraction[j] = (sum(atomic_number_array[j]*\
        #                           mass_fraction_array[j]))\
        #                       /sum(atomic_number_array[j])
        all_mass_fraction[j] = sum(mass_fraction_array[j])
    # Above change was made beacuse in input, we need Ni > Ni56        
            
    ##########################################################################################  
    # Store Ni 56, Co 56, Fe 52, Mn 52, Cr 48, and V 48 in the array
    # As nisotopes = 6
    all_mass_fraction[32] = mass_fraction_array[27][0]
    all_mass_fraction[33] = mass_fraction_array[26][1]
    all_mass_fraction[34] = mass_fraction_array[25][0]
    all_mass_fraction[35] = mass_fraction_array[24][1]
    all_mass_fraction[36] = mass_fraction_array[23][0]
    all_mass_fraction[37] = mass_fraction_array[22][3]
    
    np.savetxt(fin,all_mass_fraction, newline=' ', delimiter= ',')
    fin.write(b"\n")
    
fin.close()
#print(all_mass_fraction)
#print(sum(all_mass_fraction[:-6]))
