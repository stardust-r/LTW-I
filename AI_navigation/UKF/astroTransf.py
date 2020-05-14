#  astroTransf
#
#  File containing different functions used for coordinates
#  and time systems transformations.
#
#  Syntax:  from astroTransf import []
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
#  Creation April 22, 2020
#  Last revision: April 22, 2020
#
#  Mods:
#
#  Sources:
#
# ------------- BEGIN CODE --------------

# imports
import numpy as np
from numpy.linalg import norm
import math


def UnitVector(vec):
    #  UnitVector(vec)
    #
    #  This function computes the unit vector of vec, checking for divisions over 0
    #  and raising an error in that case
    #
    #  Syntax:  unitVec = UnitVector(vec)
    #
    #  Inputs:
    #   - vec: array to be normalised
    #
    #  Outputs:
    #   - unitVec: normalised array
    #
    #  Other files required: none
    #  Subfunctions: none
    #
    #  See also:
    #  Author: Pelayo Penarroya
    #  email: pelayo.penarroya@deimos-space.com
    #  Creation March 10, 2020
    #  Last revision: March 10, 2020
    #
    #  Mods:
    #
    #  Sources:
    #
    # ------------- BEGIN CODE --------------

    import numpy as np
    import sys

    EPS = sys.float_info.epsilon

    vecNorm = np.linalg.norm(vec)

    if vecNorm < EPS:
        raise ZeroDivisionError("Norm of given vector is 0 (EPS)")
    else:
        return np.dot(vec, 1 / vecNorm)


def Kep2Cart(oe, mu, angleUnits="deg"):
    #  Kep2Cart(oe, mu, angleUnits="deg")
    #
    #  Function to transform from keplerian to cartesian elements.
    #
    #  Syntax:  cartState = Kep2Cart(oe, mu, angleUnits="deg")
    #
    #  Inputs:
    #   - oe: array with orbital elements
    #         (sma[m], ecc[-], inc[deg or rad], raan[deg or rad], arg perigee[deg or rad], true anomaly[deg or rad]).
    #   - mu: gravitational parameter for the body around which
    #         the orbital elements are defined.
    #   - angleUnits: variable to state whether angles are given in deg or rad.
    #
    #  Outputs:
    #   - posvel: vector containing position and velocity inertial components
    #             for the given orbital elements and central body [m m/s].
    #
    #  Other files required: # TODO: check this on each function
    #  Subfunctions: # TODO: check this on each function
    #
    #  See also:
    #  Author: Pelayo Penarroya
    #  email: pelayo.penarroya@deimos-space.com
    #  Creation March 27, 2020
    #  Last revision: March 27, 2020
    #
    #  Mods:
    #
    #  Sources:
    #   [1]: Fundamentals of astrodynamics, Wakker 2009
    #
    # ------------- BEGIN CODE --------------

    # TODO: add eccentric anomaly and mean anomaly

    # check for units
    if angleUnits == "deg":
        for index, elem in enumerate(oe[2:]):
            oe[index+2] = np.deg2rad(elem)
    elif angleUnits != "rad":
        raise SystemError("angleUnits must be \"deg\" or \"rad\".")
    # initialise variables
    sma, ecc, inc, raan, argP, truAn = oe

    # recursive operations
    cosTruAn = np.cos(truAn)
    sinTruAn = np.sin(truAn)
    cosRaan = np.cos(raan)
    sinRaan = np.sin(raan)
    cosArgP = np.cos(argP)
    sinArgP = np.sin(argP)
    cosInc = np.cos(inc)
    sinInc = np.sin(inc)

    # radius and angular momentum
    rMag = (sma * (1.0 - ecc**2)) / (1 + ecc * cosTruAn)
    hMag = np.sqrt(mu * sma * (1.0 - ecc**2))

    # required parameters [1]
    l1 = cosRaan * cosArgP - sinRaan * sinArgP * cosInc
    l2 = -cosRaan * sinArgP - sinRaan * cosArgP * cosInc
    m1 = sinRaan * cosArgP + cosRaan * sinArgP * cosInc
    m2 = -sinRaan * sinArgP + cosRaan * cosArgP * cosInc
    n1 = sinArgP * sinInc
    n2 = cosArgP * sinInc
    xi = rMag * cosTruAn
    eta = rMag * sinTruAn

    # position vector
    pos = np.array([l1 * xi + l2 * eta,
                    m1 * xi + m2 * eta,
                    n1 * xi + n2 * eta])

    # velocity vector
    vel = np.array([mu / hMag * (-l1 * sinTruAn + l2 * (ecc + cosTruAn)),
                    mu / hMag * (-m1 * sinTruAn + m2 * (ecc + cosTruAn)),
                    mu / hMag * (-n1 * sinTruAn + n2 * (ecc + cosTruAn))])

    # return posvel
    return np.append(pos, vel)


