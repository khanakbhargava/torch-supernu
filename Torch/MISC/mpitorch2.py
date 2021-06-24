import os
import sys
from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

N = int(sys.argv[1])

chunk = int(N / size)
#print(chunk)

if rank != (size-1):
	command = "./torch -i " + str((rank * chunk) + 1) + " -f " + str((rank + 1) * chunk)
	#print(rank)
	print(command)	
	os.system(command)
else:
	command = "./torch -i " + str((rank * chunk) + 1) + " -f " + str(N)	
	#print(rank)
	print(command)
	os.system(command)
