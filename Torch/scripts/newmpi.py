import numpy as np
import os
import sys
from mpi4py import MPI

comm = MPI.COMM_WORLD

# Rank of the processor
my_rank = comm.Get_rank()

# No. of processors to use
nprocs = comm.Get_size()

#No. of particles to process
left_tag=[]

f = open('left_tags.dat','r')
lines = f.readlines()
for line in lines:
	lst = line.split()
	left_tag.append(lst[0])
	
nfiles = len(left_tag)
#print(nfiles)

remainder = nfiles % nprocs
quotient = (nfiles - remainder) / nprocs

files_array = quotient * np.ones(nprocs)

for j in range(remainder):
	files_array[j] = files_array[j] + 1

for i in range(int(files_array[my_rank])):
	command = "./torch -i " + str(left_tag[my_rank]) + " -f " + str(left_tag[my_rank])
	os.system(command)
	my_rank = my_rank + nprocs
