#!/usr/bin/python
# Script to extract relevant features from the Mashables corpus.
# Returns features in descending order of Fischer Criterion.

import operator
from collections import Counter

type_of_data = [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,\
                0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,\
                0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,\
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

def gaussian(mean, variance, value):
    return ((1/math.sqrt(2 * math.pi * variance)) * (math.exp((-((value - mean) * (value - mean))) / (2 * variance))))

def main():
    """
    Calculate the labels for each feature, and then the mean and 's' values, 
    then the fischer score.
    """

    # Opening the file, and extracting each line
    fp = open('./OnlineNewsPopularity.csv','r')
    data = fp.readlines()
    data_lines = data[0:int(len(data)*(0.7))]
    test_lines = data[int(len(data)*(0.7)) + 1 : ]

    # The first line consists of all features, we extract number and names.
    feature_names = data_lines[0].split(", ")
    feature_count = len(feature_names)
    instance_count = len(data_lines)
    discrete_distribution = [[]]

    # Initializing some values
    count_label1 = 0
    count_label2 = 0
    label = [0 for x in range(instance_count)]
    sum1 = [0.00 for x in range(feature_count)]
    sum2 = [0.00 for x in range(feature_count)]
    mean1 = [0.00 for x in range(feature_count)]
    mean2 = [0.00 for x in range(feature_count)]
    s1_squared = [0.00 for x in range(feature_count)]
    s2_squared = [0.00 for x in range(feature_count)]
    F = [0.00 for x in range(feature_count)]

    # Classifying each instance using the labels
    for i in range(instance_count):
        if i is not 0:
            items = data_lines[i].split(",")
            # print items[feature_count-1]
            if int(items[feature_count-1]) > 1400:
                label[i] = 1
                count_label1 += 1
            else:
                label[i] = 2
                count_label2 += 1

    # Finding sums and means of features
    for j in range(feature_count):
        if j is not 0:
            temp = []
            temp1 = []
            temp2 = []
            for i in range(instance_count):
                if i is not 0:
                    items = data_lines[i].split(",")
                    val = float(items[j].strip())
                    if label[i] == 1:
                        sum1[j] += val
                    else:
                        sum2[j] += val
                    if type_of_data[j] == 0:
                        if label[i] == 1:
                            temp1.append(val)
                        else:
                            temp2.append(val)
            if type_of_data[j] == 0:
                counter1 = Counter(temp1)
                counter2 = Counter(temp2)
                tempdict1 = {}
                tempdict2 = {}
                for key, value in counter1.iteritems():
                    tempdict1[key] = float(value)/float(count_label1)
                for key, value in counter2.iteritems():
                    tempdict2[key] = float(value)/float(count_label2)
                
                temp.append(tempdict1)
                temp.append(tempdict2)
            
            discrete_distribution.append(temp)
                        
            mean1[j] = sum1[j]/count_label1
            mean2[j] = sum2[j]/count_label2

    # Finding the variance, and the Fischer Value
    for j in range(feature_count):
        if j is not 0:
            for i in range(instance_count):
                if i is not 0:
                    items = data_lines[i].split(",")
                    val = float(items[j].strip())
                    if label[i] == 1:
                        s1_squared[j] += (val-mean1[j])*(val-mean1[j])
                    else:
                        s2_squared[j] += (val-mean2[j])*(val-mean2[j])

    # for i in range(len(feature_names)):
    #     print feature_names[i], mean1[i], mean2[i]
    print discrete_distribution
    fp.close()

if __name__ == '__main__':
    main()