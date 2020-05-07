#! /bin/bash
workdir=$1
cd $workdir
source "venv/bin/activate"
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt
