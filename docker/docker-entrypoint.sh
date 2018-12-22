#!/bin/bash

rm -rf app/conf/config.py
touch app/conf/config.py
echo "NODE_NUMBER=$1" > app/conf/config.py

python -u app.py 500$1
