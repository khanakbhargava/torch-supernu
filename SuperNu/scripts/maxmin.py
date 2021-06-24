def maxmin(filename):

    vr = []
    vz = []

    f = open(filename,'r')

    open('final_vel.dat','r')
    lines = f.readlines()
    for line in lines:
        lst = line.split()
        vr.append(float(lst[0]))
        vz.append(float(lst[1]))
    f.close()
    vr_max = max(vr)
    vz_max = max(vz)
    vz_min = min(vz)
    return vr_max, vz_max, vz_min
