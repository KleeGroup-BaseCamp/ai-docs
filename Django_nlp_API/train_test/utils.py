import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler,LabelEncoder,StandardScaler
from sklearn.model_selection import train_test_split,cross_val_score, KFold,GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score,train_test_split
from sklearn.metrics import classification_report,plot_confusion_matrix,confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
import xgboost as xgb
import matplotlib.pyplot as plt
from xgboost.sklearn import XGBClassifier
import pickle  
import os

def create_TF_IDF(df):
    train,test=train_test_split(df,test_size=0.2)

    word_vectorizer = TfidfVectorizer(
        strip_accents='unicode',
        stop_words=stopwords.words('french'),
        ngram_range=(1, 1),
        min_df=0.03,
        max_df=0.90,
        max_features=1000)

    word_vectorizer.fit(train['articles_lemmes'])
    train_word_features = word_vectorizer.transform(train['articles_lemmes'])
    test_word_features = word_vectorizer.transform(test['articles_lemmes'])

    full_train=pd.concat((pd.DataFrame(train_word_features.toarray()),pd.DataFrame(train['article_class'].reset_index(drop=True)) ),axis=1)
    full_test=pd.concat((pd.DataFrame(test_word_features.toarray()),pd.DataFrame(test['article_class'].reset_index(drop=True)) ),axis=1)
    return full_train,full_test

def train_algo(train,test,algo,name):
    Label_Scaler=LabelEncoder()
    
    y_train_scaler=Label_Scaler.fit_transform(train.article_class)
    y_test_scaler=Label_Scaler.transform(test.article_class)

    eval_set = [(test.iloc[:,:-1], y_test_scaler)]
    if algo=="XGBoost":
        ML_algo = XGBClassifier(max_depth=None,learning_rate=0.05,n_estimators=2000)
        ML_algo.fit(train.iloc[:,:-1], y_train_scaler, verbose=True, eval_set=eval_set,early_stopping_rounds=20, eval_metric="mlogloss")
    elif algo=="Random Forest":
        ML_algo=RandomForestClassifier(n_estimators=300, max_depth=None)
        ML_algo.fit(train.iloc[:,:-1], y_train_scaler)
    DIR="./models/"+name+"/"
    if not(os.path.isdir(DIR)):
        os.makedirs(DIR)
    
    pkl_filename = DIR+algo+'.pkl'
    with open(pkl_filename, 'wb') as file:
        pickle.dump(ML_algo, file)

    return ML_algo

def eval_algo(test,ML_algo,name):
    DIR="./models/"+name+"/"
    if not(os.path.isdir(DIR)):
        os.mkdir(DIR)

    Label_Scaler=LabelEncoder()
    
    y_test_scaler=Label_Scaler.fit_transform(test.article_class)
    ML_algo.score(test.iloc[:,:-1],y_test_scaler)
    y_pred=ML_algo.predict(test.iloc[:,:-1])

    target_names = list(Label_Scaler.inverse_transform(range(0,len(test.article_class.unique()))))
    report=classification_report(y_test_scaler, y_pred, output_dict=True)
    report = pd.DataFrame(report)
    report.columns=target_names+list(report.columns[-3:])
    report.transpose().to_csv(DIR+"report.csv")
    cm=pd.DataFrame(confusion_matrix(y_test_scaler, y_pred, labels=[0,1,2,3,4],normalize="true"))
    cm.index=target_names
    cm.columns=target_names
    cm.to_csv(DIR+"confusion_matrix.csv")