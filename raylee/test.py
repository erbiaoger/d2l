# %%
import numpy as np

from functools import partial

from model_gen import model_gen
from Raylee_Forward import Raylee_Forward
from raylee_lysmer import raylee_lysmer

# Define the parameters
vs = np.array([80, 120, 180, 360, 450])           # S-velocity
vp = np.round(np.array(vs) * 4)                   # P-velocity
rho = 1000*np.array([1.8, 1.8, 1.8, 1.8, 1.8])    # Density
z = np.array([0.2, 0.2, 0.2, 0.2, 1])             # Grid spacing
nn = np.array([5, 10, 40, 80, 500])               # Number of grid elements

# Frequency range and DC sampling
fmin = 3
fmax = 50
# Frequency samples
Nf = 50
freq = np.linspace(fmin, fmax, Nf)

model = model_gen(vs, vp, rho, z, nn)
model['fks'] = freq
# Set additional parameters
Nnf = 0
vpfv = 0
rhofv = 0
hfv = 0
modn = 1
vsv = model['vsv']
vpv = model['vpv']
rhov = model['rhov']
h = model['h']
f = model['fks'][0]
Nn = model['Nn']


Vs = model['vsv']
fr = model['fks']


Forw = partial(Raylee_Forward, vpv=model['vpv'], rhov=model['rhov'], h=model['h'], fks=model['fks'], Nn=model['Nn'])

# %%

# % DATA 
cvorg = Forw(Vs).T
# %%
