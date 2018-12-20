'''
Created on 28 Nov 2018

@author: Paul
@version: 1.0 (GUI)
'''
TESTING = False

import os
from os.path import dirname, join, expanduser
os.environ['KIVY_NO_CONSOLELOG']="True"

import kivy
kivy.require('1.10.1')
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock

import pandas as pd
import matplotlib
matplotlib.use('Agg')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import sys
from threading import Thread

class AnalysisScreen(Screen):
    def _test_check_vars(self):
        for value in self.ids:
            print(self.ids[value])

class TrackleteAnalysisApp(App):
    #processing vars
    excel_file_name = StringProperty('')
    additional_days = NumericProperty(0)
    N_days_used = NumericProperty(0)
    PLOT_WEIGHT = BooleanProperty()
    PLOT_HEARTRATE = BooleanProperty()
    PLOT_RATING = BooleanProperty()
    PLOT_SLEEP = BooleanProperty()
    WEIGHT_LINES = BooleanProperty()
    MALE_TRUE = BooleanProperty()
    SAVE_PLOTS = BooleanProperty()
    
    #GUI vars
    screen_names = ListProperty([])
    display_names = ListProperty([])
    hierarchy = ListProperty([])
    name_progress = StringProperty()
    val_progress = NumericProperty()
    plot_list = ListProperty([])
    athletes_loaded = BooleanProperty()
    athlete_current = StringProperty('')
    index = NumericProperty()
   
    def build(self):
        self.title = "Tracklete Analyzer"
        self.screens = {}
        self.available_screens = ['Fileloader', 'Setup', 'Athlete']
        self.name_progress = 'None'
        self.val_progress = 0
        self.screen_names = self.available_screens
        self.display_names = ['Setup']
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
            '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.file_loader_init()
        self.index = 1
        self.go_screen(1)
        self.athletes_loaded = False
        self.athlete_current = ''
    
    def file_loader_init(self):
        if not TESTING:
            if len(sys.argv) > 1:
                self.excel_file_name = sys.argv[1]
                if not self.excel_file_name[-4:]==('xlsx' or 'xls'):
                    # didn't actually supply an excel file
                    self.excel_file_name = 'None'
            else:
                # didn't supply a file at all
                self.excel_file_name = 'None'
        else:
            #for testing purposes
            self.excel_file_name = 'download.xlsx'
        
        if self.excel_file_name != 'None':
            self.bodystats_db = pd.ExcelFile(self.excel_file_name)
            if len(self.bodystats_db.sheet_names) == 1:
                # if singular bodystat export, only a single sheet
                self.name_list = self.bodystats_db.sheet_names
            else:
                # if team export, first 2 sheets contain attendance/ergo
                self.name_list = self.bodystats_db.sheet_names[2:]
    
    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        
    def go_screen_return(self):
        self.index = 1
        self.root.ids.sm.switch_to(self.load_screen(1), direction='right')
    
    def load_screen(self, idx):
        if idx in self.screens:
            return self.screens[idx]
        else:
            if idx <=1:
                screen = Builder.load_file(self.available_screens[idx])
                self.screens[idx] = screen
                return screen
            else:
                athlete_id = idx-3
                self.athlete_current = self.name_list[athlete_id]
                screen = Builder.load_file(self.available_screens[2])
                screen.ids.athlete_img.add_widget(FigureCanvasKivyAgg(self.plot_list[athlete_id]))
                return screen
    
    def _homepath(self):
        return join(expanduser('~'), "Downloads")
    
    def load_file(self, path, selection):
        self.excel_file_name = os.path.join(path, selection[0])
        
        if not self.excel_file_name[-4:]==('xlsx' or 'xls'):
            # didn't actually supply an excel file
            self.excel_file_name = 'None'
        
        if self.excel_file_name != 'None':
            self.bodystats_db = pd.ExcelFile(self.excel_file_name)
            if len(self.bodystats_db.sheet_names) == 1:
                # if singular bodystat export, only a single sheet
                self.name_list = self.bodystats_db.sheet_names
            else:
                # if team export, first 2 sheets contain attendance/ergo
                self.name_list = self.bodystats_db.sheet_names[2:]

        self.go_screen(1)
    
    def _test_check_vars(self, screen):
        self._read_ids_to_app(screen)
        print(self.additional_days)
        print(self.N_days_used)
        print(self.PLOT_WEIGHT)
        print(self.PLOT_HEARTRATE)
        print(self.PLOT_RATING)
        print(self.PLOT_SLEEP)
        print(self.WEIGHT_LINES)
    
    def _read_ids_to_app(self, screen):
        self.additional_days = int(screen.ids.additional_days.text)
        self.N_days_used = int(screen.ids.N_days_used.text)
        self.PLOT_WEIGHT = (True if screen.ids.PLOT_WEIGHT.state == 'down' else False)
        self.PLOT_HEARTRATE = (True if screen.ids.PLOT_HEARTRATE.state == 'down' else False)
        self.PLOT_RATING = (True if screen.ids.PLOT_RATING.state == 'down' else False)
        self.PLOT_SLEEP = (True if screen.ids.PLOT_SLEEP.state == 'down' else False)
        self.WEIGHT_LINES = screen.ids.WEIGHT_LINES.active
        self.MALE_TRUE = (True if screen.ids.MALE_TRUE.state == 'down' else False) #AVG_WEIGHT = 57!
        self.SAVE_PLOTS = screen.ids.SAVE_PLOTS.active
        if self.WEIGHT_LINES:
            if self.MALE_TRUE:
                self.AVG_WEIGHT = 70
            else:
                self.AVG_WEIGHT = 57
                
            if self.AVG_WEIGHT == 57: 
                self.MAX_WEIGHT = self.AVG_WEIGHT + 2.0
                self.WINT_MAX = self.MAX_WEIGHT + 2.5
            elif self.AVG_WEIGHT == 70:
                self.MAX_WEIGHT = self.AVG_WEIGHT + 2.5
                self.WINT_MAX = self.MAX_WEIGHT + 2.5
    
    def start_analysis(self):
        #first, check if there's actually an excel file chosen.
        if self.excel_file_name == 'None':
            layout = BoxLayout(orientation='vertical')
            label = Label(text="You haven't chosen an excel file yet!\nPlease go back and do so.", size_hint=(1,0.9))
            button = Button(text='Dismiss', size_hint=(1,0.1))
            layout.add_widget(label)
            layout.add_widget(button)
            popup = Popup(title="No excel file chosen", content=layout, size=layout.size)
            button.bind(on_press=popup.dismiss)
            popup.open()
        else:
            self.athletes_loaded = False
            self.display_names = ['Setup']
            self.analysis_thread = Thread(target=self.run_analysis)
            self.analysis_thread.start()
            Clock.schedule_interval(self.analysis_warnings, 1./30.)
            if TESTING: print("scheduled.")

    def analysis_warnings(self, dt):
        if (len(self.insufficient_data)>0 or len(self.no_data)>0) and self.athletes_loaded:
            Clock.unschedule(self.analysis_warnings)
            if TESTING: print("unscheduled.")
            # creates warning popup for errors during plot creation
            warn_title = 'WARNINGS: Plot Creation'
            warn_string = 'There were some problems with creating your plots. None of these are critical, so no need to worry.\n'
            for warn in self.insufficient_data:
                warn_string += "\nData for athlete {} has fewer data entries than you required, using all available data ({} days) instead.".format(warn[0], warn[1])
            for warn in self.no_data:
                warn_string += "\n\nNo {} data found for athlete {}. This plot will be left empty.".format(warn[0], warn[1])
            
            layout = BoxLayout(orientation='vertical')
            label = Label(text=warn_string, size_hint=(1,0.9))
            button = Button(text='Dismiss', size_hint=(1,0.1))
            layout.add_widget(label)
            layout.add_widget(button)
            popup = Popup(title=warn_title, content=layout, size=layout.size)
            button.bind(on_press=popup.dismiss)
            popup.open()
            self.insufficient_data = []
            self.no_data = []
    
    def run_analysis(self):     
        screen = self.root.ids.sm.current_screen
        screen.ids.bombshell.disabled = True
        self._read_ids_to_app(screen)
