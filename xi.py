'''nbodykit code to compute xi(r, mu) and the multipoles of the correlation function.'''

import time
t0 = time.time()

from nbodykit.lab import *
from nbodykit.algorithms.pair_counters import *
import numpy as np
import sys
from nbodykit import setup_logging
import yaml

setup_logging() # log output to stdout


def load_config(section, name, default=None):
    try:
        return config[section][name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "Required configuration {}:{} not fount, and no default available".format(section, name)
            raise RuntimeError(error_msg)


# Reading configurations
config_path = sys.argv[1]
with open(config_path, "r") as f:
    config = yaml.load(f)

input_path = load_config("input", "input_path")
galaxy_catalog_fname = load_config("input", "galaxy_catalog")
random_catalog_fname = load_config("input", "random_catalog")

output_path = load_config("output", "output_path")
output_name_xi = load_config("output", "output_name_xi")
output_name_xi_l = load_config("output", "output_name_xi_l")

Nbins = load_config("xi_config", "Nbins")
Rmax = load_config("xi_config", "Rmax")
binning = load_config("xi_config", "binning")
Nmu = load_config("xi_config", "Nmu")
nthreads = load_config("xi_config", "nthreads", 100)

BoxSize = load_config("simulation_config", "BoxSize")

# Read file and create catalog
#names = ['x','y','z_rsd']
names = ['x','y','z_rsd', 'w']
cat_d = CSVCatalog(input_path + galaxy_catalog_fname, names)
cat_s = CSVCatalog(input_path + random_catalog_fname, names)
cat_d['RSDPosition'] = cat_d['x'][:,None] * [1, 0, 0] + cat_d['y'][:,None] * [0, 1, 0] + cat_d['z_rsd'][:,None] * [0, 0, 1]
cat_d.attrs['BoxSize'] = [BoxSize,BoxSize,BoxSize]
cat_s['RSDPosition'] = cat_s['x'][:,None] * [1, 0, 0] + cat_s['y'][:,None] * [0, 1, 0] + cat_s['z_rsd'][:,None] * [0, 0, 1]
cat_s.attrs['BoxSize'] = [BoxSize,BoxSize,BoxSize]

epsilon = 1e-4
edges = np.linspace(0,Rmax,Nbins+1)
edges[0] = epsilon # Won't accept 0 as the first bin (no self-pairs)

# Compute 2PCF
pc_d = SimulationBox2PCF(mode='2d', data1=cat_d, edges=edges, periodic=True,
                       show_progress=True, los='z', Nmu=Nmu, position='RSDPosition', nthreads=nthreads)
pc_s = SimulationBox2PCF(mode='2d', data1=cat_s, edges=edges, periodic=True,
                       show_progress=True, los='z', Nmu=Nmu, position='RSDPosition', nthreads=nthreads)
pc_ds = SimulationBox2PCF(mode='2d', data1=cat_d, data2=cat_s, edges=edges, periodic=True,
                       show_progress=True, los='z', Nmu=Nmu, position='RSDPosition', nthreads=nthreads)

mus = np.linspace(0.5 * (1./Nmu), 0.5 * ((Nmu - 1.)/Nmu + 1.),Nmu)

# Write xi(r,mu)
f = open(output_path + output_name_xi,'w')
f.write('# Correlation function xi(r, mu)\n')
f.write('# Displaced catalog: %s\n' % (galaxy_catalog_fname))
f.write('# Random catalog: %s\n' % (random_catalog_fname))
f.write('# Code to generate this measurement in ' + __file__ + '\n')
f.write('# Boxsize = %.1f\n'  % BoxSize)
f.write('# Binning = ' + binning + '\n')
f.write('# r mu xi\n')
for i in range(pc_d.corr['r'].shape[0]):
    for j in range(pc_s.corr['r'].shape[1]):
        #print(mus[j])
        f.write('%20.8e %20.8e %20.8e\n' % (pc_d.corr['r'][i][j], mus[j], pc_d.corr['corr'][i][j] + pc_s.corr['corr'][i][j] - 2*pc_ds.corr['corr'][i][j]))

f.close()

print(time.time()-t0)

# Compute multipoles
poles_d = pc_d.corr.to_poles([0,2,4])
poles_s = pc_s.corr.to_poles([0,2,4])
poles_ds = pc_ds.corr.to_poles([0,2,4])

# Write multipoles
f = open(output_path + output_name_xi_l,'w')
f.write('# Correlation function and multipoles\n')
f.write('# Displaced catalog: %s\n' % (galaxy_catalog_fname))
f.write('# Random catalog: %s\n' % (random_catalog_fname))
f.write('# Code to generate this measurement in ' + __file__ + '\n')
f.write('# Boxsize = %.1f\n'  % BoxSize)
f.write('# Binning = ' + binning + '\n')
f.write('# r xi_0 xi_2 xi_4\n')
for i in range(poles_d['r'].shape[0]):
    xi0 = poles_d['corr_0'][i] + poles_s['corr_0'] - 2*poles_ds['corr_0']
    xi2 = poles_d['corr_2'][i] + poles_s['corr_2'] - 2*poles_ds['corr_2']
    xi4 = poles_d['corr_4'][i] + poles_s['corr_4'] - 2*poles_ds['corr_4']
    f.write('%20.8e %20.8e %20.8e %20.8e\n' % (poles_d['r'][i], xi0[i], xi2[i], xi4[i]))

f.close()

print(time.time()-t0)

