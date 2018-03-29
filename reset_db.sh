#!/bin/sh

# for ease of development when changing models

rm db.sqlite3
rm -r testresults/migrations
rm -r provisioning/migrations

./manage.py makemigrations provisioning
./manage.py makemigrations testresults
./manage.py migrate