def GetInertial2HillMatrix(posvel, transpose=0):
    #  GetInertial2HillMatrix(posvel, transpose = 0)
    #
    #  Function to obtain the transformation matrix from inertial frame to orbit frame,
    #  with components along radial and normal direction. The y component is the vectorial
    #  product obtained from the former two. It also provides the inverse transformation if
    #  transpose is equal to 1.
    #
    #  Syntax:  inertial2hillMat = GetInertial2HillMatrix(posvel) # from eci 2 hil
    #           inertial2hillMat = GetInertial2HillMatrix(posvel, 1) # from hill 2 eci
    #
    #  Inputs:
    #   - posvel: vector containing position and velocity inertial components
    #             for the given orbital elements and central body [m m/s].
    #   - transpose: flag to indicate whether the inverse transroamtion is wanted (1),
    #                or not (0).
    #
    #  Outputs:
    #   - inertial2hillMat: dcm for the transformation from inertial to hill
    #
    #  Other files required: none
    #  Subfunctions: none
    #
    #  See also:
    #  Author: Pelayo Penarroya
    #  email: pelayo.penarroya@deimos-space.com
    #  Creation April 21, 2020
    #  Last revision: April 21, 2020
    #
    #  Mods:
    #
    #  Sources:
    #
    # ------------- BEGIN CODE --------------

    pos = posvel[0:3]
    vel = posvel[3:]

    # compute unit vectors (er, et, eh)
    er = UnitVector(pos)

    # compute angular momentum vector
    h = np.cross(pos, vel)
    eh = UnitVector(h)

    # compute the last direction
    et = UnitVector(np.cross(eh, er))

    inertial2hillMat = np.array([er, et, eh])

    if transpose == 1:
        return inertial2hillMat.T
    elif transpose == 0:
        return inertial2hillMat
    else:
        raise SystemError("\"transpose\" flag can only be 0 or 1.")


def Inertial2Hill(posvelRef, posvelRel):
    #  Inertial2Hill(posvelRef, posvelRel)
    #
    #  Function to transform an inertial state vector to a hill reference frame
    #  whose ephemeris are given in inertial frame.
    #
    #  Syntax:  posvelHill = Inertial2Hill(posvelRef, posvelRel)
    #
    #  Inputs:
    #   - posvelRef: 6xN vector containing position and velocity inertial components
    #                of the centre of the hill reference frame along time. [m m/s]
    #   - posvelRel: 6xN vector containing position and velocity inertial components
    #                of an object along time. [m m/s]
    #  Outputs:
    #   - posvelHill: 6xN vector containing position and velocity hill components
    #                 of the relative object along time. [m m/s]
    #
    #  Other files required: none
    #  Subfunctions: none
    #
    #  See also:
    #  Author: Pelayo Penarroya
    #  email: pelayo.penarroya@deimos-space.com
    #  Creation April 21, 2020
    #  Last revision: April 21, 2020
    #
    #  Mods:
    #   - April 27, 2020: Bug in computation of relative vel.
    #                     Order of matrix product was wrong.
    #
    #  Sources:
    #
    # ------------- BEGIN CODE --------------

    if len(posvelRef.shape) != len(posvelRel.shape):
        raise SystemError("Input arrays must have equal dimensions.")
    elif len(posvelRef.shape) == 1 and len(posvelRef.shape) == 1:
        if posvelRef.shape[0] != 6 and posvelRel.shape[0] != 6:
            raise SystemError("States must have 6 elements.")
        nEpochs = 1
        # we create a second row with same content just so we can
        # keep the code equal for multidimensional states.
        # The for-loop will never go in there because nEpochs = 1
        posvelRef = np.array(list([posvelRef, posvelRef])).T
        posvelRel = np.array(list([posvelRel, posvelRel])).T
    elif posvelRef.shape[1] != posvelRel.shape[1]:
        raise SystemError("Both ephemeris must have the same length")
    elif posvelRef.shape[0] != 6 and posvelRel.shape[0] != 6:
        raise SystemError("States must have 6 elements.")
    else:
        nEpochs = posvelRef.shape[1]

    posvelHill = np.empty([6, nEpochs])

    for ii in range(nEpochs):

        r = posvelRef.T[ii, :3]
        v = posvelRef.T[ii, 3:]

        # get rotational speed of the frame
        n = norm(np.cross(r, v)) / (norm(r)**2)

        # get transformation matrix
        transfMat = GetInertial2HillMatrix(posvelRef.T[ii], transpose=0)

        # get rotation matrix of the frame around the inertial frame
        omegaMat = np.array([[0, n, 0], [-n, 0, 0], [0, 0, 0]])

        # transform position into inertial frame
        posRel = np.dot(transfMat, (posvelRel.T[ii, :3] - r))
        velRel = np.dot(transfMat, (posvelRel.T[ii, 3:] - v)) + np.dot(
            np.dot(omegaMat, transfMat), (posvelRel.T[ii, :3] - r))
        posvelHill[:, ii] = np.append(posRel, velRel)

    # return posvelInertial
    return posvelHill
