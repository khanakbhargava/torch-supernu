### This script uses yt to create particle trajectories from FLASH particle files

import yt
import glob

#Give path to particle files
f_parts = glob.glob("/work/07441/kbhargav/stampede2/puredet2/pure_det_hdf5_part_*")
f_parts.sort()

#Give fields to be included in the trajectories. Positions are added by default.
fields = ["particle_dens", "particle_temp", "particle_velocity_x", "particle_velocity_y"]

#Get indices of all available  particles
ds = yt.load(f_parts[0])
dd = ds.all_data()
indices = dd["particle_index"].astype("int64")

#Create individual '.dat' files for every particle
ts = yt.DatasetSeries(f_parts)
trajs = ts.particle_trajectories(indices, fields=fields) 
trajs.write_out("traj")


