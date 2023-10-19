import numpy as np
from scipy.sparse import lil_matrix, csc_matrix
from scipy.sparse.linalg import eigs
from scipy import sparse
import cmath

def raylee_lysmer(Nn, vsv, vpv, rhov, f, hv, modn, Nnf, vpfv, rhofv, hfv):
    # Number of nodes in the fluid, based on the number of elements
    if Nnf > 0:
        Nnfo = Nnf + 1
    else:
        Nnfo = 0

    # Make fluid portion of model
    kappafv = rhofv * vpfv * vpfv  # Modulus
    omga = 2 * np.pi * f  # Angular frequency

    # Initialize some local matrices
    L1 = np.zeros((2, 2))
    L3 = np.zeros((2, 2))
    M1 = np.zeros((2, 2))

    # Initialize the global matrix
    Ka1 = lil_matrix((Nnfo + 2 * Nn, Nnfo + 2 * Nn))
    Ka3 = lil_matrix((Nnfo + 2 * Nn, Nnfo + 2 * Nn))
    M = lil_matrix((Nnfo + 2 * Nn, Nnfo + 2 * Nn))

    # For all elements in the fluid
    for ii in range(0, Nnf):
        h = hfv[ii]  # Grid interval of current element
        rhof = rhofv[ii]
        kappaf = kappafv[ii]

        # Make elemental mass matrix
        M1[0, 0] = h / (2 * kappaf)
        M1[1, 1] = h / (2 * kappaf)

        # Make elemental stiffness matrices
        alph = 1 / (6 * rhof)
        bet = 1 / (6 * rhof)

        # The 4 entries of the 2x2 elemental stiffness matrices
        L1[0, 0] = 2 * alph * h
        L3[0, 0] = (6 * bet / h)
        L1[0, 1] = alph * h
        L3[0, 1] = -(6 * bet / h)
        L1[1, 0] = L1[0, 1]
        L3[1, 0] = L3[0, 1]
        L1[1, 1] = L1[0, 0]
        L3[1, 1] = L3[0, 0]

        # Assemble mass and stiffness matrices from elemental matrices
        M[(1 * (ii)):(1 * (ii + 2)), (1 * (ii)):(1 * (ii + 2))] += M1
        Ka1[(1 * (ii)):(1 * (ii + 2)), (1 * (ii)):(1 * (ii + 2))] += L1
        Ka3[(1 * (ii)):(1 * (ii + 2)), (1 * (ii)):(1 * (ii + 2))] += L3

    M[0, 0] *= 2
    Ka1[0, 0] *= 2
    Ka3[0, 0] *= 2

    # Make solid portion of model
    muv = rhov * vsv * vsv
    lamdav = rhov * vpv * vpv - 2 * muv

    Ka2 = lil_matrix((Nnfo + 2 * Nn, Nnfo + 2 * Nn))
    L1 = np.zeros((4, 4))
    L2 = np.zeros((4, 4))
    L3 = np.zeros((4, 4))
    M1 = np.zeros((4, 4))

    # For all elements in the solid
    for ii in range(0, Nn):
        h = hv[ii]  # Grid interval of current element
        mu = muv[ii]
        lamda = lamdav[ii]

        # Make elemental mass matrix
        M1[0, 0] = h * rhov[ii] / 2
        M1[1, 1] = h * rhov[ii] / 2
        M1[2, 2] = h * rhov[ii] / 2
        M1[3, 3] = h * rhov[ii] / 2

        # Make elemental stiffness matrices
        alph = ((2 * mu) + lamda) / 6
        bet = mu / 6
        theta = (mu + lamda) / 4
        psi = (mu - lamda) / 4

        # The 16 entries of the 4x4 elemental stiffness matrices
        L1[0, 0] = 2 * alph * h
        L3[0, 0] = (6 * bet / h)
        L2[0, 1] = 2 * psi
        L1[0, 2] = alph * h
        L3[0, 2] = -(6 * bet / h)
        L2[0, 3] = 2 * theta
        L2[1, 0] = L2[0, 1]
        L1[1, 1] = 2 * bet * h
        L3[1, 1] = (6 * alph / h)
        L2[1, 2] = -2 * theta
        L1[1, 3] = bet * h
        L3[1, 3] = -(6 * alph / h)
        L1[2, 0] = L1[0, 2]
        L3[2, 0] = L3[0, 2]
        L2[2, 1] = L2[1, 2]
        L1[2, 2] = L1[0, 0]
        L3[2, 2] = L3[0, 0]
        L2[2, 3] = -2 * psi
        L2[3, 0] = L2[0, 3]
        L1[3, 1] = L1[1, 3]
        L3[3, 1] = L3[1, 3]
        L2[3, 2] = L2[2, 3]
        L1[3, 3] = L1[1, 1]
        L3[3, 3] = L3[1, 1]

        # Assemble mass and stiffness matrices from elemental matrices
        if ii == Nn-1:
            slice1 = slice(Nnfo + 2 * ii, Nnfo + 2 * (ii + 1))
            M[slice1, slice1] += M1[0:2, 0:2]
            Ka1[slice1, slice1] += L1[0:2, 0:2]
            Ka2[slice1, slice1] += L2[0:2, 0:2]
            Ka3[slice1, slice1] += L3[0:2, 0:2]
        else:
            slice1 = slice(Nnfo + 2 * ii, Nnfo + 2 * (ii + 2))
            M[slice1, slice1] += M1
            Ka1[slice1, slice1] += L1
            Ka2[slice1, slice1] += L2
            Ka3[slice1, slice1] += L3
    # Construct the coupling matrix
    if Nnf > 0:
        Cm = lil_matrix((Nnfo + 2 * Nn, Nnfo + 2 * Nn))
        Cm[Nnfo, Nnfo + 2] = 1
        Cm[Nnfo + 2, Nnfo] = 1
    else:
        Cm = lil_matrix((Nnfo + 2 * Nn, Nnfo + 2 * Nn))

    # Find the Rayleigh/Scholte wave speed which would exist if the solid model
    # were a halfspace with the minimum model velocity
    if Nnf > 0:
        msloc = np.argmin(vsv)
        mfloc = np.argmin(vpfv)
        vsmay = vsv[msloc]
        vpmay = vpv[msloc]
        vpfmay = vpfv[mfloc]
        rhofmay = rhofv[mfloc]
        rhomay = rhov[msloc]
        rspd = stoneley_vel(vpmay, vsmay, vpfmay, rhofmay, rhomay)
    else:
        msloc = np.argmin(vsv)
        vsmay = vsv[msloc]
        vpmay = vpv[msloc]
        # Coefficients of Rayleigh's polynomial
        t1 = 1 / (vsmay ** 6)
        t2 = -8 / (vsmay ** 4)
        t3 = ((24 / (vsmay ** 2)) - (16 / (vpmay ** 2)))
        t4 = -16 * (1 - ((vsmay / vpmay) ** 2))
        # Rayleigh wave speed
        rspd = cmath.sqrt(min(np.roots([t1, t2, t3, t4])))

    # Find the eigenvalue closest to the upper-bound eigenvalue
    mn = modn
    opts = {'disp': 0}
    
    a = M + sparse.eye(Nnfo + 2 * Nn)
    b = omga**2 * M - Ka3 - omga * Cm
    c = sparse.eye(Nnfo + 2 * Nn)
    
    A1 = csc_matrix(np.block([[a, c], [b]]))
    
    # 计算特征值和特征向量
    A1 = csc_matrix([[M + sparse.eye(Nnfo + 2 * Nn), sparse.eye(Nnfo + 2 * Nn)],
                    [omga**2 * M - Ka3 - omga * Cm, Ka2]])

    A2 = csc_matrix([[sparse.eye(Nnfo + 2 * Nn), sparse.eye(Nnfo + 2 * Nn)],
                    [sparse.eye(Nnfo + 2 * Nn), Ka1]])
    xp, dp = eigs(A1, A2, k=mn, sigma=omga / rspd, which='LM', **opts)
    # xp, dp = eigs(csc_matrix([[lil_matrix((Nnfo + 2 * Nn, Nnfo + 2 * Nn)), sparse.eye(Nnfo + 2 * Nn, Nnfo + 2 * Nn)],
    #                          [omga ** 2 * M - Ka3 - omga * Cm, Ka2]]).all(),
    #              csc_matrix([[lil_matrix((Nnfo + 2 * Nn, Nnfo + 2 * Nn)), lil_matrix((Nnfo + 2 * Nn, Nnfo + 2 * Nn))],
    #                          [lil_matrix((Nnfo + 2 * Nn, Nnfo + 2 * Nn)), Ka1]]).all(),
    #              k=mn, sigma=omga / rspd, which='LM', **opts)
    
    x = xp[:, 0]
    d = dp[0, 0]

    # Normalize the eigenfunction
    fctr = 1 / ((np.transpose(x[0:Nnfo + 2 * Nn]) * M * x[0:Nnfo + 2 * Nn]) - (
            (np.transpose(x[0:Nnfo + 2 * Nn]) * Cm * x[0:Nnfo + 2 * Nn])) / (2 * omga))
    evp = x[0:Nnfo + 2 * Nn] * np.sqrt(fctr) * np.sign(x[Nnfo + 1])
    # Return only the eigenvector in the solid
    ev = evp[Nnfo + 1:Nnfo + 2 * Nn]

    # The wavenumber
    kk = d.real

    # The phase velocity
    vpk = omga / kk

    # The group velocity
    num = np.transpose(x[0:Nnfo + 2 * Nn]) * ((2 * d * Ka1) - Ka2) * x[0:Nnfo + 2 * Nn]
    denom = (2 * omga * (np.transpose(x[0:Nnfo + 2 * Nn]) * M * x[0:Nnfo + 2 * Nn])) - (
            np.transpose(x[0:Nnfo + 2 * Nn]) * Cm * x[0:Nnfo + 2 * Nn])
    vpg = num / denom

    return vpk, vpg, ev
