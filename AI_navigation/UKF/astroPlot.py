#  astroPlot
#
#  File containing different functions used for visualisation in astrosim
#
#  Syntax:  import astroPlot
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
#  Creation March 24, 2020
#  Last revision: March 24, 2020
#
#  Mods:
#
#  Sources:
#
# ------------- BEGIN CODE --------------


# Imports
import matplotlib.pyplot as plt
from astroTransf import Inertial2Hill


def MakeComparisonPlot(title, size=8, fontsize=12, xlabel="ElapsedDays", ylabel=["X (km)", "Y (km)", "Z (km)"]):
    #  MakeComparisonPlot(title, size=8, fontsize=12)
    #
    #  Function to create a figure to plot position or velocity differences between two objects
    #
    #  Syntax:  axes, fig = MakeComparisonPlot("Pick your title")
    #
    #  Inputs:
    #   - title: str with the title for the figure.
    #   - size: size for the figure.
    #   - fontsize: size for the font.
    #   - xlabel, ylabel: text for the labels
    #
    #  Outputs:
    #   - axes: handle to the three figure subplot's axes.
    #   - fig: handle to the figure.
    #
    #  Other files required: none
    #  Subfunctions: none
    #
    #  See also:
    #  Author: Pelayo Penarroya
    #  email: pelayo.penarroya@deimos-space.com
    #  Creation April 16, 2020
    #  Last revision: April 16, 2020
    #
    #  Mods:
    #   - May 12, 2020: Merged with velocity comparisons too
    #
    #  Sources:
    #
    # ------------- BEGIN CODE --------------

    # Make the figure
    fig = plt.figure(figsize=(size, size))

    # Make sub plot and add title
    axis1 = fig.add_subplot(311)
    plt.title(title, y=1.025, fontsize=fontsize)
    axis2 = fig.add_subplot(312)
    axis3 = fig.add_subplot(313)

    # Set axis labels
    axis1.set_ylabel(ylabel[0])
    axis2.set_ylabel(ylabel[1])
    axis3.set_ylabel(ylabel[2])

    axis3.set_xlabel(xlabel)

    axes = [axis1, axis2, axis3]

    plt.tight_layout()

    # Return the plt
    return axes, fig


def MakeResidualsPlot(title, size=8, fontsize=12, resSize=None, xlabel="ElapsedDays", ylabel=["X (km)", "Y (km)", "Z (km)"]):
    #  MakeResidualsPlot(title, size=8, fontsize=12)
    #
    #  Function to create a figure to plot residuals of a typical OD process
    #
    #  Syntax:  axes, fig = MakeResidualsPlot("Pick your title")
    #
    #  Inputs:
    #   - title: str with the title for the figure.
    #   - size: size for the figure.
    #   - fontsize: size for the font.
    #   - xlabel, ylabel: text for the labels
    #   - resSize: number of observation types in the resdiuals array
    #
    #  Outputs:
    #   - axes: handle to the three figure subplot's axes.
    #   - fig: handle to the figure.
    #
    #  Other files required: none
    #  Subfunctions: none
    #
    #  See also:
    #  Author: Pelayo Penarroya
    #  email: pelayo.penarroya@deimos-space.com
    #  Creation May 12, 2020
    #  Last revision: May 12, 2020
    #
    #  Mods:
    #
    #  Sources:
    #
    # ------------- BEGIN CODE --------------

    # Make the figure
    fig = plt.figure(figsize=(size, size))

    # check that the dimension of the residuals is given
    if resSize == None:
        raise InputError("Residual dimension must be given.")

    figDesign = resSize * 100 + 10

    axes = []

    # Make sub plot and add title
    for ii in range(resSize):
        axes.append(fig.add_subplot(figDesign + ii + 1))
        axes[-1].set_ylabel(ylabel[ii])
        if ii == 0:
            plt.title(title, y=1.025, fontsize=fontsize)

    axes[-1].set_xlabel(xlabel)

    plt.tight_layout()

    # Return the plt
    return axes, fig


def AddComparisonToPlot(axes, epochs, diff):
    #  AddPosComparisonToPlot(axes, epochs, diff)
    #
    #  Function to insert a position or velocity comparison in a figure with 3 subplots
    #
    #  Syntax:  AddComparisonToPlot(axes, epochs, diff)
    #
    #  Inputs:
    #   - axes: handle to the figure axis
    #   - epochs: 1xN array with the epochs
    #   - diff: 3xN array with the difference in position or velocity
    #
    #  Outputs:
    #   - axes: handle to the figure axes
    #
    #  Other files required: none
    #  Subfunctions: none
    #
    #  See also:
    #  Author: Pelayo Penarroya
    #  email: pelayo.penarroya@deimos-space.com
    #  Creation April 16, 2020
    #  Last revision: April 16, 2020
    #
    #  Mods:
    #   - April 21, 2020: input now is diff (no pos1 and pos2)
    #   - April 23, 2020: now velocities can also be plotted
    #
    #  Sources:
    #
    # ------------- BEGIN CODE --------------

    # check position has three components
    if diff.shape[0] != 3:
        raise SystemError("Array must have 3 components.")
    if len(epochs.shape) != 1:
        raise SystemError("Time array must have 1 dimension.")

    # check time and diff arrays are consistent
    if diff.shape[1] != epochs.shape[0]:
        raise SystemError(
            "Object has different sizes for differential and time arrays")

    # check if we are plotting a single diff
    if len(diff.shape) == 1:
        axes.scatter([diff[0]], [diff[1]],
                     [diff[2]], s=40)
    # or a series of diffs
    else:
        for ii in range(3):
            axes[ii].plot(epochs, diff[ii])

    return axes


def AddResidualsToPlot(axes, epochs, residuals, resSize):
    #  AddResidualsToPlot(axes, epochs, diff)
    #
    #  Function to insert residuals scatterings in a residual plot
    #
    #  Syntax:  AddResidualsToPlot(axes, epochs, diff)
    #
    #  Inputs:
    #   - axes: handle to the figure axis
    #   - epochs: 1xN array with the epochs
    #   - diff: 3xN array with the difference in position or velocity
    #   - resSize: number of observation types in the resdiuals array
    #
    #  Outputs:
    #   - axes: handle to the figure axes
    #
    #  Other files required: none
    #  Subfunctions: none
    #
    #  See also:
    #  Author: Pelayo Penarroya
    #  email: pelayo.penarroya@deimos-space.com
    #  Creation May 12, 2020
    #  Last revision: May 12, 2020
    #
    #  Sources:
    #
    # ------------- BEGIN CODE --------------

    # check position has three components
    if residuals.shape[0] != resSize:
        raise SystemError("Array must have %d components." % (resSize))
    if len(epochs.shape) != 1:
        raise SystemError("Time array must have 1 dimension.")

    # check time and residuals arrays are consistent
    if residuals.shape[1] != epochs.shape[0]:
        raise SystemError(
            "Object has different sizes for residuals and time arrays")

    for ii in range(resSize):
        axes[ii].scatter(epochs, residuals[ii])

    return axes
