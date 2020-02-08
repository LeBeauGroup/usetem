# USETEM

This is the useTEM framework.  The goal of this python package is to build a single use point for interacting with all control point and software.  


## USETEM Install

### Packages

pyqt5, comtypes, yapsy, bibtexparser, numpy


### Python setup

run `python setup.py install` from the distribution folder

### Configure servers


## To start

open a python terminal and run the background servers (download the source [here](https://github.com/subangstrom/usetemServers):

	python -m usetemServers.start

Click TEM Scripting and TIA scripting (buttons should turn green)

back to the python terminal and run:

	python -m ustem.start

