#! /usr/bin/env python

with open('results.2.csv') as f:
    lines = f.readlines()

for line in lines:
    parts = line.split('\t')
    new_line = '("' + parts[0] + '",' + parts[1] + ',"' + parts[2] + '",' + parts[3] + ',' + '"STD",' + parts[4].rstrip() + '),\n'
    with open('done.2.sql', 'a') as f:
        f.write(new_line)