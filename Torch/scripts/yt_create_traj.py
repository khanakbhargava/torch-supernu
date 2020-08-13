import yt
import glob

# Need some comments here to describe what this script does. What is it inputting? What does it do? How does it work?

f_parts = glob.glob("/work/07441/kbhargav/stampede2/puredet2/pure_det_hdf5_part_*")
f_parts.sort()

# Is Y_e stored in both approx19 and parameteric burn? I'm sure it is in the latter.
fields = ["particle_dens", "particle_temp", "particle_ye", "particle_velocity_x", "particle_velocity_y"]

ds = yt.load(f_parts[0])
dd = ds.all_data()
indices = dd["particle_index"].astype("int64")

ts = yt.DatasetSeries(f_parts)
trajs = ts.particle_trajectories(indices, fields=fields) 
trajs.write_out("traj")


