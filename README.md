# Trackelete Analyzer V1.0.1
A pretty small piece of software, which does one thing very well: take exported bodystat data from <a href="http://tracklete.io">Tracklete</a>, and transform these into useful graphs for humans (or, rather, coaches).

## Example Results
![Bodystat Analysis Example](Tracklete_Trends_Paul%20Hofma.png)

## How it works
You export your data from Tracklete, which gives you either a batch excel sheet (containing data for all your athletes) or a sheet with the bodystats for a single athlete. You then simply proceed to drag-and-drop this excel file onto the python script (by default named Tracklete_Analyzer.py) and you'll get a terminal shell showing you the progress as it's happening. As it goes, it will create the graphs you specified (more on that below) for each athlete (or just for the one athlete), and tell you when it's done.

## Requirements
Currently the program requires you to have a version of python installed; I intend to turn this into an independent app at some point, but haven't yet gotten around to it yet. In addition, Tracklete Analyzer makes use of the following libraries:
 - numpy
 - pandas
 - xlrd
 - matplotlib (pyplot and dates)
 - sys


 
