import numpy as np
from raylee_lysmer import raylee_lysmer

def Raylee_Forward(vsv, vpv, rhov, h, fks, Nn):
    modn = 1
    # num_frequencies = len(fks)
    
    # vvp = np.zeros(num_frequencies)
    # U = np.zeros(num_frequencies)
    # evv = np.zeros((num_frequencies, 2 * Nn))

    vvp = []
    U = []
    evv = []

    countr = 0
    for f in fks:
        kk, vpk, vgk, ev = raylee_lysmer(Nn, vsv, vpv, rhov, f, h, modn, 0, 0, 0, 0)

        countr += 1
        # vvp[countr - 1] = vpk
        # U[countr - 1] = vgk
        # evv[countr - 1, :] = ev
        vvp.append(vpk)
        U.append(vgk)
        evv.append(ev)

    return np.array(vvp), np.array(U), np.array(evv)
