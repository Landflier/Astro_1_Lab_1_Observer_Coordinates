import matplotlib.pyplot as plt
import numpy as np
import scipy
import pandas as pd
import matplotlib.ticker as ticker

# SMALL_SIZE = 8
# MEDIUM_SIZE = 10
# BIGGER_SIZE = 12
#
# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
# plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
# plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
# plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


# <editor-fold desc="Edit Pyplot default parameters">

params = {'legend.fontsize': 12,
          'figure.figsize': (11.5, 8), # standard A4
        #  'xtick.labelsize': 7
        # 'axes.titlesize':'x-large',
        # 'xtick.labelsize':'x-large',
        # 'ytick.labelsize':'x-large'
        }

plt.rcParams.update(params)
# </editor-fold>

# <editor-fold desc="Reading Motion along ecliptic Data">
satellite_data=pd.read_csv("Motion_Along_ecliptic.csv")
# data of satellites
names=satellite_data["Name"]
azimuth=satellite_data["Azimuth"]
altitude=satellite_data["Altitude"]
longitude=satellite_data["Longitude"]
corrected_azimuth=180-azimuth
# </editor-fold>

# <editor-fold desc="Fitting Polynomials">
#polynomial fitting
coeffs = np.polyfit(longitude,corrected_azimuth,1)

poly_fit=np.poly1d(coeffs)
poly_fit_deriv=np.polyder(poly_fit)
poly_fit_values=np.polyval(poly_fit,longitude)

observer_longitude=poly_fit.roots[0] # since only line intercept, take first from list

print("geo longitude for observer: ",observer_longitude)
# </editor-fold>


# <editor-fold desc="Plotting">
fig = plt.figure() # fig size in inches


ax = fig.add_axes([0.1, 0.1, 0.8, 0.8]) #add_axes takes 4 param: xmin,ymin- lower left corner, dx,dy- width and height,
                                        #values between 0 and 1., since part of graph
ax.set_title("Estimated observer longitude (" +'$\lambda$)', fontsize='large')
ax.set_xlim(min(longitude)-10, max(longitude)+10) # give more space, so Telstar (first point) fits in graph

#plot satellites, best fit, and 0 intercept
ax.errorbar(longitude, corrected_azimuth,yerr=1, fmt='o', label="Satellites", markersize=2.5)
ax.plot(longitude,poly_fit_values, label="Best fit line")
ax.plot(observer_longitude, poly_fit(observer_longitude), marker='o', markersize=4,  color= "red", label="Observer Longitude") # 2plot estimated longitude

ax.legend() # add legend
# </editor-fold>

# <editor-fold desc="Object Labels">
style = dict(size=9, color='black', ha="right",)
general_offset={"x":0, "y":1.4}

for index,satellite in satellite_data.iterrows():
    ax.text(satellite["Longitude"]+general_offset["x"],
            (180-satellite["Azimuth"])+general_offset["y"],
            satellite["Name"], **style )
# </editor-fold>

ax.annotate( '$\lambda =$'+str(round(observer_longitude,2)),
           #color="red",
            fontsize=9,
            xy=(observer_longitude, -0.5),#  xycoords='data',
            xytext=(observer_longitude-1, -8),# textcoords='offset points',
            arrowprops=dict(arrowstyle="->")
             )

# <editor-fold desc="All axes styles">
#Show only ticks for points on graph
#ax.set_xticks(longitude)
#ax.set_yticks(corrected_azimuth)

ax.set_xlabel('longitude (degrees)')
ax.set_ylabel('180-azimuth (degrees)')

ax.axhline(0, linestyle='--', color='k',linewidth=0.6) # horizontal lines
ax.axvline(0, linestyle='--', color='k',linewidth=0.6) # vertical lines
# </editor-fold>

plt.savefig('azimuth_longitude.pdf')
#
plt.show()


