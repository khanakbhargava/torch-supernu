# Converts SuperNu outputs (wavelengths and luminosity) into SNID format

import math
import numpy as np

sourceFileWV = input("Enter the source file path for the WAVELENGTHS: ")    # type full path names!!
sourceFileFLX = input("Enter the source file path for the FLUX/LUMINOSITY: ")   # ex: [ /home/mcken/Research/file_name ]
newfile = input("Enter the source file PATH and NAME for the OUTPUT file: ")  # end filename in .dat
day = input("What epoch of flux are you interested in?: ")           # choose line of flux data (10th epic is line 17)

wvData = []                                     # set list for wavelengths
flxData = []                                    # set list for flux
wvDataMod = []                                  # set list for modified wavelengths (not used if not limiting range)


# find the values of the wavelengths from the source file
inFileWV = open(sourceFileWV, "r")              # open and read source file , encoding='utf-8'
wavelengthValues = inFileWV.readlines()         # reading all lines of file
wavelengths = wavelengthValues[1]               # only read first uncommented line of file w/ wvlngths
data = wavelengths.split()                      # split string of line 1 into long string
data.pop(0)

# appending wavelengths from strings to wvData list as floats
for i in range(len(data)):                      # run through range of string
    wvData.append(float(data[i]))               # turn values of string into floats for list wvData
inFileWV.close()
print("original values of wavelengths (cm): ", wvData)  # print values of wvData to console

# converting values of wavelengths from cm to angstroms
for i in range(len(data)):
    wvData[i] = (wvData[i]) * (10 ** 8)         # conversion from cm to A
print("converted values of wavelengths (Angstrom): ", wvData)

# Finding PEAK brightness line and total max flux
lineNum = input("Number of lines in luminos file: ")    # number of lines in ---.flx_luminos file

dlambda = (6.8 * (10 ** -8))                   # bin size
flxData = []
a = []

for i in range(0, int(lineNum)):                # number of lines (lineNum)
    inFileFLX = open(sourceFileFLX, "r")        # opening file
    fluxValues = inFileFLX.readlines()          # reading lines of flux/luminosity
    flux = fluxValues[i]                        # grabbing line of flux for each line
    data = flux.split()                         # splitting values
    for j in range(len(data)):
        flxData.append(float(data[j]))          # adding values from line to new array as floats
    sumNum = sum(flxData)  # * dlambda           summing array of float values, and * by dlambda
    a.append(sumNum)                            # appending total flux value to diff array
    flxData = []                                # clearing array for next i-value

maxElement = np.amax(a)                         # defining max total flux value from 'a' array
print('Max total value of flux : ', maxElement)  # printing ^

result = np.where(a == np.amax(a))              # locating max total flux value in array
print('Returned tuple of arrays :', result)     # returning array value (array starts at 0 so below adds 1)
print('Peak Brightness Line :', result[0]+1)    # printing array value as peak brightness line

print("Max Total Values of flux for file: ", a)
print("Number of Lines read: ", len(a))

# indexValue = day - 1
dayMaxValue = a[int(day)-1]
meanPeak = dayMaxValue / 500                     # normalization number using peak bright. and bin size


# finding values of flux from source file
inFileFLX = open(sourceFileFLX, "r")
fluxValues = inFileFLX.readlines()
flux = fluxValues[int(day)-1]
data = flux.split()
for p in range(len(data)):
    flxData.append(float(data[p]))                              # changing from string to float

print("values of flux for epoch " + str(day) + ": " + flux)
for k in range(len(flxData)):
    # flxData[k] = (flxData[k]) * (10 ** -8)              # applying conversion to avoid overflow MULTIPLY BY 6.8
    flxData[k] = (flxData[k]) / meanPeak               # CHANGED FROM ABOVE TO THIS LINE
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
    for y in range(len(wvData)):                                 # using length of values of WVs (wvDataMod)
        write_buffer = str(wvData[y]) + "  " + str(flxData[y])   # printing the conv. values of wvData (wvDataMod)
        f.writelines(write_buffer)
        f.writelines("\n")
        print(write_buffer)                                      # printing values to new file

"""maxFlxVar = 0
maxFlx = []
listlength = flxData
flxData.append(flxData[0])
for y in range(len(wvData)):
    for x in range(len(listlength)-1):
        maxFlxVar = flxData[x]
        if (flxData[x] < flxData[x+1]) or (flxData[x] == flxData[x+1]):
            maxFlxVar = flxData[x+1]
        elif (flxData[x] > flxData[x+1]):
            maxFlxVar = flxData[x]
    maxFlx.append(maxFlxVar)


print(maxFlx)
print(len(maxFlx)) 

maxFlxVal = 0
for x in range(len(flxData)-1):
    if flxData[x] >= flxData[x+1]:
        maxFlxVal = flxData[x]
    elif flxData[x] < flxData[x+1]:
        maxFlxVal = flxData[x+1]

print(maxFlxVal)

days = [13, 30, 39, 47, 65, 82]
values = []
for x in range(len(days)):
    values = np.array([wvData[x],flxData[x]])

values = np.array([flxData])
print(values)"""
