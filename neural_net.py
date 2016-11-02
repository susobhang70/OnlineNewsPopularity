#!/usr/bin/python

import numpy as np
import csv
import sys
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

indexes = [7, 9, 12, 14, 16, 17, 18, 25, 26, 27, 36, 37, 38, 39, 40, 41, 43, 44, 45, 49]
field_names = []

def readfile():
	data = []
	labels = []
	shares = []
	with open('OnlineNewsPopularity.csv', 'rb') as csvfile:
		data_lines = csv.reader(csvfile, delimiter=',')
		for i in data_lines:
			# for j in indexes:
			for j in range(len(i)):
				if j is not 0:
					field_names.append(i[j])
			break
		for item in data_lines:
			temp = []
			for i in range(len(item)):
				if i is not 0:
			# for i in indexes:
					temp.append(float(item[i]))
			data.append(temp)
			shares.append(float(item[-1]))
	for i in shares:
		if i < 1400:
			labels.append(-1)
		else:
			labels.append(1)
	return data, labels, shares

def split_data(data, labels, randomize):
	# data = data[:2000]
	# labels = labels[:2000]
	if randomize is False:
		train_data   = data[0:int(len(data)*(0.7))]
		train_labels = labels[0:int(len(data)*(0.7))]
		test_data    = data[int(len(data)*(0.7)) + 1 : ]
		test_labels  = labels[int(len(data)*(0.7)) + 1 : ]
		return train_data, test_data, train_labels, test_labels

	else:
		return train_test_split(data, labels, test_size = 0.3)

def main():
	data, labels, shares =  readfile()
	a, b = 0, 0
	for p in range(10):
		train_data, test_data, train_labels, test_labels = split_data(data, labels, True)

		clf = MLPClassifier(hidden_layer_sizes = (10, 10, 10, 10, 100), activation = 'logistic')
		clf.fit(train_data, train_labels)
		t1 = clf.score(test_data, test_labels)
		t2 = clf.score(train_data, train_labels)
		a += t1
		b += t2
		print t1, t2, clf.n_layers_

	print a/10, b/10

if __name__ == '__main__':
	np.random.seed()
	main()