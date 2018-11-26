# Trackelete Analyzer V1.0.1
A pretty small piece of software, which does one thing very well: take exported bodystat data from <a href="http://tracklete.io">Tracklete</a>, and transform these into useful graphs for humans (or, rather, coaches).

## Example Results
![Bodystat Analysis Example](Tracklete_Trends_Paul%20Hofma.png)

## How it works
You export your data from Tracklete, which gives you either a batch excel sheet (containing data for all your athletes) or a sheet with the bodystats for a single athlete. You then simply proceed to drag-and-drop this excel file onto the Python script (by default named Tracklete_Analyzer.py) and you'll get a terminal shell showing you the progress as it's happening. As it goes, it will create the graphs you specified (more on that below) for each athlete (or just for the one athlete) including the relevant trend lines, and tell you when it's done.

There are currently a few options for you as coach to fiddle with; these can be set by opening the program with your text editor of choice, and editing a few very simple lines below where it says OPTIONAL PARAMS. I'd recommend you not to touch anything that is outside of this part of the code (that is, anything including and below SETUP), as this may cause the program to no longer work if you don't know what you're doing. If you're familiar with Python there shouldn't be anything too unfamiliar in there, so feel free to have at it; any and all suggestions for improvement are of course appreciated!

### Options Available
These are all also detailed in the program itself right where you have to change them, and should speak for themselves, mostly. For reference's sake, however, they're also listed here:
 - additional_days : this lets you set a number of additional days for which to plot the trends. Useful to get an indication of where the trend is heading.
 - N_days_used : this lets you set how many days (starting at the most recent and counting backwards) of data you want to use.
 - plots : these are your on/off switches for which of the 4 'types' of bodystats (weight, heartrate, rating<sup>[1](#myfootnote1)</sup>, sleep) you want to plot.
 - weight_lines : whether to include lines to indicate a certain weight requirement; built in such a way that you only need to set this to true and then enter the average weight for your category (presumably 70 for men and 57 for women).

#### Footnotes:
<a name="myfootnote1">1</a>: Note that 'rating' is the column with the star in Tracklete; this is supposed to give your athlete a way to rate their overall well being for the day.

## Requirements
Currently the program requires you to have a version of python installed; I intend to turn this into an independent app at some point, but haven't yet gotten around to it yet. In addition, Tracklete Analyzer makes use of the following libraries:
 - numpy
 - pandas
 - xlrd
 - matplotlib (pyplot and dates)
 - sys
 
 ## Scheduled improvements for future versions:
 - "Idiot Proofing": I'm planning to turn this into an independent executable with a proper GUI, so it's still easily useable by folks who don't feel comfortable tinkering the program manually. Initially I'll be doing this only for windows (providing you with a .exe) - though I expect to have Mac and Linux versions ready shortly after (which should be much easier as Mac comes with Python preinstalled and if you don't have Python installed and you're running Linux what are you even doing tbh).
 - Better statistics: I'd like to at least be abel to give a margin of error on the trend lines. For this I'll likely have to include some additional packages for statistics (in the meantime likely forcing me to rewrite the whole bit of code that does the calculations for the trend lines), and I'd have to read up on the <i>actual</i> statistics as well... which sounds a lot like work, and so is likely to be put off for a little while. I'm only human folks.
 - More options: Mostly, this is just adding more bells and whistles. Giving you an option for how many trend lines you'd like to include, giving you higher-order trendline options, using more sophistic fitters in general (i.e. adding a sinusoid for women's coaches in particular, since periods tend to have at least some recurring, not-insignificant impact on all bodystats), the possibilities area essentially only limited by anything you would like to be able to see. If you have any ideas, feel free to shoot me a message (or else feel free to add to my code yourself! If you do, I'd appreciated if you did share it with me so I can add it to the repo here).


 