#         if TESTING: self._test_check_vars(screen)
        PLOTS = [self.PLOT_WEIGHT, self.PLOT_HEARTRATE, self.PLOT_RATING, self.PLOT_SLEEP]
        if self.excel_file_name == None:
            popup = Popup(title='ERROR: You have not supplied a valid Excel file', content=Label(text="ERROR: You haven't supplied a valid Excel file yet.\nPlease go back and do so."), size_hint=(None, None), size=(400, 400))
            popup.open()
        elif sum(PLOTS) == 0: 
            popup = Popup(title='ERROR: No plots enabled', content=Label(text="You have not enabled any plots;\nplease go back and select any number of plots to create."), size_hint=(None, None), size=(400, 400))
            popup.open()
        else:
            #warning and plot lists
            self.insufficient_data = []
            self.no_data = []
            self.plot_list = []
            name_count = 0
            
            for name in self.name_list:
                """ For each in name in name_list, make a plot """
#                 if TESTING: print("Creating plots for {}".format(name))
                self.name_progress = name
                self.val_progress = int(name_count / len(self.name_list) * 100.)
                name_count += 1
                
                fig, axes = plt.subplots(sum(PLOTS),1,sharex=True,figsize=(12,12))
                if sum(PLOTS) == 1:
                    axes = [axes]
                 
                input_file = self.bodystats_db.parse(name)
                 
                if self.N_days_used != 0:
                    """ Optional Param: N_days_used implementation. """
                    len(input_file)
