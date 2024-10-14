#!/bin/bash

set -x

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade pip
pip install --upgrade pip
pip install -r requirements.txt

pyinstaller --onefile acctop.py