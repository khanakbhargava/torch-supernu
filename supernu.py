import numpy as np
import os.path

def lim2slc(x, xlim):
  '''create an array slice from an array plus a min,max tuple'''
  if xlim is None: return slice(None)#{{{
  elif len(xlim) != 2: raise Exception('wrong xlim shape')
  elif xlim[0] > x[-1]  or  xlim[1] < x[0]: return slice(None)
  return slice( *tuple(np.searchsorted(x, xlim) + [0,1]))
#}}}


class Output:
  '''SuperNu output file class'''
  def __init__(self, fname):#{{{
    #-- filename
    self.fname = fname
    assert os.path.isdir(self.fname) #-- assert input is directory name
    if self.fname[-1] != '/': self.fname += '/' #-- append a slash if not provided
    #-- simulation name
    self.read_name()
    #-- grid size and dimensions
    self.read_tsptime()  #-- time steps
    self.read_flxgrid()  #-- flux bin sizes
    #-- volume data
    try: self.read_volgrid() #-- volume grid
    except IOError: print 'no grid file'

    #-- read flux automatically
    print 'reading:', self.fname
    self.readflux()


  def readflux(self):
    self.read_luminos()
    self.read_lumnum()
    try: self.read_lumdev()
    except IOError: print 'no flx_lumdev file'
    try: self.read_gamlum()
    except IOError: print 'no flx_gamluminos file'


  def readgrid(self):
    try: self.read_temp()
    except IOError: print 'no temp read'
    except ValueError: print 'temp format invalid'
    try: self.read_eraddens()
    except IOError: print 'no eraddens read'
    except ValueError: print 'eraddens format invalid'


  def toflux(self):
    '''conversion matrix to translate luminosity into flux units [erg/s/ster]'''
    toflux = np.ones([self.nphi, self.nmu, 1, self.nwl])
    toflux *= self.dwl
    toflux *= self.dmu.reshape(-1, 1, 1)
    toflux *= self.dphi.reshape(-1, 1, 1, 1)
    toflux = 1/toflux
    return toflux


#-- grid sizes
#-----------------------------------------------------------------------
  def read_name(self):
    '''SuperNu output.name file.  This is the simulation name.'''
    fname = self.fname + 'output.name'#{{{
    try:
      with open(fname,'r') as f: self.name = f.readline().strip()
    except IOError:
      print 'no such file:', fname
      self.name = ''
#}}}

  def read_tsptime(self):
    '''SuperNu output.tsp_time file'''
    fname = self.fname + 'output.tsp_time'#{{{
    with open(fname,'r') as f:
      self.ntime = int(f.readline().replace('#',''))
      self.time = self.tleft = np.atleast_1d(np.loadtxt(f))
    #-- new format includes end of last timestep
    if len(self.time) != self.ntime: self.time = self.tleft[:-1]
    self.ntime = len(self.time)
#}}}

  def read_flxgrid(self):
    '''SuperNu output.wlgrid file'''
    fname = self.fname + 'output.flx_grid'#{{{
    with open(fname,'r') as f:
      dims = f.readline().replace('#','') #-- strip leading #
      dims = [int(s) for s in dims.split()]
      lines = [f.readline() for i in range(len(dims))]
    #-- fix for old output files
    if len(dims) == 1: dims[0] -= 1
    #-- dim 1
    self.wlleft = np.fromstring(lines[0], sep=' ')
    #-- dim 2
    if len(dims) > 1: self.muleft = np.fromstring(lines[1], sep=' ')
    #-- dim 3
    if len(dims) > 2: self.phileft = np.fromstring(lines[2], sep=' ')

    self.wl = .5*(self.wlleft[:-1] + self.wlleft[1:])
    self.dwl = self.wlleft[1:] - self.wlleft[:-1]
    self.nwl = len(self.wl)

    self.mu = .5*(self.muleft[:-1] + self.muleft[1:])
    self.dmu = self.muleft[1:] - self.muleft[:-1]
    self.nmu = len(self.mu)

    self.phi = .5*(self.phileft[:-1] + self.phileft[1:])
    self.dphi = self.phileft[1:] - self.phileft[:-1]
    self.nphi = len(self.phi)
