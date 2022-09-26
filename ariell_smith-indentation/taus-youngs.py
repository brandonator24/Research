"""
Author: Brandon Pardi
Created: 9/14/2022, 12:45 pm
Last Modified: 9/18/2022 4:44pm
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
import sys


'''
README
- grabs data from 'taus-youngs.csv' and organizes it into multiple dataframes for grouping swarm and boxplots
    - see README for 'indentation_data.py to see how the csv is generated
    - also doubles checks for duplicate entries in the csv and rewrites to it if duplicated were found
- 4 swarm/box plots will be generated for each figure
    - 1 figure each for Tau, Tau_rsq, E, E_rsq
    - each figure will contain a plot for soft, stiff, soft_viscoelastic, stiff_viscoelastic

WIP
- currently viscoelastic data does not exist yet.
'''

# error checking for opening csv file into df
try:
    df = pd.read_csv("aggregate_data/taus-youngs.csv")
except pd.errors.EmptyDataError as empty_err:
    print(f"Data frame empty!\nerr: {empty_err}")
    sys.exit(1)
except pd.errors.ParserError as parse_err:
    print(f"Could not parse CSV, check for improper delimiters\n(clear csv and try again)\n{parse_err}")
    sys.exit(1)

df = df.drop_duplicates()
#df.to_csv("aggregate_data/taus-youngs.csv", index=False)

tau_df = df[['Tau', 'data_category']]
tau_rsq_df = df[['T_rsq', 'data_category']]
E_df = df[['E', 'data_category']]
E_rsq_df = df[['E_rsq', 'data_category']]

'''
figure 1: Taus
figure 2: Tau rsq
figure 3: Youngs Modulus
figure 4: Youngs mod rsq
'''

plt.figure(1)
swarm1 = sns.swarmplot(x='data_category', y='Tau', data=tau_df)
box1 = sns.boxplot(x='data_category', y='Tau', data=tau_df, boxprops={'facecolor':'None'})
medians1 = tau_df.groupby(['data_category'])['Tau'].median()
v_offset1 = tau_df['Tau'].median() * 0.02 # offset so display isn't right on line
for xtick in box1.get_xticks():
    box1.text(xtick,medians1[xtick] + v_offset1,medians1[xtick], horizontalalignment='center', size='x-small', color='b')
plt.savefig("taus-youngs_plots/TAUS-swarmplot.png")

plt.figure(2)
swarm2 = sns.swarmplot(x='data_category', y='T_rsq', data=tau_rsq_df)
box2 = sns.boxplot(x='data_category', y='T_rsq', data=tau_rsq_df, boxprops={'facecolor':'None'})
medians2 = tau_rsq_df.groupby(['data_category'])['T_rsq'].median()
v_offset2 = tau_rsq_df['T_rsq'].median() * 0.005
for xtick in box2.get_xticks():
    box2.text(xtick,medians2[xtick] + v_offset2,medians2[xtick], horizontalalignment='center', size='x-small', color='b')
plt.savefig("taus-youngs_plots/TAUS-RSQ-swarmplot.png")

plt.figure(3)
swarm3 = sns.swarmplot(x='data_category', y='E', data=E_df)
box3 = sns.boxplot(x='data_category', y='E', data=E_df, boxprops={'facecolor':'None'})
medians3 = E_df.groupby(['data_category'])['E'].median()
v_offset3 = E_df['E'].median() * 0.02
for xtick in box3.get_xticks():
    box3.text(xtick,medians3[xtick] + v_offset3,medians3[xtick], horizontalalignment='center', size='x-small', color='b')
plt.savefig("taus-youngs_plots/YOUNGS-swarmplot.png")

plt.figure(4)
swarm4 = sns.swarmplot(x='data_category', y='E_rsq', data=E_rsq_df)
box4 = sns.boxplot(x='data_category', y='E_rsq', data=E_rsq_df, boxprops={'facecolor':'None'})
medians4 = E_rsq_df.groupby(['data_category'])['E_rsq'].median()
v_offset4 = E_rsq_df['E_rsq'].median() * 0.005
for xtick in box4.get_xticks():
    box4.text(xtick,medians4[xtick] + v_offset4,medians4[xtick], horizontalalignment='center', size='x-small', color='b')
plt.savefig("taus-youngs_plots/YOUNGS-RSQ-swarmplot.png")