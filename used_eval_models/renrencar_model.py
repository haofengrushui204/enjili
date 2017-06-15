# -*- coding:utf-8 -*-
'''
Created on 2017/5/25

@author: kongyangyang
'''
#人人车二手车估值模型
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import GradientBoostingRegressor
from src.auto_evaluation_models.config import  *
from sklearn.utils import shuffle
import matplotlib.pyplot as plt


class RRCarEstimation(object):
    def __init__(self):
        self.data_x = None
        self.data_y = None
        self.xcbj = []

    def getFeature(self, srcpath):
        data_x = []
        data_y = []
        xcbj = []
        with open(srcpath, 'r') as file_read:
            for line in file_read:
                items = [float(item) for item in line.strip().split(",")]
                data_x.append(items[:-2])
                data_y.append(items[-2])
                xcbj.append(items[-1])

        # X_scaled = preprocessing.scale(data_x)
        self.data_x = np.array(data_x)
        self.data_y = np.array(data_y)
        self.xcbj = np.array(xcbj)

    def train_gbdt(self,n_estimators = 300,learning_rate = 0.01, max_depth = 5,random_state = 0, loss = "lad"):
        X, y,xcbj = shuffle(self.data_x, self.data_y, self.xcbj, random_state=random_state)
        X = X.astype(np.float32)
        offset = int(X.shape[0] * 0.7)
        X_train, y_train = X[:offset], y[:offset]
        X_test, y_test = X[offset:], y[offset:]
        print X_train.shape,X_test.shape

        params = {"n_estimators":n_estimators,
                 "learning_rate":learning_rate,
                 "max_depth":max_depth,
                 "random_state":random_state,
                 "loss":loss
                 }
        est = GradientBoostingRegressor(**params).fit(X_train, y_train)

        y_train_predict = est.predict(X_train)
        mae = mean_absolute_error(y_train, y_train_predict)
        print("train MAE: %.4f" % mae)

        y_test_predict = est.predict(X_test)
        mae = mean_absolute_error(y_test, y_test_predict)
        print("test MAE: %.4f" % mae)

        # y_pred = est.predict(X_test)
        # for i in range(y_pred.shape[0]):
        #     print y_test[i],y_pred[i], y_test[i] - y_pred[i]
        # self.gdrt_plot(est, params, X_test, y_test)

        # self.train_gbdt_with_czbj(X_train, y_train, X_test, y_test, y_train_predict, y_test_predict, xcbj, offset, params)

    def train_gbdt_with_czbj(self, X_train, y_train, X_test, y_test, y_train_predict, y_test_predict, xcbj, offset, params):
        m, n = X_train.shape
        X_train_new = np.zeros((m, n+1))
        for i in range(m):
            X_train_new[i,:-1] = X_train[i,:]
            if xcbj[i]*y_train_predict[i] * 0.03 > 0.3:
                X_train_new[i,-1] = y_train_predict[i] * 0.03
            else:
                X_train_new[i,-1] = 0.3 / xcbj[i]

        m, n = X_test.shape
        X_test_new = np.zeros((m, n+1))
        for i in range(m):
            X_test_new[i,:-1] = X_test[i,:]
            if xcbj[offset + i]*y_test_predict[i] * 0.03 > 0.3:
                X_test_new[i,-1] = y_test_predict[i] * 0.03
            else:
                X_test_new[i,-1] = 0.3 / xcbj[offset + i]

        est = GradientBoostingRegressor(**params).fit(X_train_new, y_train)

        mae = mean_absolute_error(y_train, est.predict(X_train_new))
        print("train MAE with czbj: %.4f" % mae)

        mae = mean_absolute_error(y_test, est.predict(X_test_new))
        print("test MAE czbj: %.4f" % mae)


    def gdrt_plot(self, est, params, X_test, y_test):
        test_score = np.zeros((params['n_estimators'],), dtype=np.float64)

        for i, y_pred in enumerate(est.staged_predict(X_test)):
            test_score[i] = est.loss_(y_test, y_pred)

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.title('Deviance')
        plt.plot(np.arange(params['n_estimators']) + 1, est.train_score_, 'b-',
                 label='Training Set Deviance')
        plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
                 label='Test Set Deviance')
        plt.legend(loc='upper right')
        plt.xlabel('Boosting Iterations')
        plt.ylabel('Deviance')
        plt.show()

    def analysis(self, est):
        '''
            gbrt 结果分析
        '''


    def main(self, samples_path, n_estimators = 300, learning_rate = 0.01, max_depth = 5, random_state = 0, loss = "lad", mode = "train"):
        if mode == "train":
            self.getFeature(samples_path)
            self.train_gbdt(n_estimators, learning_rate, max_depth, random_state, loss)
        else:
            pass



if __name__ == "__main__":
    RRCarEstimation_tool = RRCarEstimation()
    RRCarEstimation_tool.getFeature(workdir + "rrcar_samples")
    RRCarEstimation_tool.train_gbdt()


