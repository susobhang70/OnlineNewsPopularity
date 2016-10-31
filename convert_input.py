#!/usr/bin/python
import numpy as np
import csv

data = []
labels = []
rf = open("NewOnlineNewsPopularity.csv", 'wb')
wr = csv.writer(rf)
with open('OnlineNewsPopularity.csv', 'rb') as csvfile:
    data_lines = csv.reader(csvfile, delimiter=',')
    for i in data_lines:
        data.append(i[1:])
        break
    for item in data_lines:
        temp = item[1:]
        if float(item[-1]) < 1400:
        	temp[-1] = -1
        else:
        	temp[-1] = 1
        data.append(temp)
wr.writerows(data)