#}}}

  def read_volgrid(self):
    '''SuperNu output.grid file'''
    fname = self.fname + 'output.grd_grid'#{{{
    with open(fname,'r') as f:
      dims = f.readline().replace('#','') #-- strip leading #
      if len(dims.split()) == 1:
        self.igeom = int(dims)
        dims = f.readline().replace('#','') #-- strip leading #
      #-- grid dimensions
      dims = [int(s) for s in dims.split()]
      #-- file layout
      layout = f.readline().replace('#','') #-- strip leading #
      layout = [int(s) for s in layout.split()]
      #-- grid cell boundaries
      dimlines = [f.readline() for i in range(3)]
      #-- grid cell pointers
      #layoutlines = [f.readline() for i in range(layout[1])]

    #-- fix for old output files
    if len(dims) == 1: dims[0] -= 1

    self.xleft = np.fromstring(dimlines[0], sep=' ')
    self.yleft = np.fromstring(dimlines[1], sep=' ')
    self.zleft = np.fromstring(dimlines[2], sep=' ')

    self.x = .5*(self.xleft[:-1] + self.xleft[1:])
    self.dx = self.xleft[1:] - self.xleft[:-1]
    self.nx = len(self.x)
    assert self.nx == dims[0]

    self.y = .5*(self.yleft[:-1] + self.yleft[1:])
    self.dy = self.yleft[1:] - self.yleft[:-1]
    self.ny = len(self.y)
    assert self.ny == dims[1]

    self.z = .5*(self.zleft[:-1] + self.zleft[1:])
    self.dz = self.zleft[1:] - self.zleft[:-1]
    self.nz = len(self.z)
    assert self.nz == dims[2]
#}}}


#-- flux data
#-----------------------------------------------------------------------
  def read_luminos(self):
    '''SuperNu output.flx_luminos file'''
    fname = self.fname + 'output.flx_luminos'#{{{
    self.lum = np.loadtxt(fname)
    nrow, nwl = self.lum.shape
    if nrow != self.ntime*self.nmu*self.nphi: print self.fname, nrow, self.ntime*self.nmu*self.nphi
    assert nrow == self.ntime*self.nmu*self.nphi
    assert nwl == self.nwl
    self.lum = self.lum.reshape(self.ntime, self.nphi, self.nmu, self.nwl)
    self.lum = np.rollaxis(self.lum, 0, 3) #(self.nphi, self.nmu, self.ntime, self.nwl)

    #-- convert lum from erg/s to erg/s/cm/ster
    self.flux = self.toflux() * self.lum
#}}}

  def read_lumnum(self):
    '''SuperNu output.flx_lumnum file'''
    fname = self.fname + 'output.flx_lumnum'#{{{
    self.lumnum = np.loadtxt(fname)
    nrow, nwl = self.lumnum.shape
    assert nrow == self.ntime*self.nmu*self.nphi
    assert nwl == self.nwl
    self.lumnum = self.lumnum.reshape(self.ntime, self.nphi, self.nmu, self.nwl)
    self.lumnum = np.rollaxis(self.lumnum, 0, 3) #(self.nphi, self.nmu, self.ntime, self.nwl)
#}}}

  def read_lumdev(self):
    '''SuperNu output.flx_lumdev file'''
    fname = self.fname + 'output.flx_lumdev'#{{{
    self.lumdev = np.loadtxt(fname)
    nrow, nwl = self.lumdev.shape
    assert nrow == self.ntime*self.nmu*self.nphi
    assert nwl == self.nwl
    self.lumdev = self.lumdev.reshape(self.ntime, self.nphi, self.nmu, self.nwl)
    self.lumdev = np.rollaxis(self.lumdev, 0, 3) #(self.nphi, self.nmu, self.ntime, self.nwl)

    #-- sample standard deviation
    with np.errstate(invalid='ignore'):
      ##-- s2 per particle
      #self.lumdev = self.lumdev/self.lumnum - (self.lum/self.lumnum)**2
      ##-- total s2
      #self.lumdev *= self.lumnum
      ##-- total s
      #self.lumdev **= .5
      #-- total s
      self.lumdev = (self.lumdev - self.lum**2/self.lumnum)**.5
    self.lumdev[np.isnan(self.lumnum)] = 0