#                     if TESTING: print("using input_file[{}:]".format(self.N_days_used))
                    if self.N_days_used <= len(input_file): 
                        input_file = input_file[:self.N_days_used]
                    else:
                        available_data = len(input_file)
                        self.insufficient_data.append([name, available_data])
                        if TESTING: print("Data for athlete {} has fewer than N_days_used ({}) data entries, using all available data ({}) instead.".format(name, self.N_days_used, len(input_file)))
             
                plot_counter = 0
                 
                if PLOTS[0]:
                    #################
                    ## WEIGHT PLOT ##
                    #################
                     
                    input_file['Date'] =  pd.to_datetime(input_file['Date'], dayfirst=True)
                     
                    x, y = input_file['Date'], input_file['Weight [kg]']
                    if y.isnull().all() == False:
                        x = mdates.date2num(x)
                        idx = np.isfinite(x) & np.isfinite(y)
                        axes[plot_counter].plot(x[idx],y[idx],label="data")
                         
                        xx = np.linspace(x.min(), x.max()+self.additional_days, 100)
                        dd = mdates.num2date(xx)
                         
                        z1 = np.polyfit(x[idx], y[idx], 1)
                        p1 = np.poly1d(z1)
                        axes[plot_counter].plot(dd,p1(xx),"r--",label=r"Trend, 1st order [$\Delta$={}{:.2}/w]".format(("+" if z1[0]>0 else ""), z1[0]*7))
                         
                        z2 = np.polyfit(x[idx], y[idx], 2)
                        p2 = np.poly1d(z2)
                        axes[plot_counter].plot(dd,p2(xx),"g--",lw=0.8,label="Trend, 2nd order".format("a"))
                         
                        if self.WEIGHT_LINES:
                            """ Weight lines implementation. """
                            w = input_file['Weight [kg]']
                            if np.max(w) >= self.WINT_MAX-1.:
                                axes[plot_counter].axhline(self.WINT_MAX,color="black",lw=0.8, ls=':')
                            axes[plot_counter].axhline(self.MAX_WEIGHT,color="black",ls="--",lw=0.8)
                            if np.min(w) < self.MAX_WEIGHT-1.:
                                axes[plot_counter].axhline(57.0,color="black",ls="-.",lw=0.8)
                         
                        axes[plot_counter].legend()
                        axes[plot_counter].set(ylabel="Weight [kg]",xlim=(x.min(), x.max()+self.additional_days))
                    else:
                        self.no_data.append(['weight', name])
                        if TESTING: print("WARNING: No weight data found for athlete {}.\nThis plot will be empty.".format(name))
                     
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
                         
                        xx = np.linspace(x.min(), x.max()+self.additional_days, 100)
                        dd = mdates.num2date(xx)
                          
                        z1 = np.polyfit(x[idx], y[idx], 1)
                        p1 = np.poly1d(z1)
                        axes[plot_counter].plot(dd,p1(xx),"r--",label="trend, 1st order")
                           
                        z2 = np.polyfit(x[idx], y[idx], 2)
                        p2 = np.poly1d(z2)
                        axes[plot_counter].plot(dd,p2(xx),"g--",lw=0.8,label="trend, 2nd order")
                          
                        axes[plot_counter].axhline(np.mean(input_file['Heartrate [bpm]']),label="avg",color="black",lw=0.8,ls="-.")
                        axes[plot_counter].legend(ncol=4)
                        axes[plot_counter].set(ylabel="Heartrate [bpm]",xlim=(x.min(), x.max()+self.additional_days))
                    else:
                        self.no_data.append(['heartrate', name])
                        if TESTING: print("WARNING: No heartrate data found for athlete {}\nThis plot will be empty.".format(name))
                     
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
                         
                        xx = np.linspace(x.min(), x.max()+self.additional_days, 100)
                        dd = mdates.num2date(xx)
                            
                        z1 = np.polyfit(x[idx], y[idx], 1)
                        p1 = np.poly1d(z1)
                        axes[plot_counter].plot(dd,p1(xx),"r--",label="trend, 1st order")
                           
                        z2 = np.polyfit(x[idx], y[idx], 2)
                        p2 = np.poly1d(z2)
                        axes[plot_counter].plot(dd,p2(xx),"g--",lw=0.8,label="trend, 2nd order")
                            
                        axes[plot_counter].axhline(np.mean(input_file['Rating [1:10]']),label="avg", color="black",lw=0.8,ls="-.")
                            
                        axes[plot_counter].legend(ncol=4)
                        axes[plot_counter].set(ylabel="Rating [1:10]",ylim=(-0.5,10.5),xlim=(x.min(), x.max()+self.additional_days))
                    else:
                        self.no_data.append(['rating', name])
                        if TESTING: print("WARNING: No rating data found for athlete {}\nThis plot will be empty.".format(name))
             
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
                         
                        xx = np.linspace(x.min(), x.max()+self.additional_days, 100)
                        dd = mdates.num2date(xx)
                         
                        z1 = np.polyfit(x[idx], y[idx], 1)
                        p1 = np.poly1d(z1)
                        axes[plot_counter].plot(dd,p1(xx),"r--",label="trend, 1st order")
                           
                        z2 = np.polyfit(x[idx], y[idx], 2)
                        p2 = np.poly1d(z2)
                        axes[plot_counter].plot(dd,p2(xx),"g--",lw=0.8,label="trend, 2nd order")
                          
                        axes[plot_counter].axhline(np.mean(input_file['Sleep [h]']),label="avg",color="black",lw=0.8,ls="-.")
                        axes[plot_counter].legend(ncol=4)
                        axes[plot_counter].set(ylabel="Sleep [h]",xlim=(x.min(), x.max()+self.additional_days))
                    else:
                        self.no_data.append(['sleep', name]) 
                        if TESTING: print("WARNING: No sleep data found for athlete {}\nThis plot will be empty.".format(name)) 
                     
                    plot_counter+=1
             
                #######################
                ## PLOTTING BUSINESS ##
                #######################
                 
                axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
                axes[-1].set_xlabel("Date")
                axes[0].set_title("{}: Trends".format(name))
                if self.SAVE_PLOTS: 
                    if not os.path.isdir(join(os.path.dirname(self.excel_file_name), "Tracklete Trends")):
                        os.mkdir(join(os.path.dirname(self.excel_file_name), "Tracklete Trends"))
                    fig.savefig(join(os.path.dirname(self.excel_file_name), "Tracklete Trends", "Tracklete_Trends_{}.png".format(name)))
#                         os.mkdir(join("..", "Tracklete Trends"))
#                     fig.savefig(join("..", "Tracklete Trends", "Tracklete_Trends_{}.png".format(name)))
                self.plot_list.append(fig)
                self.display_names.append(name)
                self.screen_names.append(name)

            self.name_progress = 'Done'
            self.val_progress = 100
            screen.ids.bombshell.disabled = False
            self.athletes_loaded = True
#             self.root.ids.spnr.focus()
            
if __name__ == '__main__':
    TrackleteAnalysisApp().run()
