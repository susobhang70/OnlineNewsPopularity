#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import csv
np.seterr(all='raise')
THETA = 0.000000001
ETA   = 0.0000007

features_list = ['kw_avg_avg', 'LDA_02', 'data_channel_is_world', 'is_weekend',\
                'data_channel_is_socmed', 'weekday_is_saturday', 'LDA_04', 'data_channel_is_entertainment',\
                'data_channel_is_tech', 'kw_max_avg', 'weekday_is_sunday', 'LDA_00', 'num_hrefs',\
                'global_subjectivity', 'kw_min_avg', 'global_sentiment_polarity', 'rate_negative_words',\
                'num_keywords', 'num_imgs', 'LDA_01']

def augment(w):
    return np.column_stack( [np.array([1]*(len(w))), w])

def convert_to_binary(B):
    C = []
    for i in B:
        if i > 1400:
            C.append(1)
        else:
            C.append(-1)
    return C

def LMS(y, b, eta, theta, a):
    k = 0
    normalcount = 1
    flag = False
    while True:
        # try:
            neweta = eta / normalcount
            estimatedValue = np.dot(a, y[k])
            product = neweta * (b[k] - estimatedValue)
            newvector = product * y[k]
            newvalue = np.linalg.norm(newvector)
            a = a + newvector
            # print newvalue, product, neweta, b[k], estimatedValue, k, normalcount, list(i for i in newvector), list(i for i in y[k]), list(i for i in a)
            # print
            if newvalue < theta and flag:
                print b[k], estimatedValue, normalcount
                break
            normalcount += 1
            if k == len(y) - 1:
                flag = True
            k = (k + 1) % len(y)
        # except:
        #     # print product
        #     print y[k]
        #     print a
        #     print b[k]
        #     print normalcount
        #     break
    # print a
    return a

def main():
    with open('OnlineNewsPopularity.csv', 'r') as file:
        content = csv.reader((line.replace(', ', ',') for line in file), delimiter=',', quotechar='|')
        processedContent = []
        for row in content:
            processedContent.append(row)
        data = []
        indexList = []
        B = []
        for i in range(len(processedContent[0])):
            if str(processedContent[0][i]) in features_list:
                indexList.append(i)
        processedContent = processedContent[1:]
        for i in processedContent:
            tempList = []
            for j in indexList:
                tempList.append(i[j])
            B.append(float(i[-1]))
            data.append(tempList)

        for i in range(len(data)):
            for j in range(len(data[i])):
                data[i][j] = float(data[i][j])

        B = convert_to_binary(B)
        # print B
        data = np.array(data, dtype = np.float64)

        data = augment(data)
        
        traindata  = data[:int(0.7 * len(data))]
        trainresult = B[:int(0.7 * len(data))]
        cvtestdata = data[int(0.7 * len(data)) + 1:]
        cvtestresult = B[int(0.7 * len(data)) + 1:]

        weights = [1.0000] * (len(features_list) + 1)
        # weights = np.random.rand(len(features_list) + 1)

        weights = LMS(traindata, trainresult, ETA, THETA, weights)
        # weights = LMS(data, B, ETA, THETA, weights)

        # testing from now
        count = 0
        for i in range(len(cvtestdata)):
            estimatedValue = np.dot(weights, cvtestdata[i])
            # print estimatedValue
            if estimatedValue >= 0:
                estimatedValue = 1
            else:
                estimatedValue = -1
            if estimatedValue == cvtestresult[i]:
                count = count + 1
        # for i in range(len(data)):
        #     estimatedValue = np.dot(weights, data[i])
        #     if estimatedValue >= 0:
        #         estimatedValue = 1
        #     else:
        #         estimatedValue = -1
        #     if estimatedValue == B[i]:
        #         count = count + 1

        accuracy = float(count) * 100.00 / float(len(cvtestresult))
        # accuracy = float(count) * 100.00 / float(len(B))
        print accuracy

if __name__ == '__main__':
    main()