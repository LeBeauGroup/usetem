# USETEM

This is the useTEM framework.  The goal of this python package is to build a single use point for interacting with all control point and software.  


## USETEM Install

### Packages

comtypes, pyqt5, comtypes, yapsy, bibtexparser, numpy


### Python setup

Start->  Computer (right click) -> Properties -> Advanced System Settings -> Advanced Tab -> Environmental variables button

Click new (user variables for supervisor)

Variable Name: PYTHONPATH (all caps)
Variable Value: path to directory containing the usetem folder


### Configure servers


## To start

open an anaconda terminal and run:

	python -m useTEM.servers

Click TEM Scripting and TIA scripting (buttons should turn green)

back to the anaconda terminal and run:

	python -m useTEM.launch

