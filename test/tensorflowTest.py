# encoding: utf-8

'''
@author: LiDami
@license: (C) Copyright 2013-2017, BigBigData Manager Corporation Limited.
@contact: li.dami@foxmail.com
@software: MacBookPro
@file: tensorflowTest.py
@time: 2017/12/10 21:09
@desc:
'''
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# a = np.zeros((3,3))
# ta = tf.convert_to_tensor(a)
# with tf.Session() as sess:
#     print (sess.run(ta))


# num_points = 1000
# vector_set = []
# for i in range(num_points):
#     x1 = np.random.normal(0.0,0.55)
#     y1 = x1 * 0.1 + 0.3 + np.random.normal(0.0,0.03)
#     vector_set.append([x1,y1])
#
#
# x_data = [v[0] for v in vector_set]
# y_data = [v[1] for v in vector_set]
#
# plt.scatter(x_data,y_data,c='r')
# plt.show()

from sklearn.feature_extraction.text import CountVectorizer
texts = ["A B C ","B B D","C C A"]
cv = CountVectorizer()
cv_fit = cv.fit_transform(texts)

print(cv.get_feature_names())
 # print(cv.get_feature_names())
 # print(cv_fit.toarray())
 # print(cv_fit.toarray().sum(axis=0))



