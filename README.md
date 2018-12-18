# Trackelete Analyzer V1.0.1
A pretty small piece of software, which does one thing very well: take exported bodystat data from <a href="http://tracklete.io">Tracklete</a>, and transform these into useful graphs for humans (or, rather, coaches).

## Example Results
![Bodystat Analysis Example](Tracklete_Trends_Paul%20Hofma.png)

## How it works - App Version
If you've downloaded the .zip file, you'll find that it contains a folder and a (shortcut to a) file called Tracklete_Analysis.exe. The latter file is all you'll ever need to touch, so don't worry about the folder. You can put this shortcut file anywhere you like, it'll work regardless. Note that the first time you start it up it may take a little longer than normal (approx. 10 seconds or so), afterwards it should be much faster. Data should ONLY be gotten from Tracklete, which gives you either a batch excel sheet (containing data for all your athletes) or a sheet with the bodystats for a single athlete. Note that the app was designed to take in the files as presented by Tracklete, and so if you've kept your own set of excel files for whatever reason it won't necessarily load them. You can load in your excel file(s) either by dropping them onto the app itself, or by using the built-in fileloader. 

You've got a few options to fiddle with, all of which are presented on the main screen. Once you're happy with your setup, simply click 'Create Plots' at the bottom. Once it's finished, you'll be able browse through the created graphs using the menu in the top right, or (if you chose to do so) browse them at your leisure on your pc. Fullscreen is advised if you're going to look at your graphs; they're saved at fairly large size, and the in-app version will scale with the window size.

## How it works - GUI-less version
This functions much like the GUI version, except that you'll have to set the options inside the Python script itself. They're pretty clearly labeled and can be found under the header OPTIONAL PARAMS, so you should find them pretty easily. Loading excel files for the GUI-less version is only possible by drag-and-dropping the excel file of choice onto the python script. You'll get a terminal window showing you the progress as it's happening. As it goes, it will create the graphs you specified (more on that below) for each athlete (or just for the one athlete) including the relevant trend lines, and tell you when it's done.

You export your data from Tracklete, which gives you either a batch excel sheet (containing data for all your athletes) or a sheet with the bodystats for a single athlete. You then simply proceed to drag-and-drop this excel file onto the the Python script (by default named Tracklete_Analysis.py) and you'll get a terminal shell showing you the progress as it's happening. As it goes, it will create the graphs for each athlete as specified, and tell you when it's done.

Most important benefit? Only Python and basic libraries required, and the 'program' is just a few kb worth of python script compared to a few hundred MB worth of app.

