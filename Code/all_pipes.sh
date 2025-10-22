#!/bin/bash

rm -rf ~/.local/share/Trash/*
echo "Trash emptied."

./pipeline_CasPedia.py
./pipeline_JSON.py
./pipeline_Marcus.py
./pipeline_NCBI.py
./pipeline_uniprot.py

python3 check_pipe.py