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
    xdotool keyup "ctrl"
    xdotool keyup "shift"
    xdotool keyup "alt"
    xdotool keyup "meta"
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
if [ $1 -eq 11 ]; then
    # Hold down the control key while clicking
    xdotool keydown "ctrl"
    xdotool click "1"
    xdotool keyup "ctrl"
fi
if [ $1 -eq 12 ]; then
    # Hold down the shift key while clicking
    xdotool keydown "shift"
    xdotool click "1"
    xdotool keyup "shift"
fi
if [ $1 -eq 13 ]; then
    # Hold down the alt key while clicking
    xdotool keydown "meta"
    xdotool click "1"
    xdotool keyup "meta"
fi
if [ $1 -eq 14 ]; then
    # Hold down the control key while dragging
    xdotool keydown "ctrl"
    xdotool mousedown 1
fi
if [ $1 -eq 15 ]; then
    # Hold down the shift key while dragging
    xdotool keydown "shift"
    xdotool mousedown 1
fi
if [ $1 -eq 16 ]; then
    # Hold down the alt key while dragging
    xdotool keydown "meta"
    xdotool mousedown 1
fi
if [ $1 -eq 17 ]; then
    # Hold down the control key while right clicking
    xdotool keydown "ctrl"
    xdotool click "3"
    xdotool keyup "ctrl"
fi
if [ $1 -eq 18 ]; then
    # Hold down the shift key while right clicking
    xdotool keydown "shift"
    xdotool click "3"
    xdotool keyup "shift"
fi
if [ $1 -eq 19 ]; then
    # Hold down the alt key while right clicking
    xdotool keydown "meta"
    xdotool click "3"
    xdotool keyup "meta"
fi
