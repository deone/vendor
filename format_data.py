#! /usr/bin/env python

with open('results.csv') as f:
    lines = f.readlines()

for line in lines:
    parts = line.split(',')
    new_line = '(' + parts[0] + ',' + parts[1] + ',' + parts[2] + ',' + parts[3] + ',' + parts[4] + ',' + parts[5] + ',' + parts[6].rstrip() + '),'
    with open('done.sql', 'a') as f:
        f.write(new_line)