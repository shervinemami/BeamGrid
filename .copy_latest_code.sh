#!/bin/bash
# Exit the script if any command gives an error.
set -o errexit
# Show a '+' symbol and show every single command just before it's executed.
set -o xtrace


M=/Core/SpeechRec/my_dragonfly_grammar/MacroSystem
cd MacroSystem
cp -a $M/_aenea.py .
cp -a $M/_all.py .
cp -a $M/keyboard.py .
cp -a $M/lettermap.py .
cp -a $M/mousebuttons.py .
cp -a $M/_mousegrid_symbols.py .
cp -a $M/mousegridutils.py .
cp -a $M/_mouse_start.py .
cp -a $M/programs.py .
cp -a $M/punctuationmap.py .
cp -a $M/_record_or_play.py .
cp -a $M/symbolmap.py .
cp -a $M/words.py .
cd ..

P=/Core/SpeechRec/aenea/server/linux_x11/plugins
cd plugins
cp -a $P/updateRecognition.py .
cp -a $P/standalone_grids.py .
cp -a $P/showHistory.py .
cp -a $P/invisibleWindow.py .
cp -a $P/clickMouseGrid.sh .
cp -a $P/clickMouseGrid.py .
cd ..

# Disable my customisations before it gets published
sed -i '/ENABLE_BLINKSTICK = True/c\ENABLE_BLINKSTICK = False' MacroSystem/_aenea.py 
