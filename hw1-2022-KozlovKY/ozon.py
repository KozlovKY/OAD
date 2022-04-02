#!/usr/bin/env python3
import json
import argparse
from re import I
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import netcdf

import os

# Because GitHub Classroom was not configured for geopy

try:

    from geopy.geocoders import Nominatim

except ImportError:

    os.system('pip3 install geopy')

    from geopy.geocoders import Nominatim




parser = argparse.ArgumentParser()
parser.add_argument('longitude', metavar='LON', type=str, help='Longitude, deg')
parser.add_argument('-latitude',  metavar='LAT', type=str, help='Latitude, deg') 

if __name__ == "__main__":
    args = parser.parse_args() 
    args.longitude = ' '.join(args.longitude.split(' ')[::-1]) 
    geolocator = Nominatim(user_agent="translator")
    location = geolocator.geocode(args.longitude) 
    print(location)
    args.longitude = 18.46
    args.latitude = 73.24

with netcdf.netcdf_file('MSR-2.nc', mmap=False) as netcdf_file:
    print("Dimension: {}".format(netcdf_file.dimensions))
    variables = netcdf_file.variables
    for v in variables:
        var = variables[v]
        print("Variable {} dims {} shape {}".format(v, var.dimensions, var.data.shape))
lon_index = np.searchsorted(variables['longitude'].data, args.longitude)
lat_index = np.searchsorted(variables['latitude'].data, args.latitude)



def task_1(a):
    return float(np.amax(a)), float(np.amin(a)), round(np.average(a),1)


all_ozon = np.array(variables['Average_O3_column'][:, lat_index, lon_index])


january_ozon= all_ozon[::12]



july_ozon = all_ozon[6::12]



t = np.array(variables['time'][:])
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('time (months)')
ax.set_ylabel('ozon (Dobs)')
plt.title("Ozone assessment")
ax.plot(t, all_ozon, label = 'all time')
ax.plot(t[::12], january_ozon, color = "red", label = 'january')
ax.plot(t[6::12], july_ozon, color = "green", label = 'july')
ax.legend()
ax.grid()

plt.savefig('ozon.png')



d = {
  "coordinates":
  [round(args.longitude,2), round(args.latitude,2)]
  ,
  "jan": {
    "min": task_1(january_ozon)[1],
    "max": task_1(january_ozon)[0],
    "mean": task_1(january_ozon)[2],
  },
  "jul": {
    "min": task_1(july_ozon)[1],
    "max": task_1(july_ozon)[0],
    "mean": task_1(july_ozon)[2]
  },
  "all": {
    "min": task_1(all_ozon)[1],
    "max": task_1(all_ozon)[0],
    "mean": task_1(all_ozon)[2]
  }
}

with open('ozon.json', 'w') as f:
    json.dump(d, f, indent=4)