## Options Available
The options currently available for your graphs are:
 - Additional days : this lets you set a number of additional days for which to plot the trends. Useful to get an indication of where the trend is heading.
 - Total number of days to use : this lets you set how many days (starting at the most recent and counting backwards) of data you want to use. Useful to see investigate trends over longer or shorter periods of time. Note that trends over shorter periods will _by definition_ be less reliable predictors!
 - Plots to include : these are your on/off switches for which of the 4 'types' of bodystats (weight, heartrate, rating<sup>[1](#myfootnote1)</sup>, sleep) you want to plot.
 - Weight lines : whether to include lines to indicate a certain weight requirement; built in such a way that you only need to set this to true and then enter the average weight for your category (presumably 70 for men and 57 for women).
 - Save Plots (_app only_) : whether to save the plots (these will be saved at fairly large size to ensure good quality, and are saved as .png files in the app's "internal folder" (_bug note_: this is a minor bug and will be fixed asap; the intent is to put the images in the folder the excel file came from).

### Footnotes:
<a name="myfootnote1">1</a>: Note that 'rating' is the column with the star in Tracklete; this is supposed to give your athlete a way to rate their overall well being for the day.

## Requirements:
### GUI version:
None! It should work out of the box (which is why the file size is a bit big...). Currently there is only a windows version, sadly, but expect at least a working version for OSX shortly. 

### GUI-less version:
You'll need to have Python 3 installed. In addition, Tracklete Analyzer makes use of the following libraries, which may or may not have come pre-installed with the Python distribution you have installed:
 - numpy
 - pandas
 - xlrd
 - matplotlib
 
If you'd like to execute the GUI version as a Python script (saving you some space, as well as starting up slightly faster), you can find it in the project code. You'll also need to install the Kivy library, as well as the matplotlib extension from Kivy Garden. 

## FAQ
### Where do I download it?
For those of you unfamiliar with GitHub: download the most current version of the app by going to <a href=https://github.com/PaulHofma/tracklete-analysis/releases>Releases</a>. There you just click the .zip file for the version you'd like to download, probably named something like tracklete-analysis-gui-v#.#.#.zip.

### Why is the app so big? And what is that giant folder with complicated-looking stuff for?
Simply put: I've got to bundle it with not only Python, but also several not-so-small visual libraries. In addition, the library I'm using for the UI (kivy) tends to act up when trying to bundle into a 'singular' app (which is why the app is currently distributed as a folder instead of a neat single file. I hope to figure this out at some point, but I'm afraid that it will be for a future release.

### Why is there no Mac/OSX or Linux version?
Working on it! Working from a Windows pc, bundling for Windows is a lot easier, and so that was the first step I chose to take. Note that it should be fairly simple to execute the pure Python version (find it either in the GUI-less release or in the source code) as every Mac has Python 2.7 preinstalled! This means you'll have to use the 3to2 lib to get it to work for you, but it shouldn't be much more work. As for Linux: how come you're using Linux but don't know how to use pip or Python??? For this reason, Linux is currently the absolute bottom priority, but if any real desperate requests come in I might consider it.

### MATH: What's with all this 'Trend Order' business?
In case you're interested in the math used but not certain what is meant by 'order' in this case: I'm plotting polynomials of order x, meaning these are functions of the type y = a + bx + cx<sup>2</sup> + dx<sup>3</sup> .... The highest power of x in this case denotes the order; so a 'First order trend' is a trend with formula y = a + bx, a straight line. By comparison, the other 'standard' order plotted is second order, so y = a + bx + cx<sup>2</sup>. While lower order trends are good for getting a feeling for the general <i>direction</i> of a trend, a higher order trend is better for picking up on the more subtle <i>details</i>. For example, for an athlete who has been losing weight but is now stabilizing, a second order trend will generally be a much better predictor than a first order trend. Again, human fysiology is complicated and models are simple by necessity; however, trends of different order may reveal different details about the data, and therefore using some common sense and combining insights from different curves may therefore help give you a better idea of what the <i>true</i> trend is.

## Scheduled improvements for future versions:
 - Better statistics: I'd like to at least be able to give a margin of error on the trend lines. For this I'll likely have to include some additional packages for statistics (in the meantime likely forcing me to rewrite the whole bit of code that does the calculations for the trend lines), and I'd have to read up on the <i>actual</i> statistics as well... which sounds a lot like work, and so is likely to be put off for a little while. I'm only human folks.
   - Progress: 0% - not yet started
 - GUI improvment: There's a few more bells and whistles I'd like to add to the GUI - everything major is in there currently, but there are a couple of touches that I couldn't get to work in the initial release but that I'd like to get working at some point in the future.
   - Progress: 0% - not yet started
 - More options: Mostly, this is just adding more bells and whistles. Giving you an option for how many trend lines you'd like to include, giving you higher-order trendline options, using more sophistic fitters in general (i.e. adding a sinusoid for women's coaches in particular, since periods tend to have at least some recurring, not-insignificant impact on all bodystats), the possibilities are essentially only limited by anything you would like to be able to see. If you have any ideas, feel free to shoot me a message, or else feel free to add to my code yourself! If you do, I'd appreciate it if you would share it with me so I can add it to the repo here.
   - Progress: 
    - More/different order n trendlines: 0% - not yet started
    - More sophistic fitters: 0% - not yet started
 - Mac and Linux ports: Eventually I'd like to have at least a Mac port, which I see as something 'essential' to the project. However, with a standalone windows version out there I think the project is good to go for now, so this will probably take a little while as I let it rest for a bit.
  - Progress:
   - Mac: 0% - not yet started
   - Linux: 0% - not yet started (low priority)
