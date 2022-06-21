#THIS PROGRAM MUST BE RUN THIRD!! AFTER "standardize.py"

from itertools import chain

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime


#from standardize import standardize


import pandas as pd
trueElevationData = pd.read_csv('standardizedElevation.csv')
estimatedElevationData = pd.read_csv('estimatedHeights.csv')

# Extract the data we're interested in
lat = trueElevationData['Lat1'].values
lon = trueElevationData['Long1'].values

elevation = trueElevationData['Elevation'].values
lat = lat[:-1]
lon = lon[:-1]
elevation = elevation[:-1]

estimatedElevation = estimatedElevationData["elevations"].values
estimatedLat = estimatedElevationData['Lat1'].values
estimatedLon = trueElevationData['Long1'].values



def draw_map(m, scale=0.2):
    # draw a shaded-relief image
    m.shadedrelief(scale=scale)
    m.drawcountries(linewidth=0.5, color='k')
    m.bluemarble()

    
    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 0))
    lons = m.drawmeridians(np.linspace(-180, 180, 0))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)
    
    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')


fig = plt.figure(figsize=(10, 5), edgecolor='w') #8, 6
m = Basemap(projection='cyl', resolution='l',
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, )
draw_map(m)

print(len(lat))
print(estimatedElevation)

print(max(np.log10(elevation)))
print(min(np.log10(elevation)))
m.scatter(lon, lat, latlon=True,
	#c=(elevation), s=(estimatedElevation)/20,
	#c=((np.log10(elevation))* 1658.93649), s=(estimatedElevation)/20,
	c=((np.log10(elevation))), s=(estimatedElevation)/20,

    cmap='Reds', alpha=0.5)
#plt.clim(0, 6300)

# 3. create colorbar and legend
plt.colorbar(label=f"Log_10(True Elevation)")

for a in [1600, 3200, 6400]:

    plt.scatter([], [], c='Red', alpha=0.5, s=a/20,
                label=str(a) + ' m')
plt.legend(scatterpoints=1, frameon=True,
           labelspacing=1, loc='upper left', title = "Predicted Elevation", prop={'size': 12});
plt.grid(True)
plt.title("Elevation Data Overlayed on World Map ")
plt.savefig("Elevation_Data_Overlayed_on_World_Map.png")
plt.show()
