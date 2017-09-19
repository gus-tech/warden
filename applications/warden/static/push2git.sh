#!/bin/bash

cd /home/www-data/web2py
git add .
git commit -m "$1"
git push -u origin master
