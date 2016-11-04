#!/usr/bin/python

import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

EPOCHS = 10

def NaiveBayesPipeline(traindata, trainlabels):
	nvpipeline = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()),])
	nvpipeline = nvpipeline.fit(traindata, trainlabels)
	return nvpipeline

def RandomForestPipeline(traindata, trainlabels):
	rfpipeline = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), \
		('clf', RandomForestClassifier(n_estimators = NUM_TREES, n_jobs = 8)),])
	rfpipeline = rfpipeline.fit(traindata, trainlabels)
	return rfpipeline

def NeuralNetPipeline(traindata, trainlabels):
	nnpipeline = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MLPClassifier(hidden_layer_sizes = (10, 10, 10, 10, 100))),])
	nnpipeline = nnpipeline.fit(traindata, trainlabels)
	return nnpipeline

def SVMPipeline(traindata, trainlabels):
	svmpipeline = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SVC(kernel='rbf')),])
	svmpipeline = svmpipeline.fit(traindata, trainlabels)
	return svmpipeline

def predict(pipeline, testdata, testlabels):
	predicted = pipeline.predict(testdata)
	print np.mean(predicted == testlabels)

def remove_missing(alist):
	alist[39371:] = []
	alist[34378:35001] = []
	alist[29007:30001] = []
	alist[24060:25001] = []
	alist[19564:20001] = []
	alist[14816:15001] = []
	return alist

def readfiles():
	fp = open('./fullarticles','r')
	data_lines = fp.readlines()
	data = []
	temp = ""
	# j = 0
	for i in data_lines:
		if "----------------------------------------------------" in i:
			data.append(temp)
			temp = ""
		else:
			temp += i
	return data

def readlabels():
	labels = []
	with open('./../OnlineNewsPopularity.csv', 'rb') as csvfile:
		data_lines = csv.reader(csvfile, delimiter=',')
		for i in data_lines:
			break
		for item in data_lines:
			# labels.append(float(item[-1]))
			if(float(item[-1]) < 1400):
				labels.append(-1)
			else:
				labels.append(1)
	return np.array(remove_missing(labels))

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
	labels = readlabels()
	data = np.array(readfiles())
	print CountVectorizer().fit_transform(data).shape
	sys.exit(0)
	# for i in range(EPOCHS):
	# 	train_data, test_data, train_labels, test_labels = split_data(data, labels, True)
	# 	nvpipeline = NaiveBayesPipeline(train_data, train_labels)
	# 	predict(nvpipeline, test_data, test_labels)
	k_fold = KFold(n_splits=10, shuffle = True)
	for k, (train, test) in enumerate(k_fold.split(data, labels)):
		# print train
		# print labels[train]
		svmpipeline = SVMPipeline(data[train], labels[train])
		predict(svmpipeline, data[test], labels[test])

if __name__ == '__main__':
	main()