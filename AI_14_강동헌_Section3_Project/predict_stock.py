import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
import joblib


df = pd.read_csv('sam22y.csv')
df.set_index('Date', drop=True, inplace=True)
df.dropna(how='all', inplace=True)

feature = df.loc[ :, ['Open','High','Low','Close','Adj Close','Volume']]
target = df['Change']

from sklearn.preprocessing import StandardScaler
SS=StandardScaler()
feature_scaled=SS.fit_transform(feature)

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(feature_scaled,target)

from xgboost import XGBClassifier
pipe = make_pipeline(
    XGBClassifier(n_estimators=200
                  , random_state=2
                  , n_jobs=-1
                  , max_depth=7
                  , learning_rate=0.2
                 )
)

pipe.fit(X_train, y_train);

predict = pipe.predict(X_test)

plt.plot(predict,'b--')
plt.plot(y_test,'r')

joblib.dump(pipe, 'model_sam22y.pkl')