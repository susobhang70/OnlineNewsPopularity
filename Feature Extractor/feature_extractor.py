#!/usr/bin/python
# Script to extract relevant features from the Mashables corpus.
# Returns features in descending order of Fischer Criterion.

import operator

def main():
    """
    Calculate the labels for each feature, and then the mean and 's' values, 
    then the fischer score.
    """

    # Opening the file, and extracting each line
    fp = open('./OnlineNewsPopularity.csv','r')
    data_lines = fp.readlines()

    # The first line consists of all features, we extract number and names.
    feature_names = data_lines[0].split(",")
    feature_count = len(feature_names)
    instance_count = len(data_lines)
    # print instance_count

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
            for i in range(instance_count):
                if i is not 0:
                    items = data_lines[i].split(",")
                    val = float(items[j].strip())
                    if label[i] == 1:
                        sum1[j] += val
                    else:
                        sum2[j] += val
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
            F[j] = ((mean1[j] - mean2[j])*(mean1[j] - mean2[j]))/(s1_squared[j] + s2_squared[j])


    # Making a dict with Fisher Values and Feature Names, and Sorting
    mapping = dict(zip(feature_names, F))
    sorted_mapping = sorted(mapping.items(), key=operator.itemgetter(1))
    sorted_mapping.reverse()
    i = 0
    for key, value in sorted_mapping:
        if i != 0:
            print str(key) + ',' + str(value) + ',' + str(mean1[i]) + ',' + str(mean2[i]) + ',' + str(s1_squared[i]) + ',' + str(s2_squared[i])
        i = i + 1

    fp.close()

if __name__ == '__main__':
    main()