# Example: Matplotlib for 3D Graphing in wxPyhton
## Table of contents
* [Project Description](#Project-Description)
* [Requirements](#Requirements)
* [How to Use](#How-to-Use)
* [Images](#Images)
* [Future Work](#Future-Work)


## Project Description
This project is an example of drawing 'live' data in a 3D matplotlib widget in a wxPython frame. Rather than generating random data,
'node' objects have been created with 2 different movement options to demonstrate a callback and update. The nodes keep full record of all past location, and their full paths (or just the current location). User Input controls the type of path drawn (connected, unconnected, single dot)


## Requirements
Library requirements for locally run Python code are included in requirements.txt and can be 
installed using 'pip install -r requirements.txt'

* contourpy==1.0.7
* cycler==0.11.0
* fonttools==4.38.0
* kiwisolver==1.4.4
* matplotlib==3.6.3
* numpy==1.24.1
* packaging==23.0
* Pillow==9.4.0
* pyparsing==3.0.9
* python-dateutil==2.8.2
* six==1.16.0
* wxPython==4.2.0

## How to Use

The program can be run from main.py, either in an IDE or with 'python main.py'

Users can select a path display type in the drop down menu, and enter the number of nodes. 
'Run' starts the example with new nodes, while 'Stop' ends the walk model. 


## Images

<p align="center">

<img src="https://github.com/LC-Linkous/Example_wxPython-Matplotlib/blob/master/imgs/connected-example.PNG" width="250">

<img src="https://github.com/LC-Linkous/Example_wxPython-Matplotlib/blob/master/imgs/unconnected-example.PNG" width="250">

<img src="https://github.com/LC-Linkous/Example_wxPython-Matplotlib/blob/master/imgs/single-example.PNG" width="250">
</p>

## Future Work 
This may or may not be updated - it is meant as an example only, not as a fully functioning project. 

* Cosmetic:
    * using a scroll bar when the node summary is longer than the summary box

* Functionality:
    * Stop currently stops the nodes completely, this should be changed to act as a stop/resume button. Run always resets the model.