#}}}

  def read_gamlum(self):
    '''SuperNu output.flx_gamluminos file'''
    fname = self.fname + 'output.flx_gamluminos'#{{{
    self.gamlum = np.loadtxt(fname)
    nrow, = self.gamlum.shape
    assert nrow == self.ntime * self.nmu * self.nphi
    self.gamlum = self.gamlum.reshape(self.ntime, self.nphi, self.nmu)
    self.gamlum = np.rollaxis(self.gamlum, 0, 3) #(self.nphi, self.nmu, self.ntime)
#}}}


  def rebin_viewingangle(self, mode):
    '''rebin over viewing angle'''
    #-- mu#{{{
    if mode in ['mu', 'pi4']:
      self.nmu = 1
      self.muleft = self.muleft[[0,-1]]
      self.mu = .5*np.array([self.muleft[-1] + self.muleft[0]])
      self.dmu = np.array([self.muleft[-1] - self.muleft[0]])
      try:
        for arr in [self.lum, self.lumnum, self.gamlum]:
          arr[...] = arr.sum(axis=1, keepdims=True)
      except AttributeError: pass

    #-- phi
    if mode in ['phi', 'pi4']:
      self.nphi = 1
      self.phileft = self.phileft[[0,-1]]
      self.phi = .5*np.array([self.phileft[-1] + self.phileft[0]])
      self.dphi = np.array([self.phileft[-1] - self.phileft[0]])
      try:
        for arr in [self.lum, self.lumnum, self.gamlum]:
          arr[...] = arr.sum(axis=0, keepdims=True)
      except AttributeError: pass

    #-- convert flux from lum
    if mode in ['mu', 'phi', 'pi4']:
      try:
        self.flux = self.toflux() * self.lum
      except AttributeError: pass
#}}}


#-- volume data
#-----------------------------------------------------------------------
  def read_temp(self):
    '''SuperNu output.temp file'''
    fname = self.fname + 'output.grd_temp'#{{{
    self.temp = np.loadtxt(fname)
    nrow, nx = self.temp.shape
    print nrow, self.ntime, self.nx, self.ny, self.nz
    assert nrow == self.ntime*self.ny*self.nz
    assert nx == self.nx
    self.temp = self.temp.reshape(self.ntime, self.nz, self.ny, self.nx)
#}}}

  def read_eraddens(self):
    '''SuperNu output.temp file'''
    fname = self.fname + 'output.grd_eraddens'#{{{
    self.eraddens = np.loadtxt(fname)
    nrow, nx = self.eraddens.shape
    assert nrow == self.ntime*self.ny*self.nz
    assert nx == self.nx
    self.eraddens = self.eraddens.reshape(self.ntime, self.nz, self.ny, self.nx)
#}}}

  def read_opac(self):
    '''SuperNu output.opac file'''
    fname = self.fname + 'output.grd_opac'#{{{
    with open(fname,'r') as f:
      header = f.readline()[1:] #remove leading #
      opac = np.loadtxt(f)
    #-- dimensions
    nwl, nx, ntime = tuple([int(s) for s in header.split()])
    nrow, ncol = opac.shape
    assert ncol == nwl+2
    assert nwl == self.nwl
    assert nx == self.nx
    assert ntime*nx == nrow
    ntime = nrow/nx
    #-- reshape
    opac = opac.reshape(ntime, nx, nwl+2)
    self.opac_temp = opac[:, :, 0].reshape(ntime, nx)
    self.opac_sig = opac[:, :, 1].reshape(ntime, nx)
    self.opac_cap = opac[:, :, 2:]
#}}}


  def read_timing(self):
    '''SuperNu output.timing file'''
    fname = self.fname + 'output.timing'#{{{
    with open(fname,'r') as f:
      header = f.readline()[1:].split() #remove leading #
      timing = np.loadtxt(f).transpose()
    #-- dict
    self.timing = {}
    for i,key in enumerate(header):
      self.timing[key] = timing[i]
#}}}

  def read_counters(self):
    '''SuperNu output.counters file'''
    fname = self.fname + 'output.counters'#{{{
    with open(fname,'r') as f:
      header = f.readline()[1:].split() #remove leading #
      counters = np.loadtxt(f).transpose()
    #-- dict
    self.counters = {}
    for i,key in enumerate(header):
      self.counters[key] = counters[i]
#}}}
#}}}


# vim: sw=2:fdm=marker
