```
Made by:  
    Felix Poerner
    mail@felix-poerner.de
```

# Octoint
Qt Interface for Octoprint 3D Printer control
based on the great Octopi API and Octorest from  dougbrion. \
https://felix-poerner.de/octoprint-interface/

## Installation
Clone the Repo and install the following Packages:
- PySide2
- octorest
- PyOpenGL
- Cython
- qdarkstyle
- PyYaml
- numpy

Then run this command (Cython needed) `python3 ./octoint/gcode/setup.py build_ext --inplace`
After that start the Tool and it will ask for an Ip Address and an API Key (found on the server under User Settings).
Then run run.py and make sure the octopi server is running.

## Modules
#### octoint.viewers
Responsible for all visualization type things for the interface.\
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
_TODO_
 
#### octoint.gcode
Handles everything to do with interpreting the gcode files (needs to be compiled)
 
#### octoint.main_utils
Contains logging, time measurement helpers and QThread Worker
