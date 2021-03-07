from SkyNet import *
import numpy as np
import sys
import multiprocessing

import pdb

TIME_INDX = 0
TEMP_INDX = 1
DENS_INDX = 2

def run_skynet(args):
  do_inv, do_screen, do_heat , traj_filename= args

  if (do_inv):
    pref = "S_DB_"
  else:
    pref = "S_noDB_"

  if (do_screen):
    pref = pref + "scr_"
  else:
    pref = pref + "noScr_"

  if (do_heat):
    pref = pref + "heat"
  else:
    pref = pref + "noHeat"

  with open("sunet") as f:
    nuclides = [l.strip() for l in f.readlines()]

  nuclib = NuclideLibrary.CreateFromWinv("winvne_v2.0.dat", nuclides)

  opts = NetworkOptions()
  opts.ConvergenceCriterion = NetworkConvergenceCriterion.Mass
  opts.MassDeviationThreshold = 1.0E-10
  opts.IsSelfHeating = do_heat
  opts.EnableScreening = do_screen
  opts.DisableStdoutOutput = True
  #opts.MinDt = 1.0e-22
  #opts.NSEEvolutionMinT9 = 20.0

  helm = HelmholtzEOS(SkyNetRoot + "/data/helm_table.dat")

  strongReactionLibrary = REACLIBReactionLibrary("reaclib",
    ReactionType.Strong, do_inv, LeptonMode.TreatAllAsDecayExceptLabelEC,
    "Strong reactions", nuclib, opts, True, True)
  weakReactionLibrary = REACLIBReactionLibrary("reaclib",
    ReactionType.Weak, False, LeptonMode.TreatAllAsDecayExceptLabelEC,
    "Weak reactions", nuclib, opts, True, True)

  reactionLibraries = [strongReactionLibrary, weakReactionLibrary]

  screen = SkyNetScreening(nuclib)
  net = ReactionNetwork(nuclib, reactionLibraries, helm, screen, opts)
  nuclib = net.GetNuclideLibrary()

  fout = open("sunet", "w")
  for n in nuclib.Names():
    fout.write("%5s\n" % n)
  fout.close()

  # Set the initial composition. C/0 = 50/50
  Y0 = np.zeros(nuclib.NumNuclides())
  Y0[nuclib.NuclideIdsVsNames()["c12"]] = 0.5 / 12.0
  Y0[nuclib.NuclideIdsVsNames()["o16"]] = 0.5 / 16.0

  # load the trajectory file:
  dat = np.loadtxt(traj_filename)
  time_arr = dat[:,TIME_INDX]
  temp_arr = dat[:,TEMP_INDX]/1e9 # Temp should be in T9
  dens_arr = dat[:,DENS_INDX]
  #pdb.set_trace()
  #temperature_vs_time = PiecewiseLinearFunction(dat[:,0], dat[:,1], True)
  temperature_vs_time = PiecewiseLinearFunction(time_arr, temp_arr, True)
  density_vs_time = PiecewiseLinearFunction(time_arr, dens_arr, True)

  t0 = 0.0
  tfinal = time_arr[-1]
  print(tfinal)

  # Burn at constant density and temperature.
  #t0 = 0.0
  #tfinal = 1.0e2
  #T = 3
  #rho = 1.0e7
  #temperature_vs_time = ConstantFunction(T) # If you want o burn at a constant Temp.
  #density_vs_time = ConstantFunction(rho) # If you want to burn at a constant Density.
  #T = 6

  if (do_heat):
   # output = net.EvolveSelfHeatingWithInitialTemperature(Y0, t0, tfinal,
   #     T, density_vs_time, pref, 1.0E-12)
    output = net.EvolveSelfHeatingWithInitialTemperature(Y0, t0, tfinal,
        temperature_vs_time, density_vs_time, pref, 1.0E-12)
 
  else:
    output = net.Evolve(Y0, t0, tfinal, temperature_vs_time,
        density_vs_time, pref, 1.0E-15 )
    #pdb.set_trace()


if __name__ == '__main__':
  """
  num_cores = multiprocessing.cpu_count()
  print("Running with %i worker threads" % num_cores)
  pool = multiprocessing.Pool(num_cores)
  args = []
  for inv in [True, False]:
    for scr in [True, False]:
#      for heat in [True, False]:
      for heat in [True]:
        args.append((inv, scr, heat))
  print(args)
  pool.map_async(run_skynet, args)
  # done submitting jobs
  pool.close()
  pool.join()
  """
  #inv = True
  inv = True
  #scr = True
  scr = False
  heat = False
  #heat = True
  traj_filename = "tempdens1.dat"
  args = [inv, scr, heat, traj_filename]
  run_skynet(args)

