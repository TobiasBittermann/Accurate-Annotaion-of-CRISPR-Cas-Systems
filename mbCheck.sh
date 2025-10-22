#!/bin/bash

# Verzeichnis, das überprüft werden soll (Standard: aktuelles Verzeichnis)
DIR="${1:-.}"

# Grenze in MB
SIZE_LIMIT=100

echo "Suche nach Dateien größer als ${SIZE_LIMIT}MB in ${DIR} ..."
echo "---------------------------------------------"

# find Befehl: -type f (Dateien), -size +100M (größer als 100MB)
find "$DIR" -type f -size +"$SIZE_LIMIT"M -exec ls -lh {} \; | awk '{ print $9 ": " $5 }'

echo "---------------------------------------------"
echo "Fertig."

