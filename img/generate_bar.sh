#!/bin/bash

for idx in {0..100}
do
    convert -size 102x16 xc:white -fill "#BCD2EE" -draw "rectangle 0,0 $idx,15" -stroke black -strokewidth 1 -fill none -draw "rectangle 0,0 101,15" -stroke none -fill black -pointsize 12 -font "Courier" -gravity center -draw "text 0,2 '$idx%'" bar_$idx.gif
done