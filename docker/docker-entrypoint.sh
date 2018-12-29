#!/bin/bash

rm -rf app/conf/config.py
touch app/conf/config.py
echo "NODE_NUMBER=$1" > app/conf/config.py

python -m app.infra.sqlite.table
sqlite3 sqlite/pychain_db_$1.sqlite3 < docker/genesis_transaction.sql

python -u app.py 500$1
