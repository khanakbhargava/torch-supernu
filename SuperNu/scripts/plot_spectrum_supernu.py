# A short script to plot the time-dependent spectrum from supernu

# plot_spectrum_supernu.py

import math
import numpy as np
import matplotlib.pyplot as plt

# Verbosity flag (set to verbose by default)

verbose = 1
line_toread = 24

# Open the ASCII file containing the time information

f = open ('output.tsp_time')

times = []

for line in f:
        strippedline = line.strip()
        if strippedline.startswith("#") :
                if (verbose == 1) :
                        print line,
        else :
# Split the line of data into fields
                lst = line.split()
# Convert line information from ASCII to floats
		times.append (float (lst [0]))
f.close ()

# Open the ASCII file containing the wavelength information

f = open ('output.flx_grid')
# Header line
line = f.readline()
line = f.readline()
lst = line.split()
wavelength = [float (i) for i in lst]
f.close ()

wavelength.pop (0)

wavearr = np.asarray (wavelength) * 1.e8
#wavearrmin1 = np.roll (wavearr, 1)

# Get centered wavelength values; cut leading entry
#xaxis = wavearr + (wavearr - wavearrmin1) / 2.
#xaxis = np.delete (xaxis, 0)

#print "Size of wavelength array = ", len (xaxis)

# Open the ASCII file containing the spectral data

f = open ('output.flx_luminos')

spec = [None] * 150
j = 0

for line in f:
	if line.startswith("#") :
		if (verbose == 1) :
			print line,
	else :
# Split the line of data into fields
		lst = line.split()
# Convert line information from ASCII to floats
		spec [j] = [float(i) for i in lst]
		j = j + 1

#print spec [line_toread]

specarray = np.asarray (spec [line_toread] )
#specarray = np.log (specarray) / math.log (10.)

print "Size of spec array = ", len (spec [line_toread])

print "Time (days) = ", times [line_toread] / 86400.

iter = 0

for wavelength in wavearr:
  print wavelength, ' ', specarray [iter]
  iter = iter + 1

plt.plot (wavearr, specarray)
plt.xlim (3000., 9000.)
plt.savefig ('spectrum', format = 'pdf')
