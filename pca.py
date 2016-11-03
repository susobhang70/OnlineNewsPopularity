#!/usr/bin/python

import numpy as np
import csv

from sklearn.decomposition import PCA
from sklearn.model_selection import KFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LinearRegression

field_names = []

def readfile():
	data = []
	labels = []
	with open('OnlineNewsPopularity.csv', 'rb') as csvfile:
		data_lines = csv.reader(csvfile, delimiter=',')
		for i in data_lines:
			break
		for item in data_lines:
			data.append(item[1:-1])
			if(float(item[-1]) < 1400):
				labels.append(-1)
			else:
				labels.append(1)
	data = np.array(data).astype(float)
	labels = np.array(labels)
	return data, labels

def main():
	data, labels = readfile()
	k_fold = KFold(n_splits=10, shuffle = True)
	for k, (train, test) in enumerate(k_fold.split(data, labels)):
		pca = PCA(n_components = 20)
		train_data = pca.fit_transform(data[train])
		test_data = pca.transform(data[test])
		# clf = GaussianNB()
		clf = MLPClassifier(hidden_layer_sizes = (10, 10, 10, 10, 100))
		clf.fit(train_data, labels[train])
		print clf.score(test_data, labels[test])


if __name__ == '__main__':
	main()