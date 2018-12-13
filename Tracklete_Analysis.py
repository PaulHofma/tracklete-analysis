'''
Created on 19 Nov 2018

@author: Paul Hofma
@version: 1.0.1 (GUILESS VERSION)

@disclaimer:
You're advised to take any and all trends it reproduces with a good dose of salt and 
common sense. These are simply the trends visible in the data, and while the graph extrapolates for 
another 2 weeks by default, these results are (obviously) not guaranteed. In addition, 1st and 2nd order
interpolations are by their nature rather simplistic, and especially e.g. weight graph may display
something more like exponential or slightly sinusoidal behaviour; none of this will be modelled 
(though perhaps it may be in a future version).

TL;DR - human fysiology is complicated. These graphs are simple. Draw your conclusions with some caution.

'''

##################
## INSTRUCTIONS ##
##################
"""
Current version takes in a csv file with Tracklete bodystats, and returns (and saves) graphs for weight,
heartrate, and mood. Also draws trend lines in all of these, both 1st (linear) and second (quadratic) order.

HOW TO USE:
1. Export bodystats as excel (either individual or group) from Tracklete.io

2. Set parameters in OPTIONAL PARAMS below as desired.
    
3. Run script by dragging bodystat-excel onto the program.

"""
######################################################
## OPTIONAL PARAMS - SET THESE YOURSELF IF YOU WANT ##
######################################################
"""
Want to see the trend developed for longer/shorter? As implied in the name, measured in days.
Shorter/longer may be appropriate, especially if you have either few/a lot of data. 
""" 
additional_days = 7

"""
Want to only use the last N days of data? Default is use all available data; leave 0 in this case.
Useful if you just want to analyse recent vs global trends.
Note that results with fewer data will give less reliable results.
"""
N_days_used = 30

"""
Which plots do you want to see?
Set to False to disable plot, or True to enable plot.
Default plots weight, heartrate, and rating (how they're feeling), and omits hours slept.
Note that more than three graphs will likely get a bit crowded (depending on your monitor).
"""
PLOT_WEIGHT = True
PLOT_HEARTRATE = True
PLOT_RATING = True
PLOT_SLEEP = False

"""
Do you want additional weight lines? Mostly useful for lightweight coaches.
If so, enter average weights (summer) below, and set 'WEIGHT_LINES' to True.
Plots will then get lines (when relevant) for:
    - max weight (winter)
    - max weight (summer)
    - avg weight (summer)
"""
WEIGHT_LINES = True
AVG_WEIGHT = 57

##########################
##                      ##
##   --   SETUP   --    ##
##                      ##
##########################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import sys

TESTING = False

if not TESTING:
    assert len(sys.argv) > 1, "You did not provide a file to run."
    excel_file_name = sys.argv[1]
    assert excel_file_name[-4:]==('xlsx' or 'xls'), "You did not provide an Excel file."
else:
    excel_file_name = 'download.xlsx'
#     excel_file_name = 'download singular.xlsx'
#     excel_file_name = 'download (2).xlsx'

bodystats_db = pd.ExcelFile(excel_file_name)
if len(bodystats_db.sheet_names) == 1:
    # if singular bodystat export 
    name_list = bodystats_db.sheet_names
else:
    # if team export, first 2 sheets contain attendance/ergo
    name_list = bodystats_db.sheet_names[2:]

if TESTING: print(name_list)

if WEIGHT_LINES:
    assert(AVG_WEIGHT == 57 or AVG_WEIGHT == 70), "The average athlete weight provided doesn't match either 57 or 70 kg."
    if AVG_WEIGHT == 57: 
        MAX_WEIGHT = AVG_WEIGHT + 2.0
        WINT_MAX = MAX_WEIGHT + 2.5
    elif AVG_WEIGHT == 70:
        MAX_WEIGHT = AVG_WEIGHT + 2.5
        WINT_MAX = MAX_WEIGHT + 2.5       
        
################
## PLOT STUFF ##
################

PLOTS = [PLOT_WEIGHT, PLOT_HEARTRATE, PLOT_RATING, PLOT_SLEEP]
assert sum(PLOTS) != 0, "You have not enabled any plots! See Optional Parameters."

for name in name_list:
    """ For each in name in name_list, make a plot """
    print("Creating plots for {}".format(name))
    fig, axes = plt.subplots(sum(PLOTS),1,sharex=True,figsize=(12,12))
    if sum(PLOTS) == 1:
        axes = [axes]
    
    input_file = bodystats_db.parse(name)
    
    if N_days_used != 0:
        """ Optional Param: N_days_used implementation. """
        len(input_file)
        if TESTING: print("using input_file[{}:]".format(N_days_used))
        if N_days_used <= len(input_file):
#             print((len(input_file)-N_days_used), len(input_file)) 
            input_file = input_file[:N_days_used]
