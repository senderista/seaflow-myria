
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import csv


# In[2]:

# import the data
# 3-D matrix with T, S and the biological variable, e.g. mean bead fluorescence
fileURL = 'https://rest.myria.cs.washington.edu:1776/dataset/user-armbrustlab/program-seaflow/relation-beads_TS/data?format=csv'
result = pd.read_csv(fileURL,skiprows=1).values


# In[3]:

# the data
x = result[:,2] # salinity 
y = result[:,1] # temperature
z = result[:,0] # bead fsc_mean


fig, axScatter = plt.subplots(figsize=(10,10))

# the scatter plot:
im = axScatter.scatter(x, y, c=z, cmap = cm.jet )
axScatter.set_aspect(1.)
plt.xlabel('Salinity')
plt.ylabel('Temperature')

# create new axes on the right and on the top of the current axes
# The first argument of the new_vertical(new_horizontal) method is
# the height (width) of the axes to be created in inches.
divider = make_axes_locatable(axScatter)
axHistx = divider.append_axes("top", 1.2, pad=0.1, sharex=axScatter)
axHisty = divider.append_axes("right", 1.2, pad=0.1, sharey=axScatter)

# make some labels invisible
plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(),
         visible=False)

# now determine nice limits by hand:
binwidth = 0.25
# xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
xymax = np.max([40,40])
lim = ( int(xymax/binwidth) + 1) * binwidth

bins = np.arange(0, lim + binwidth, binwidth)
axHistx.hist(x, bins=bins)
axHisty.hist(y, bins=bins, orientation='horizontal')

axHistx.set_xbound(upper = 40)
axHisty.set_ybound(upper = 40)

# the xaxis of axHistx and yaxis of axHisty are shared with axScatter,
# thus there is no need to manually adjust the xlim and ylim of these
# axis.

#axHistx.axis["bottom"].major_ticklabels.set_visible(False)
for tl in axHistx.get_xticklabels():
    tl.set_visible(False)
axHistx.set_yticks([0, 50, 100])

#axHisty.axis["left"].major_ticklabels.set_visible(False)
for tl in axHisty.get_yticklabels():
    tl.set_visible(False)
axHisty.set_xticks([0, 50, 100])

plt.draw()

cbar_ax = fig.add_axes([1, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)

plt.show()


# In[6]:



