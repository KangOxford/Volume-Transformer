import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from os import listdir;from os.path import isfile, join
import statsmodels.api as sm

'''1. transfer data format from format A to B'''
'''2. fulfill nan with the mean of surrounding values'''
'''3. generate sym.csv with all the dates merged in single csv'''

'''format A
['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1', 'timeIndex', 'timeHMs',
       'timeHMe', 'volBuyQty', 'volBuyNotional', 'volSellQty',
       'volSellNotional', 'nrTrades', 'volBuyQty_lit', 'volBuyNotional_lit',
       'volBuyNrTrades_lit', 'volSellQty_lit', 'volSellNotional_lit',
       'volSellNrTrades_lit', 'volBuyQty_hid', 'volBuyNotional_hid',
       'volBuyNrTrades_hid', 'volSellQty_hid', 'volSellNotional_hid',
       'volSellNrTrades_hid', 'bidPx', 'askPx', 'bidQty', 'askQty', 'pret_1m',
       'symbol', 'vol', 'jump_value', 'is_jump', 'signed_jump']
'''
'''format B
['symbol', 'date', 'timeHMs', 'timeHMe', 'intrSn', 'qty', 'volBuyQty',
       'volSellQty', 'ntn', 'volBuyNotional', 'volSellNotional', 'nrTrades',
       'ntr', 'volBuyNrTrades_lit', 'volSellNrTrades_lit']
'''

def ols(train, test):
    def out_of_sample(results, test):
        pred_x = test[0]
        pred_x = sm.add_constant(pred_x, has_constant='add')
        pred_y = results.predict(pred_x)
        real_y = test[1]
        from sklearn.metrics import r2_score
        r_squared = r2_score(real_y, pred_y)
        return r_squared

    import statsmodels.api as sm
    X = train[0]
    # X = sm.add_constant(X)
    X = sm.add_constant(X, has_constant='add')
    Y = train[1]
    results = sm.OLS(Y, X).fit()
    print(results.summary())
    return out_of_sample(results, test)


path = "/Users/kang/Data/"
data_path = path + "out/"
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
file = onlyfiles[0]
df = pd.read_csv(data_path + file, index_col=0)

df_list = []
gpd = df.groupby("date")
for index, item in gpd:
    print
    item['VO'] = item.qty.shift(-1)
    item = item.dropna()
    df_list.append(item)
dflst = pd.DataFrame(pd.concat(df_list))

X0 = dflst.iloc[:,1:-1]
X0 = X0[['date',"intrSn","qty","volBuyQty","volSellQty","volBuyNotional","nrTrades"]]
y0 = dflst.iloc[:,-1]

index = 10000
window_size = 3900
X = X0.iloc[index-window_size:index,:]
y = y0.iloc[index-window_size:index]
X = sm.add_constant(X, has_constant='add')
results = sm.OLS(y, X).fit()
print(results.summary())
y_hat = results.predict([1] +list(X0.iloc[index,:]))
y_true = y0.iloc[index]
(y_true, y_hat)
