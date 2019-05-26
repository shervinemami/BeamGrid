#!/bin/bash

echo "In clickMouseGrid.sh $1"
if [ $1 -ge 1 -a $1 -lt 6 ]; then
    # Send whichever click event was given
    xdotool click "$1"
fi
if [ $1 -eq 6 ]; then
    # Send a left-buttton mousedown event
    xdotool mousedown 1
fi
if [ $1 -eq 7 ]; then
    # Send many mouseup events
    xdotool mouseup 1   # left
    xdotool mouseup 2   # middle
    xdotool mouseup 3   # right 
fi
if [ $1 -eq 8 ]; then
    # Send a middle-button mousedown event, to potentially scroll fast
    xdotool mousedown 2
fi
if [ $1 -eq 9 ]; then
    # Send a double-click
    xdotool click --repeat 2 --delay 200 1
fi
if [ $1 -eq 10 ]; then
    # Send a triple-click
    xdotool click --repeat 3 --delay 200 1
fi