#             print(input_file)
        else:
            print("Data for athlete {} has fewer than N_days_used ({}) data entries, using all available data ({}) instead.".format(name, N_days_used, len(input_file)))

    plot_counter = 0
    
    if PLOTS[0]:
        #################
        ## WEIGHT PLOT ##
        #################
        
        # print input_file
        input_file['Date'] =  pd.to_datetime(input_file['Date'], dayfirst=True)
        
        x, y = input_file['Date'], input_file['Weight [kg]']
        if y.isnull().all() == False:
            x = mdates.date2num(x)
            idx = np.isfinite(x) & np.isfinite(y)
            axes[plot_counter].plot(x[idx],y[idx],label="data")
            
            xx = np.linspace(x.min(), x.max()+additional_days, 100)
            dd = mdates.num2date(xx)
            
            z1 = np.polyfit(x[idx], y[idx], 1)
            p1 = np.poly1d(z1)
            axes[plot_counter].plot(dd,p1(xx),"r--",label=r"Trend, 1st order [$\Delta$={}{:.2}/w]".format(("+" if z1[0]>0 else ""), z1[0]*7))
            
            z2 = np.polyfit(x[idx], y[idx], 2)
            p2 = np.poly1d(z2)
            axes[plot_counter].plot(dd,p2(xx),"g--",lw=0.8,label="Trend, 2nd order".format("a"))
            
            if WEIGHT_LINES:
                """ Weight lines implementation. """
                w = input_file['Weight [kg]']
                if np.max(w) >= WINT_MAX-1.:
                    axes[plot_counter].axhline(WINT_MAX,color="black",lw=0.8, ls=':')
                axes[plot_counter].axhline(MAX_WEIGHT,color="black",ls="--",lw=0.8)
                if np.min(w) < MAX_WEIGHT-1.:
                    axes[plot_counter].axhline(57.0,color="black",ls="-.",lw=0.8)
            
            axes[plot_counter].legend()
            axes[plot_counter].set(ylabel="Weight [kg]",xlim=(x.min(), x.max()+additional_days))
        else:
            print("WARNING: No weight data found for athlete {}.\nThis plot will be empty.".format(name))
        
        plot_counter+=1
    
    if PLOTS[1]:
        ####################
        ## HEARTRATE PLOT ##
        ####################
         
        x, y = input_file['Date'], input_file['Heartrate [bpm]']
        if y.isnull().all() == False:
            x = mdates.date2num(x)
            idx = np.isfinite(x) & np.isfinite(y)
            axes[plot_counter].plot(x[idx],y[idx],label="data")
            
            xx = np.linspace(x.min(), x.max()+additional_days, 100)
            dd = mdates.num2date(xx)
             
            z1 = np.polyfit(x[idx], y[idx], 1)
            p1 = np.poly1d(z1)
            axes[plot_counter].plot(dd,p1(xx),"r--",label="trend, 1st order")
              
            z2 = np.polyfit(x[idx], y[idx], 2)
            p2 = np.poly1d(z2)
            axes[plot_counter].plot(dd,p2(xx),"g--",lw=0.8,label="trend, 2nd order")
             
            axes[plot_counter].axhline(np.mean(input_file['Heartrate [bpm]']),label="avg",color="black",lw=0.8,ls="-.")
            axes[plot_counter].legend(ncol=4)
            axes[plot_counter].set(ylabel="Heartrate [bpm]",xlim=(x.min(), x.max()+additional_days))
        else:
            print("WARNING: No heartrate data found for athlete {}\nThis plot will be empty.".format(name))
        
        plot_counter+=1
     
    if PLOTS[2]:
        ################
        ## FEELY PLOT ##
        ################
          
        x, y = input_file['Date'], input_file['Rating [1:10]']
        if y.isnull().all() == False:
            x = mdates.date2num(x)
            idx = np.isfinite(x) & np.isfinite(y)
            axes[plot_counter].plot(x[idx],y[idx],label="data")
            
            xx = np.linspace(x.min(), x.max()+additional_days, 100)
            dd = mdates.num2date(xx)
               
            z1 = np.polyfit(x[idx], y[idx], 1)
            p1 = np.poly1d(z1)
            axes[plot_counter].plot(dd,p1(xx),"r--",label="trend, 1st order")
              
            z2 = np.polyfit(x[idx], y[idx], 2)
            p2 = np.poly1d(z2)
            axes[plot_counter].plot(dd,p2(xx),"g--",lw=0.8,label="trend, 2nd order")
               
            axes[plot_counter].axhline(np.mean(input_file['Rating [1:10]']),label="avg", color="black",lw=0.8,ls="-.")
               
            axes[plot_counter].legend(ncol=4)
            axes[plot_counter].set(ylabel="Rating [1:10]",ylim=(-0.5,10.5),xlim=(x.min(), x.max()+additional_days))
        else:
            print("WARNING: No rating data found for athlete {}\nThis plot will be empty.".format(name))

        plot_counter+=1
    
    if PLOTS[3]:
        ################
        ## SLEEP PLOT ##
        ################
         
        x, y = input_file['Date'], input_file['Sleep [h]']
        if y.isnull().all() == False:
            x = mdates.date2num(x)
            idx = np.isfinite(x) & np.isfinite(y)
            axes[plot_counter].plot(x[idx],y[idx],label="data")
            
            xx = np.linspace(x.min(), x.max()+additional_days, 100)
            dd = mdates.num2date(xx)
            
            z1 = np.polyfit(x[idx], y[idx], 1)
            p1 = np.poly1d(z1)
            axes[plot_counter].plot(dd,p1(xx),"r--",label="trend, 1st order")
              
            z2 = np.polyfit(x[idx], y[idx], 2)
            p2 = np.poly1d(z2)
            axes[plot_counter].plot(dd,p2(xx),"g--",lw=0.8,label="trend, 2nd order")
             
            axes[plot_counter].axhline(np.mean(input_file['Sleep [h]']),label="avg",color="black",lw=0.8,ls="-.")
            axes[plot_counter].legend(ncol=4)
            axes[plot_counter].set(ylabel="Sleep [h]",xlim=(x.min(), x.max()+additional_days))
        else: 
            print("WARNING: No sleep data found for athlete {}\nThis plot will be empty.".format(name)) 
        
        plot_counter+=1

    #######################
    ## PLOTTING BUSINESS ##
    #######################
    
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
    axes[-1].set_xlabel("Date")
    axes[0].set_title("{}: Trends".format(name))
    fig.savefig("Tracklete_Trends_{}.png".format(name))
    if TESTING: plt.show()
    
input("Finished! Press enter to close.")
