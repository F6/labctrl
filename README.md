# labctrl

A unified lab equipment controlling framework and experiment monitoring front end.

This software is available directly from github https://github.com/F6/labctrl as git repo or zip file. 
If you encounter any problem, feel free to contact me for help.

This software starts as an effort to provide consistent, well-documented programming interfaces for various instruments in our ultrafast laser lab here at Peking University, to accelerate the development of new instruments and methods, because the old LabView APIs and programs are suprisingly hard to read and modify.

Python, C++ and JavaScript are chosen as the primary language used for this project, but I think adequate support for adapting other language modules are supported because nearly everything is passed around as JSON and YAML, thus it should be relatively easy to interface with existing code including our old APIs in LabView, in case you still need them.

3 levels of abstraction is provided, namely "device", "method" and "app".

A device is just a lab equipment that accomplishes some simple task, like moving a motor, taking a photo, measuring voltages, etc. The device hides complicated drivers and diffrences between instrument brands under the carpet.

A method is a simple procedure that is used everywhere, for example if you'd like to take a microscopic photo of the sample between Raman scans with your home made confocal microscope, you may want to first turn off laser shutter to avoid burning camera, then turn on camera shutter, take the picture with camera, and put everything back to continue Raman scan. This procedure requires the use of multiple devices, but not suitable to be built as a single app.

An app is an integrated front end for experiment setups and monitoring, i.e. the GUI for the software. Different experiments
require different devices, methods and GUI elements, so a seperate app is made for each type of experiment. Devices, methods
and GUI elements are reusable in different apps, so developing apps are blazingly fast for most experiments.

## To add a new device

Most of the equipments are connected to different computers in our lab, so devices are in general distributed. Web API is chosen because we want it to be simple and reliable.

To add a new device, first, implement the RESTful API for the new device in "servers", also provide an emulator if possible (the emulator helps you to debug higher layer programs without actually having to be connected to the lab equipment).

By "RESRful" we mean the device tells the user what it can do when accessed, this makes it simpler for users to use it without complicated documentation.

Assign a new port to your API and add it to the table in servers/README.md (to avoid conflicting with existing devices.)

Add a json config file of the new device in "configs". The config file must include the API host and port for the new device， because servers are isolated part of the software and probably runs on other computers, the program have no way to know which port and host to access if not specified in the configs (unless we include UDP broadcasting in our software, but this is not as reliable as directly pin down the addresses).

Add remote API caller classes in "components" to provide local API.

Add the corresponding factory class in "components" to provide UI widgets and other functions of the device. Factory for Bokeh UI widgets are prefered because it is web-based.

## To add a new method

First, determine the components needed for the method. Specify them at the beginning of your method program.

Assign a new method name and short name in "configs/methods", put method specific settings there

Implement the method unit operation and thread task in "methods"

## To add a new app

Apps are put in the apps folder. You can copy and paste an existing app to start quickly.

The app includes several basic components, mainly one front end template, some static theme files (bootstrap
and feather icon are used), and a main.py

Basically all logic is in main.py because most experiments are not very complicated. In case your experiment
is extremely complicated, consider split your experiment into reusable parts and add them as methods.


Copyright 2022, x \[at\] zzi.io