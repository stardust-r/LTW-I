#  script_TemplateUkf
#
#  Template script for navigation exercises using UKF
#
#  Syntax:  script_TemplateUkf.py
#
#  Inputs:
#
#  Outputs:
#
#  Other files required: none
#  Subfunctions: none
#
#  See also:
#  Author: Pelayo Penarroya
#  email: pelayo.penarroya@deimos-space.com
#  Creation May 06, 2020
#  Last revision: May 06, 2020
#
#  Mods:
#
# ------------- BEGIN CODE --------------

# Imports

import numpy as np
from numpy.linalg import norm
from datetime import datetime
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
import spiceypy as spice
from filterpy.kalman import (
    UnscentedKalmanFilter,
    MerweScaledSigmaPoints,
    JulierSigmaPoints,
)
from filterpy.common import Q_discrete_white_noise
from astroPlot import *
from astroTransf import *

# load spice kernels
PATH_METAKERNEL = "kernels/astrosim_metakernels.txt"
spice.furnsh(PATH_METAKERNEL)

# some constants
KM2M = 1e3
M2KM = 1e-3

# Definition of simulation environment


# time
tStart = datetime(2020, 4, 13, 17)  # utc
tStop = tStart + relativedelta(hours=24)

# reference frames
rf = "J2000"
originRf = "LUTETIA"

# massive bodies and models for each of them (numbers for coefficients, strings for shapemodels)
massBodies = [
    originRf,
]

# solar radiation pressure
srpFlag = 0

# state definition
sma = max(spice.bodvrd(originRf, "RADII", 3)[1]) * 15 * KM2M  # play with this
oe = [sma, 0.1, 45, 15, 135, 77]  # random orbit
mu = spice.bodvrd(originRf, "GM", 1)[1][0] * KM2M ** 3
cartState = Kep2Cart(oe, mu)
epoch = spice.str2et(str(tStart))

tStartEt = spice.str2et(str(tStart))
tStopEt = spice.str2et(str(tStop))
tSpan = [tStartEt, tStopEt]
tSpanEphemeris = [tStartEt - 12 * 3600, tStopEt + 12 * 3600]

# # dynamics for the problem
# dynSim = DyncamicSetup(massBodies, srpFlag)
# dynSim.populateEphemeris("ALL", tSpanEphemeris, rf, originRf)

# spacecraft True Trajectory
epochs, statesTrue = [], []
statesTrue.append(cartState)
epochs.append(epoch)

# add uncertainties for simulation
np.random.seed(11)
posStd = 1e4  # m   # play with this
velStd = 1e-1  # m / s
state_std = np.array([posStd, posStd, posStd, velStd, velStd, velStd])
stateEst = cartState + (np.random.rand(6) * state_std * 2) - state_std

# spacecraft Sim Trajectory
statesEst = []
statesEst.append(stateEst)

# UKF


def propagate(x, dt, mu):

    # propagate using spice
    newState = spice.prop2b(mu, x, dt)

    return newState


def computeAzel(x, obsNoise):

    # vector to body
    bodyPos_sc = -x[0:3]

    azimuth = np.arctan2(bodyPos_sc[1], bodyPos_sc[0])
    elevation = np.arctan2(bodyPos_sc[2], norm(bodyPos_sc[0:2]))

    return [azimuth, elevation] + (np.random.rand(2) * obsNoise * 2) - obsNoise


# design observations
dt = 300  # s   # play with this
# z_std = 1e2  # m - initial observervation uncertainty
z_std = 1e-3  # rads - initial observervation uncertainty  # play with this

# create sigma points to use in the filter.
points = MerweScaledSigmaPoints(6, alpha=0.1, beta=2.0, kappa=-1)
# points = JulierSigmaPoints(6)

# azel observations
kf = UnscentedKalmanFilter(
    dim_x=6, dim_z=2, dt=dt, fx=propagate, hx=computeAzel, points=points
)
# initial observation uncertainty
kf.R = np.diag([z_std ** 2, z_std ** 2])

kf.x = statesEst[0]  # estimated initial state
kf.P *= state_std ** 2  # initial state uncertainty
# add noise to the update step
kf.Q = Q_discrete_white_noise(dim=3, dt=dt, var=0.01 ** 2, block_size=2)

nObs = 10
time = np.arange(0, nObs * dt, dt)

# xTrue, xEst, azelTrue, azelEst = [], [], [], [], []
obsTrue, obsEst = [], []
counter = 0

for _ in time:

    counter += 1
    print(counter)

    # the true spacecraft moves forward
    newTrueState = spice.prop2b(mu, statesTrue[-1], dt)
    statesTrue.append(newTrueState)
    epochs.append(epochs[-1] + dt)

    # and takes a noisy observation
    obsTrue.append(computeAzel(statesTrue[-1], z_std))

    # predict is for fx
    kf.predict(mu=mu)

    # update is for hx
    kf.update(obsTrue[-1], obsNoise=z_std)

    # update state for simulated spacecraft
    statesEst.append(kf.x)

    # compute the true observation from the estimated position
    obsEst.append(computeAzel(statesEst[-1], 0))

# diff in states
hillDiff = Inertial2Hill(np.array(statesTrue).T, np.array(statesEst).T) * M2KM

# residuals
residuals = (np.array(obsTrue) - np.array(obsEst)).T

# Plot the results


axes1, fig1 = MakeComparisonPlot(
    "Truth vs Estimation",
    xlabel="Elapsed seconds",
    ylabel=["R (km)", "T (km)", "N (km)"],
)
AddComparisonToPlot(axes1, np.array(epochs) - epochs[0], hillDiff[0:3])

axes2, fig2 = MakeResidualsPlot(
    "Residuals",
    xlabel="Elapsed seconds",
    resSize=2,
    ylabel=["Az (rad)", "El (rad)"],
)
AddResidualsToPlot(
    axes2, np.array(epochs[1:]) - epochs[1], residuals, resSize=2
)

plt.show()

print("Done!")
