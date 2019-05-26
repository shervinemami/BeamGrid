# BeamGrid
By Shervin Emami (http://shervinemami.info), 2019

BeamGrid lets you control your computer mouse by using speech recognition or just a keyboard on Linux. It contains several grid modes for controlling the mouse in different ways.
It's based on the "DouglasGrid" and "Rainbow" mouse grid modes of Caster on Windowd, but instead of just limiting the possibe options to numbers and colors, it uses numbers, alphabet, nnon-alphabet keyboard symbols, and non-keyboard unicode symbols, so that there are a large number of possible symbols that can be displayed with just 1 or 2 symbols, therefore allowing fine grained selection with just a few utterances. It also supports a keyboard-only mode, as a much faster alternative to MouseKeys that many Linux systems come with. But keyboard-only mode doesn't have the extra unicode symbols and therefore is not as fine-grained as the unicode mode.

* "Beam" mode is generally the fastest way to left-click anywhere on the screen using your voice. It moves to a rough position then performs a left mouse click.
* "Glide" lets you quickly move left or right with high accuracy and range, such as to select some text characters using "drag" & "release".
* "Sink" lets you quickly move up or down with high accuracy and range, such as to select a row of characters.
* "Ladder" shows the X grid followed by the Y grid, letting you move the mouse to a 2D position with high accuracy.
* Other modes include "Grid" mode that moves the mouse in a 2D grid just like Beam mode, but doesn't click the mouse, allowing you to say "Grid 5 6 psychic", etc.

2D Beam mode:
![Screenshot of the 2D "Beam" mouse grid](https://raw.githubusercontent.com/shervinemami/BeamGrid/master/Screenshots/2D_grid.png "Screenshot of the 2D Beam mouse grid")

1D "Glide" mode (X-axis):
![Screenshot of the 1D "Glide" X-axis mouse grid](https://raw.githubusercontent.com/shervinemami/BeamGrid/master/Screenshots/X_grid.png "Screenshot of the 1D Glide X-axis mouse grid")

1D "Sink" mode (Y-axis):
![Screenshot of the 1D "Sink" Y-axis mouse grid](https://raw.githubusercontent.com/shervinemami/BeamGrid/master/Screenshots/Y_grid.png "Screenshot of the 1D Sink Y-axis mouse grid")

Configuring BeamGrid is tedious, but once you've set it up, you can control the mouse in Linux by voice using Aenea + Dragonfly + Dragon Naturally Speaking.
It should be possible to port this to other voice coding systems such as Caster on Windows or Talon on Mac, but they haven't been ported so far.

Video demo of BeamGrid:
[![Video demo](https://img.youtube.com/vi/xbdwNQfrlKI/0.jpg "Video demo" (https://youtu.be/xbdwNQfrlKI)

