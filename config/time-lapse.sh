#!/bin/bash

#zeitstempel fuer dateiname generieren
timestamp=$(date +%Y-%m-%d_%H-%M)
echo $timestamp

#dateiname zuweisen
filename=/usr/local/media/images/$timestamp.jpg

#Foto erstellen
echo $filename

fswebcam --no-banner -r 640x480 -d /dev/video0 -i 0 -F 15 -D 4 -S 40 --jpeg 95 $filename