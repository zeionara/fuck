#!/bin/bash

# This script was used for debugging the problem of package_data in setup.py
# The solution was to put files inside package directory

rm -rf build
rm -rf dist
rm -rf *.egg-info
rm -rf /home/zeio/anaconda3/lib/python3.9/site-packages/fuck

# rm -rf /home/zeio/anaconda3/lib/python3.9/site-packages/f_ck-0.0.10-py3.9.egg/fuck

# python setup.py sdist
# pip install dist/f-ck-0.0.10.tar.gz
# tree /home/zeio/anaconda3/lib/python3.9/site-packages/fuck

# python setup.py install
# tree /home/zeio/anaconda3/lib/python3.9/site-packages/f_ck-0.0.10-py3.9.egg

# ls ~/anaconda3/assets
