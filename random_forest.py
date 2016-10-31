#!/usr/bin/python

import numpy as np
import csv
import sys
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from multiprocessing.dummy import Pool as ThreadPool 

SAMPLE_SIZE = 1500
FEATURE_SIZE = 5
MIN_NODE_SIZE = 50
NUM_TREES = 6

indexes = [7, 9, 12, 14, 16, 17, 18, 25, 26, 27, 36, 37, 38, 39, 40, 41, 43, 44, 45, 49]
field_names = []

def binary_split(index, value, data, labels):
	left = []
	leftlabels = []
	right = []
	rightlabels = []
	for i in range(len(data)):
		if data[i][index] >= value:
			left.append(data[i])
			leftlabels.append(labels[i])
		else:
			right.append(data[i])
			rightlabels.append(labels[i])
	# print len(rightlabels), len(leftlabels)
	return left, right, leftlabels, rightlabels

class Node():
	'''Node of a random forest'''
	def __init__(self, dataset, labels, depth = 0):
		self.data = dataset[:]
		self.datalen = len(self.data)
		self.labels = labels[:]
		self.candidate_indexes = 0
		self.feature_index = 0
		self.feature_value = 0
		self.left = None
		self.right = None
		self.depth = depth
		if self.datalen <= MIN_NODE_SIZE:
			self.__leaf = True
			self.C1, self.C2 = self.class_frequency()
		else:
			self.__leaf = False

	def isLeaf(self):
		return self.__leaf

	def clearData(self):
		self.data = []
		self.labels = []
		self.candidate_indexes = []
		self.datalen = 0

	def class_frequency(self):
		count2 = 0
		for i in self.labels:
			if i is 1:
				count2 += 1
		return (self.datalen - count2), count2

	def gini_score(self, labels):
		count2 = 0
		total = float(len(labels))
		for i in labels:
			if i is 1:
				count2 += 1
		count1 = float(total - count2)/total
		count2 = float(count2)/total
		return (1 - (count1**2 + count2**2))

	def __select_features(self):
		self.candidate_indexes = resample(list(range(20)), replace = False, n_samples = FEATURE_SIZE)
		# print self.candidate_indexes

	def populateChild(self):

		if self.__leaf == True:
			return
		
		# selecting m features out of p
		self.__select_features()

		# max storing variables
		max_score, max_val, max_j, split_left, split_right, split_left_labels, split_right_labels = 0, 0, 0, 0, 0, 0, 0

		for i in self.data:
			for j in self.candidate_indexes:
				# split data
				leftdata, rightdata, leftlabels, rightlabels = binary_split(j, i[j], self.data, self.labels)

				# calculate gini scores
				IDP = self.gini_score(self.labels)
				try:
					IDL = self.gini_score(leftlabels)
					IDR = self.gini_score(rightlabels)
				except:
					continue

				# calculate information gain
				IG  = IDP - (float(len(leftdata))/self.datalen)*(IDL) - (float(len(rightdata))/self.datalen)*(IDR)

				# update max
				if IG > max_score:
					max_score = IG
					max_val = i[j]
					max_j = j
					split_left, split_right = leftdata[:], rightdata[:]
					split_left_labels, split_right_labels = leftlabels[:], rightlabels[:]

		# selecting max
		self.feature_index = max_j
		self.feature_value = max_val

		# hack
		try:
			a,b,c,d = len(split_left), len(split_left_labels), len(split_right), len(split_right_labels)
		except:
			self.__leaf = True
			self.C1, self.C2 = self.class_frequency()
			return

		# print self.depth, max_j, max_val, len(split_left), len(split_left_labels), len(split_right), len(split_right_labels)

		# making child nodes
		self.left = Node(split_left, split_left_labels, self.depth + 1)
		self.right = Node(split_right, split_right_labels, self.depth + 1)

		# clear data
		self.clearData()

		# populate child nodes
		self.left.populateChild()
		self.right.populateChild()

class Tree():
	'''Random decision tree'''
	# def __init__(self, dataset, labels):
	def __init__(self, args):
		dataset = args[0]
		labels = args[1]
		self.root = Node(dataset, labels)
		self.root.populateChild()

	def classify(self, data):
		current = self.root
		while not current.isLeaf():
			if data[current.feature_index] >= current.feature_value:
				current = current.right
			else:
				current = current.left
		if current.C1 >= current.C2:
			return -1
		else:
			return 1

	# def print(self, dataset):

def readfile():
	data = []
	labels = []
	shares = []
	with open('OnlineNewsPopularity.csv', 'rb') as csvfile:
		data_lines = csv.reader(csvfile, delimiter=',')
		for i in data_lines:
			for j in indexes:
				field_names.append(i[j])
			break
		for item in data_lines:
			temp = []
			for i in indexes:
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

def bootstrap_data(data, labels):
	return resample(data, labels, n_samples = SAMPLE_SIZE)

def print_something(args):
	print "Hello"

def main():
	data, labels, shares =  readfile()
	train_data, test_data, train_labels, test_labels = split_data(data, labels, True)
	list_of_trees = []

	for i in range(NUM_TREES):
		sampled_data, sampled_labels = bootstrap_data(train_data, train_labels)
		tree = Tree([sampled_data, sampled_labels])
		list_of_trees.append(tree)

	# Make the Pool of workers
	# pool = ThreadPool(6) 
	# s1, l1 = bootstrap_data(train_data, train_labels)
	# s2, l2 = bootstrap_data(train_data, train_labels)
	# s3, l3 = bootstrap_data(train_data, train_labels)
	# s4, l4 = bootstrap_data(train_data, train_labels)
	# s5, l5 = bootstrap_data(train_data, train_labels)
	# s6, l6 = bootstrap_data(train_data, train_labels)

	# args = [[s1, l1], [s2, l2], [s3, l3], [s4, l4], [s5, l5], [s6, l6]]

	# list_of_trees = pool.map(Tree, args)
	# pool.close() 
	# pool.join()

	count = 0
	for i in range(10):
		count1 = 0
		count2 = 0
		for j in range(NUM_TREES):
			if list_of_trees[j].classify(test_data[i]) == 1:
				count1 += 1
			else:
				count2 += 1
		if (count1 > count2 and test_labels[i] == -1) or (count2 > count1 and test_labels[i] == 1):
			count += 1
	print count

if __name__ == '__main__':
	np.random.seed()
	main()