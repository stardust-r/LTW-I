#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:16:56 2019

@author: kqb12101
"""

from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats

# shape, location, and scale of the skenormal distribution
a, loc, scale = 5, 10, 3

# number of samples
ns=100


# draw a sample
data = stats.skewnorm(a, loc, scale).rvs(ns)
# estimate parameters from sample
ae, loce, scalee = stats.skewnorm.fit(data)
# Plot the PDF.
plt.figure()
plt.hist(data, bins=100, density=True, alpha=0.6, color='g')
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = stats.skewnorm.pdf(x,ae, loce, scalee)#.rvs(100)
plt.plot(x, p, 'k', linewidth=2)
print("True parameters:")
print([a, loc, scale])
print(" ")
print("Estimated parameters:")
print([ae, loce, scalee])

samples = data[:ns]
print(" ")
print("Mean (lower bound, upper bound):")
print(bs.bootstrap(samples, stat_func=bs_stats.mean))
print(" ")
print("Standard deviation (lower bound, upper bound):")
print(bs.bootstrap(samples, stat_func=bs_stats.std))
print(" ")
print("Skewness (lower bound, upper bound):")
print(bs.bootstrap(samples, stat_func=bs_stats.skew))
print(" ")
print("Kurtosis (lower bound, upper bound):")
print(bs.bootstrap(samples, stat_func=bs_stats.kurt))