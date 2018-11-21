import matplotlib.pyplot as plt
import numpy as np
import scipy
import pandas as pd


# <editor-fold desc="Edit Pyplot default parameters">

params = {'legend.fontsize': 12,
          'figure.figsize': (11.5, 8), # standard A4
          'xtick.labelsize': 8
        # 'axes.titlesize':'x-large',
        # 'xtick.labelsize':'x-large',
        # 'ytick.labelsize':'x-large'
        }

plt.rcParams.update(params)
# </editor-fold>


# <editor-fold desc="Read Satellite data from csv">
satellite_data=pd.read_csv("Satellite_Data.csv")
# data of satellites
names=satellite_data["Name"]
azimuth=satellite_data["Azimuth"]
altitude=satellite_data["Altitude"]
longitude=satellite_data["Longitude"]
# </editor-fold>


# <editor-fold desc="Fitting and derivative polynomials">
coeffs = np.polyfit(azimuth,altitude,2)

poly_fit=np.poly1d(coeffs)
poly_fit_deriv=np.polyder(poly_fit)

a_max_azimuth=poly_fit_deriv.roots[0]
a_max=poly_fit(a_max_azimuth)

azimuth_fit_values= np.linspace(min(azimuth), max(azimuth), 200) # calculate 200 polyiaml values, so pictue looks smooth
poly_fit_values=np.polyval(poly_fit,azimuth_fit_values)
# </editor-fold>


# <editor-fold desc="Plotting">
fig=plt.figure()

ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax.set_xlim(min(azimuth_fit_values)-10, max(azimuth_fit_values)+10)

ax.set_title("Maximum observable geostationary altitude")
#plot satellites with errorbars
ax.errorbar(azimuth, altitude, xerr=0.5, yerr=0.5, fmt='*', markersize=2.5, ecolor='black',capsize=3, label="Satellite")
#plot the fit polynoial
ax.plot(azimuth_fit_values, poly_fit_values, label='Best Fit')
#put maximum point
ax.plot(a_max_azimuth, a_max, marker='o', markersize=4,  color= "red", label="Maximum")
# </editor-fold>


# <editor-fold desc="Labeling Datapoints">
specific_satellites=("Thor 3", "Eutelsat 5", "Eutelsat W3A")
specific_positioning= {
         "Thor 3" : dict(ha="right", va="top"),
         "Eutelsat 5": dict(ha="left", va="top"),
         "Eutelsat W3A": dict(ha="center",va="top"),
         }
specific_offsets= {
         "Thor 3" : {"x":0, "y": -0.1},
         "Eutelsat 5": {"x":0.3, "y": -0.1},
         "Eutelsat W3A": {"x":0, "y": -0.5},
    }
general_offset={"x":0, "y":0.6}

style = dict(size=10, color='black')
for index,satellite in satellite_data.iterrows():
    text=ax.text(satellite["Azimuth"]+general_offset["x"],
                 (satellite["Altitude"]+general_offset["y"]),
                 satellite["Name"], **style, ha="center")
    #fix Thor 3 leabel
    if satellite["Name"] in specific_satellites:
        text.set_visible(False) # first remove the text
        ax.text(satellite["Azimuth"]+specific_offsets[satellite["Name"]]["x"],
             satellite["Altitude"]+specific_offsets[satellite["Name"]]["y"],
             satellite["Name"]+" ",
             **style, **specific_positioning[satellite["Name"]])
# </editor-fold>


# <editor-fold desc="Labeling Maximum of Best Fit">
# Labeling Maximum of Best Fit
ax.annotate( "a_max="+str(round(a_max,2)),
             fontsize=10,
            # color="red",
             xy=(a_max_azimuth-0.2, a_max),
             xytext=(a_max_azimuth-12, a_max+0.5),
             arrowprops=dict(arrowstyle="->")
            )
# </editor-fold>


# <editor-fold desc="Axis labels and style">
ax.set_xlabel('Azimuth (degrees)')
ax.set_ylabel('Altitude (degrees)')
ax.legend()
#ax.set_xticks(azimuth)
#ax.set_yticks(altitude)
# </editor-fold>

plt.savefig('Maximum_observable_GEO_altitude.pdf')
plt.show()


