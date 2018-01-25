from __future__ import division

import dill
import os
from pkg_resources import resource_filename
import sys

import numpy as np

import nanoparticle_optimization as np_opt


'''
----------
Statepoint
----------
'''
sigma_bead = 0.5
radius = 4.0

'''
--------------------
Optimization Details
--------------------
'''
gridpoints = 25
configurations = 10
r_dependent_sampling = True

'''
----------------
Load Target Data
----------------
'''
resource_package = np_opt.__name__
target_path = os.path.join('utils', 'target_data', 'np_np', 'truncated',
    'U_{}nm_truncated.txt'.format(int(radius)))
target = np_opt.load_target(resource_filename(resource_package, target_path))
target.separations /= 10 # Convert distances from angstroms to nanometers

'''
------------------------------
Create Two-Nanoparticle System
------------------------------
'''
nano = np_opt.CG_nano(radius, sigma=sigma_bead)
system = np_opt.System(nano)

'''
----------------------------------------
Define Force field Parameters and Bounds
----------------------------------------
'''
sigma = np_opt.Parameter(value=sigma_bead, fixed=True)
m = np_opt.Parameter(value=4.5, upper=5.0, lower=4.0)
epsilon = np_opt.Parameter(value=1.0, upper=2.0, lower=0.25)
n = np_opt.Parameter(value=35.0, fixed=True)
forcefield = np_opt.Mie(sigma=sigma, epsilon=epsilon, n=n, m=m)

'''
-----------------------------------
Define and Execute the Optimization
-----------------------------------
'''
optimization = np_opt.Optimization(forcefield=forcefield, systems=system,
                                   targets=target, configurations=configurations)
optimization.optimize(gridpoints=gridpoints, verbose=True, polishing_function=None,
                      r_dependent_sampling=r_dependent_sampling)

'''
--------------------------
Serialize the Optimization
--------------------------
'''
dill.dump(optimization, open('opt-sigma{}.p'.format(sigma_bead), 'wb'))
