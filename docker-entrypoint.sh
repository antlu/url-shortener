#!/bin/sh

python -m flask init-db
python -m flask run --host 0.0.0.0 --port 5000
