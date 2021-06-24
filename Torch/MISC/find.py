import re
import glob
import os

files = glob.glob("/scratch/07441/kbhargav/DEF2_STD_torch/*final.dat")
files.sort()

print(len(files))
#print(files[0])

proc_files=[]
proc_tag = []

for i in range(len(files)):
	head_tail=os.path.split(files[i])
	proc_files.append(head_tail[1])
	string = proc_files[i]
	s = re.findall(r"\d+",string)
	#s.group(0)
	#print(s)
	proc_tag.append(s[0])

print(len(proc_tag))
#print(proc_tag)

left_tag = []
f = open('left_tags.dat','a')
for i in range(1,9992):
	if str(i) in proc_tag:
		continue
	else:
		left_tag.append(i)
		f.write(str(i))
		f.write("\n")
f.close()
print(len(left_tag))
