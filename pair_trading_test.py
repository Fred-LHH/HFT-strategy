import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.api as tsaapi
import os

class CointTest(object):

    def __init__(self, X1, X2):
        self.X1 = X1
        self.X2 = X2
        self.bias = 0
        self.beta = 1
        self.e = []

    def adf_test(self):
        '''
        检验X1, X2是否是同阶单整序列
        Return:
        ADF检验的P值
        '''
        p_x1 = tsaapi.stattools.adfuller(self.X1)
        p_x2 = tsaapi.stattools.adfuller(self.X2)
        return p_x1[1], p_x2[1]
    
    def adf_test_diff(self):
        '''
        检验差分后的X1, X2是否是平稳的
        Return:
        diff_X1(X2) ADF检验的P值
        '''
        diff_p_x1 = tsaapi.stattools.adfuller(pd.Series(self.X1).diff().dropna())
        diff_p_x2 = tsaapi.stattools.adfuller(pd.Series(self.X2).diff().dropna())
        return diff_p_x1[1], diff_p_x2[1]
    
    def fit(self, print_summary=False):
        '''
        Return:
        b, beta, e
        '''
        self.X2 = sm.add_constant(self.X2)
        ols = sm.OLS(self.X1, self.X2)
        result = ols.fit()
        if print_summary:
            print(result.summary2())
        self.b = result.params[0]
        self.beta = result.params[1]
        self.e = result.resid
        return self.b, self.beta, self.e
    
    def resid_con_test(self, maxlag=None):
        '''
        检验残差是否平稳
        maxlag: 最大滞后项, 默认为AIC
        Return:
        ADF检验统计量, Pvalue, 滞后阶数, critical value
        '''
        ADFresult = tsaapi.stattools.adfuller(self.e, maxlag=maxlag)
        return ADFresult[0], ADFresult[1], ADFresult[2], ADFresult[4]
    
                