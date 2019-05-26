#!/bin/bash
# A voice controlled mouse that supports Linux and fine-grained movements. Caster's Rainbow grid is very cool, it lets
# you move the mouse by voice and is quite fast. But it's not fine-grained enough to select text, and it only runs on
# Windows. I use Aenea to remotely control Linux and therefore don't have any mouse grid modes available at all! So
# I've been implementing my own voice based mouse grid system that works on Linux and is fine-grained enough to select
# individual characters and yet is still fast to use. I don't know how portable it will be outside of aenea & Linux or
# even to other Linux machines since it relies very heavily on the font configuration of the computer. But I'm hoping
# it can eventually support Aenea on Linux, Caster on Windows, and probably Talon on Mac.
# By Shervin Emami, 2019. http://shervinemami.info/


# Make sure the grid isn't already running in the background
pkill -f -9 standalone_grids.py
pkill -f -9 invisibleWindow.py


# Default to args "x -s", but allow it to be overriden, such as:
# "x -v -u -c 30"
AXIS='x'
SERVICE_MODE='-s'
KEYBOARD_MODE='-u'
if [[ $# -ge 1 ]]; then
    AXIS=$1
    SERVICE_MODE='-v'
fi
if [[ $# -ge 2 ]]; then
    SERVICE_MODE=$2
fi
if [[ $# -ge 3 ]]; then
    KEYBOARD_MODE=$3
fi
if [[ $# -ge 4 ]]; then
    CELL_SIZE="$4 $5"
fi

if [[ $AXIS != "cancel" ]]; then

    # Start the grid, running in service mode in the background
    #python plugins/showMouseGrid.py $ARGS

    # Note that we create 2 windows, but it doesn't matter which order they get executed in.
    # Keypresses will go to the InvisibleWindow app, and mouseclicks will go to the MouseGrid app.

    # Create a background process to start running our invisible window and return here straight away
    python plugins/invisibleWindow.py $SERVICE_MODE &

    # Create a background process to start running our grid script and return here straight away
    python plugins/standalone_grids.py -g $AXIS $SERVICE_MODE $KEYBOARD_MODE $CELL_SIZE &

fi
