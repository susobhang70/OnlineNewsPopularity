#!/usr/bin/python
# Script to implement SVM using scikit

import numpy as np
import csv
from sklearn import svm
from sklearn.model_selection import train_test_split

indexes = [7, 9, 12, 14, 16, 17, 18, 25, 26, 27, 36, 37, 38, 39, 40, 41, 43, 44, 45, 49]
field_names = 0

def readfile():
    data = []
    labels = []
    shares = []
    with open('OnlineNewsPopularity.csv', 'rb') as csvfile:
        data_lines = csv.reader(csvfile, delimiter=',')
        # for item in data_lines:
        for i in data_lines:
            field_names = i[:]
            break
        for item in data_lines:
            temp = []
            for i in indexes:
                temp.append(float(item[i]))
            data.append(np.array(temp))
            shares.append(float(item[-1]))
    data = np.array(data)
    shares = np.array(shares)
    for i in shares:
        if i < 1400:
            labels.append(-1)
        else:
            labels.append(1)
    labels = np.array(labels)
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
        return train_test_split(data, labels, test_size = 0.3, random_state = 42)

def main():
    data, labels, shares = readfile()
    # train_data, test_data, train_labels, test_labels = split_data(data, labels, False)

    # print train_data.shape, test_data.shape, train_labels.shape, test_labels.shape

    # SVM1 = svm.SVC(kernel="linear")
    # SVM1.fit(train_data, train_labels)
    # print 'SVM with linear kernel, no cv randomization =', SVM1.score(test_data, test_labels)*100,'%'

    # SVM1 = svm.SVC(kernel="rbf")
    # SVM1.fit(train_data, train_labels)
    # print 'SVM with rbf kernel, no cv randomization =', SVM1.score(test_data, test_labels)*100,'%'

    # SVM1 = svm.SVC(kernel="poly")
    # SVM1.fit(train_data, train_labels)
    # print 'SVM with poly kernel, no cv randomization =', SVM1.score(test_data, test_labels)*100,'%'

    for i in range(10):
        train_data, test_data, train_labels, test_labels = split_data(data, labels, True)

        SVM1 = svm.SVC(kernel="linear")
        SVM1.fit(train_data, train_labels)
        print '#', i, 'SVM with linear kernel, with cv randomization =', SVM1.score(test_data, test_labels)*100,'%'

        SVM1 = svm.SVC(kernel="rbf")
        SVM1.fit(train_data, train_labels)
        print '#', i, 'SVM with rbf kernel, with cv randomization =', SVM1.score(test_data, test_labels)*100,'%'

        # SVM1 = svm.SVC(kernel="poly")
        # SVM1.fit(train_data, train_labels)
        # print '#', i, 'SVM with poly kernel, with cv randomization =', SVM1.score(test_data, test_labels)*100,'%'

if __name__ == '__main__':
    np.random.seed()
    main()