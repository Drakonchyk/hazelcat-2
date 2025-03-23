#!/usr/bin/env bash

python writer.py &
sleep 1
python reader1.py &
python reader2.py &
wait
