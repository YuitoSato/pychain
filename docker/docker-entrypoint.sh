#!/bin/bash

rm -rf app/conf/config.py
touch app/conf/config.py
echo "NODE_NUMBER=$1" >> app/conf/config.py
echo "SQLALCHEMY_DATABASE_URI=\"sqlite:///sqlite/pychain_db_$1.sqlite3\"" >> app/conf/config.py

FLASK_APP=run.py flask db init
FLASK_APP=run.py flask db migrate
FLASK_APP=run.py flask db upgrade

sqlite3 sqlite/pychain_db_$1.sqlite3 < docker/genesis_transaction.sql
python -u entrypoint.py 500$1
