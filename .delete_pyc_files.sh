#!/bin/bash

find . -wholename "*pyc" -exec rm -fv \{\} \;
