```
Made by:  
    Felix Poerner
    mail@felix-poerner.de
```

# Octoint
Qt Interface for Octoprint 3D Printer control
based on the great Octopi API and Octorest. \
A fun nonsense project I've been working on for a bit, where I try to learn as many new things about Qt as possible. \
Any feedback is greatly appreciated since I'm new to OpenGl and newish to Qt.

https://felix-poerner.de/octoint/ \

## Installation
Clone the Repo and install the following Packages:
- PySide2
- octorest
- PyOpenGL
- Cython
- qdarkstyle
- PyYaml
- numpy

Run this command (Cython needed) `python3 ./octoint/gcode/setup.py build_ext --inplace`
After that start the Tool and it will ask for an Ip Address and an API Key (found on the server under User Settings).
Click connect to connect to the octopi. If everything worked out, you will be asked to select a printer profile. Select the correct one and press confirm.
Currently you cannot close the window by pressing the x. You'll have to stop the python program itself. If anything went wrong during Setup just delete the config.yaml file and start again.
If everything worked, you should see a window like this (without the model):

![alt text](https://felix-poerner.de/wp-content/uploads/2020/06/Screenshot-from-2020-06-07-17-56-57-700x442.png)

## Usage
In the top left corner are the printer settings and information about the current state. \
To print a gcode file just double click on it in the list and press the print button. \
Next to that are additional buttons for pause/play, restart and aborting the print.
Below the file list are the upload, select gcode (equivalent to double click on item in list) and the delete button. \
Underneath those is a tab containing basic printhead movement.

And in the bottom left corner is the temperature graph with two textfields below to set the target temperature for the bed and tool. \
The main screen contains an OpenGl widget with basic pan, zoom and rotation functionality and above are a checkbox to preview the selected print and a slider to see parts of the print.
During printing disable the preview checkbox to see the current progress of the print.



## Modules
#### octoint.viewers
Visualization for the selected print.\
Currently only has an OpenGL Viewer but there might be a webcam viewer in the future.
 
#### octoint.sensors
Display Sensor Information
 
#### octoint.printsettings
Display all Print Information and Printcontrolls about available files and selected/current print  
 
#### octoint.setup
Set up config file containing API Key, Ip Address of the octopi server and the selected Print Profile
 
#### octoint.move
Control Printermovement

#### octoint.settings
_will be added in the future_
 
#### octoint.gcode
Parsing gcode files (needs to be compiled)
 
#### octoint.main_utils
Contains logging, time measurement decorator and QThread Worker
