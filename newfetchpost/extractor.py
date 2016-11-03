#!/home/susobhan/.virtualenvs/goose/bin/python

import csv
import sys
from goose import Goose

def readfile():
	data = []
	with open('./../OnlineNewsPopularity.csv', 'rb') as csvfile:
		data_lines = csv.reader(csvfile, delimiter=',')
		for i in data_lines:
			break
		for i in data_lines:
			data.append(i[0])
	return data

def main():
	data = readfile()
	g = Goose()
	target = open('articles', 'w')
	for i in range(len(data)):
		article = g.extract(url=data[i])
		temp =  article.cleaned_text
		target.write(temp.encode("ascii", "ignore"))
		target.write('\n--------------------------------------------------------------\n')
		if (i+1) % 400 == 0:
			print (i+1), '%'
	target.close()

if __name__ == '__main__':
	main()