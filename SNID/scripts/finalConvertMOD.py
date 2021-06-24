# Converts SuperNu outputs (wavelengths and luminosity) into SNID format

import math

sourceFileWV = input("Enter the source file path for the WAVELENGTHS: ")    # type full path names!!
sourceFileFLX = input("Enter the source file path for the FLUX/LUMINOSITY: ")   # ex: [ /home/mcken/Research/file_name ]
newfile = input("Enter the source file PATH and NAME for the OUTPUT file: ")  # end filename in .dat
day = input("What epoch of flux are you interested in?: ")             # choose line of flux data (10th epic is line 17)

wvData = []                                     # set list for wavelengths
flxData = []                                    # set list for flux
wvDataMod = []                                  # set list for modified wavelengths (not used if not limiting range)
D = 3.086e26

# find the values of the wavelengths from the source file
inFileWV = open(sourceFileWV, "r")              # open and read source file , encoding='utf-8'
wavelengthValues = inFileWV.readlines()         # reading all lines of file
wavelengths = wavelengthValues[1]               # only read first uncommented line of file w/ wvlngths
data = wavelengths.split()                      # split string of line 1 into long string
data.pop(0)

# appending wavelengths from strings to wvData list as floats
for i in range(len(data)):                      # run through range of string
    wvData.append(float(data[i]))               # turn values of string into floats for list wvData
#wvData.pop(0)
inFileWV.close()
print("original values of wavelengths (cm): ", wvData)  # print values of wvData to console

# converting values of wavelengths from cm to angstroms
for i in range(len(data)):
    wvData[i] = (wvData[i]) * (10 ** 8)         # conversion from cm to A
print("converted values of wavelengths (Angstrom): ", wvData)

# finding values of flux from source file
inFileFLX = open(sourceFileFLX, "r")
fluxValues = inFileFLX.readlines()
flux = fluxValues[int(day)]
data = flux.split()
for i in range(len(data)):
    flxData.append(float(data[i]))                              # changing from string to float

print("values of flux for epic " + str(day) + ": " + flux)
for k in range(len(flxData)):
    flxData[k] = (flxData[k]) * (10 ** -8)                     # applying conversion to avoid overflow
    #flxData[k] = (flxData[k]) / (4 * math.pi * D ** 2)          # DIFFERENT CONVERSION
print("modified values of flux for epic " + str(day) + ": ")    # printing mod. values to console


# limiting range of wavelengths to 2,500 to 20,000 angstroms (newer templates) ---- unneeded
"""for z in range(len(wvData)):
    if wvData[z] < 2500 or wvData[z] > 10000:                   # this limits wavelengths to 2500 to 20000 A
        continue                                                # could be modified to fix PGPLOT graph in SNID
    else:
        wvDataMod.append(wvData[z])"""                          # this still shows some errors, so be careful if using


print(wvData)                                                   # change to wvDataMod if limiting range
q = len(wvData)
r = len(flxData)
print("bin sizes: ", q, r)

# printing values to SNID-formatted file
with open(newfile, 'w') as f:
    for j in range(len(wvData)):                                 # using length of values of WVs (wvDataMod)
        write_buffer = str(wvData[j]) + "  " + str(flxData[j])   # printing the conv. values of wvData (wvDataMod)
        f.writelines(write_buffer)
        f.writelines("\n")
        print(write_buffer)                                      # printing values to new file
