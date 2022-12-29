"""
Author: Brandon Pardi
Created: 12/28/2022, 3:45 pm
Last Modified: 12/28/2022 10:35 pm
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

'''
WIP
- 

'''

def gaussian(x, a, b, c, d):
    return a * np.exp(-(x - b) ** 2 / (2 * c ** 2)) + d

# function to find array value closest to passed in value
# used to find values in data closes to the results of the curve fit
def find_nearest(array, value):
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    return array[index], index

# grab data
df = pd.read_csv("fiji_data/PAA intensity profile2.csv")
xdata = df['Distance_(pixels)'].values
ydata = df['Gray_Value'].values

# set up plots
span_plot = plt.figure()
span_plot.set_figwidth(10)
span_plot.set_figheight(6)
span_ax = span_plot.add_subplot(2,1,1) # main plot data
zoom_ax = span_plot.add_subplot(2,1,2) # zoomed data and fit
span_ax.set_title("Click and drag to select range")

# plotting the data
raw_plot, = span_ax.plot(xdata, ydata, '.', color='blue', markersize=1, label='raw intensity data')
zoom_plot, = zoom_ax.plot(xdata, ydata, '.', color='green', markersize=2, label='spanned intensity data')

# function called by span selector when a selection is made
# is given the min and max from the span selected, and returns void
def onselect(xmin, xmax):
    zoom_ax.clear()
    # find indices of data points corresponding to selection
    imin, imax = np.searchsorted(xdata, (xmin, xmax))
    imax = min(len(xdata)-1, imax)

    # grab data corresponding to that region
    xspan = xdata[imin:imax]
    yspan = ydata[imin:imax]

    # plot the newly specified range
    zoom_ax.plot(xspan, yspan, '.', color='green', markersize=4, label='spanned intensity data')

    # initial paramaters for gaussian fit
    mean = sum(xspan * yspan) / sum(yspan)
    sigma = np.sqrt(sum(yspan * (xspan - mean) ** 2) / sum(yspan))
    p0 = [max(yspan), mean, sigma, 0]

    # perform curve fit on specified range
    params, covariance = curve_fit(gaussian, xspan, yspan, p0=p0)
    print(f"Gauss fit paramaters: {params}")

    # generate data for a smooth curve for this fit
    # note: xdata is input so we use it also for the fit data
    xfit = np.linspace(np.min(xdata), np.max(xdata), 1000)
    yfit = gaussian(xfit, *params)

    # plot the fit data on top of the zoomed plot
    zoom_ax.plot(xfit, yfit, 'black', label='gaussian fit')

    # grab applicable data from fit
    x0_gauss, x0_ind_gauss = find_nearest(xspan, params[1]) # xpoint in data closest to curves peak
    y0_gauss = yspan[x0_ind_gauss]
    print(f"Gaussian Fit method: x0 - {x0_gauss}; y0 - {y0_gauss}\n")
    
    # alternative method of finding min point, grouping and averaging
    mins = np.partition(yspan, 4)[0:5]
    avg_min_val = mins.mean() # multiple occurences of this may occur in list
    y0_avg, _ = find_nearest(yspan, avg_min_val)
    # take median value of all occurences of the found average
    y0_avg_indices = np.where(yspan==y0_avg)[0]
    y0_avg_ind = int(np.median(y0_avg_indices))
    x0_avg = xspan[y0_avg_ind]
    print(f"Mins: {mins}; Avg Min: {avg_min_val};\nIndices w/ closest avg min:{y0_avg_indices}; median index: {y0_avg_ind}")
    print(f"Average Values method: x0 - {x0_avg}; y0 - {y0_avg}\n")

    # plot the different found min points
    zoom_ax.scatter(x=x0_gauss, y=y0_gauss, c='red', label=f'gaussian minima: {x0_gauss}, {y0_gauss}', zorder=4)
    zoom_ax.scatter(x=x0_avg, y=y0_avg, c='purple', label=f'average minima: {x0_avg}, {y0_avg}', zorder=5)

    # set limits so plot is zoomed to fit
    zoom_ax.set_xlim(xspan.min()-5, xspan.max()+5)
    zoom_ax.set_ylim(min(yspan.min(),yfit.min())-5, max(yspan.max(), yfit.max())+5)
    plt.legend()
    span_plot.canvas.draw_idle()
    

# Add the span selector widget
span = SpanSelector(span_ax, onselect, 'horizontal', useblit=True, span_stays=True,
                    rectprops=dict(alpha=0.3, facecolor='gray'))

plt.show()