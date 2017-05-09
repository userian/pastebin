#!/bin/bash
virtualenv pastbin
source pastbin/bin/activate
pip install flask
export FLASK_APP=pastebin.py
flask run 