#! /bin/bash
workdir=$1
cd $workdir
source "venv/bin/activate"
python main.py
