import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import MinMaxScaler,LabelEncoder,StandardScaler
from sklearn.model_selection import train_test_split,cross_val_score, KFold,GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,plot_confusion_matrix,confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from mlxtend.feature_selection import ColumnSelector
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
import xgboost as xgb
import matplotlib.pyplot as plt
from xgboost.sklearn import XGBClassifier
import pickle  
import os
from donnees.utils import *
import spacy

def create_TF_IDF(df):
    train,test=train_test_split(df,test_size=0.2)

    word_vectorizer = TfidfVectorizer(
        strip_accents='unicode',
        ngram_range=(1, 1),
        min_df=0.03,
        max_df=0.90,
        max_features=500)

    word_vectorizer.fit(train['articles_lemmes'])
    train_word_features = word_vectorizer.transform(train['articles_lemmes'])
    test_word_features = word_vectorizer.transform(test['articles_lemmes'])

    full_train=pd.concat((pd.DataFrame(train_word_features.toarray()),pd.DataFrame(train['article_class'].reset_index(drop=True)) ),axis=1)
    full_test=pd.concat((pd.DataFrame(test_word_features.toarray()),pd.DataFrame(test['article_class'].reset_index(drop=True)) ),axis=1)
    return full_train,full_test

def create_TF_IDF_cluster(df):

    word_vectorizer = TfidfVectorizer(
        strip_accents='unicode',
        ngram_range=(1, 1),
        min_df=0.03,
        max_df=0.90,
        max_features=500)

    full_word_features =word_vectorizer.fit_transform(df['articles_lemmes'])

    full=pd.concat((pd.DataFrame(full_word_features.toarray()),pd.DataFrame(df['article_class'].reset_index(drop=True)) ),axis=1)
    return full

def plot_top_words(model, feature_names, n_top_words,plot=False):
    topic=model.components_[0]
    top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
    top_features = [feature_names[i] for i in top_features_ind.flatten()]
    weights = topic[top_features_ind]
    if plot:
        fig, axes = plt.subplots(1, 1, figsize=(15, 8), sharex=True)
        ax = axes
        ax.barh(top_features, weights, height=0.7)
        ax.invert_yaxis()
        ax.tick_params(axis='both', which='major', labelsize=20)
        for i in 'top right left'.split():
            ax.spines[i].set_visible(False)
        plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
        plt.show()

    df_topic=pd.DataFrame({"feature":top_features,"weight":weights})
    
    return "_".join(top_features[:5]),df_topic


def train_algo(df,algo,name,nb_clusters='auto'):
    DIR="./models/"+name+"/"
    if not(os.path.isdir(DIR)):
        os.makedirs(DIR)

    if algo=="XGBoost":
        train,test=train_test_split(df,test_size=0.2)
        word_vectorizer = TfidfVectorizer(
                            strip_accents='unicode',
                            stop_words=stopwords.words('french'),
                            ngram_range=(1, 1),
                            min_df=0.03,
                            max_df=0.90,
                            max_features=500)

        pipe=Pipeline([
            ('col_selector', ColumnSelector(cols=('articles_lemmes'),drop_axis=True)),
            ('TF_IDF', word_vectorizer),
        ])
        
        X_train=pipe.fit_transform(train)
        X_test=pipe.transform(test)

        Label_Scaler=LabelEncoder()
        y_train_scaler=Label_Scaler.fit_transform(train.article_class)
        y_test_scaler=Label_Scaler.transform(test.article_class)

        eval_set = (X_test, y_test_scaler)

        ML_algo = XGBClassifier(max_depth=None,learning_rate=0.05,n_estimators=2000)
        ML_algo.fit(X_train, y_train_scaler, verbose=True, eval_set=[eval_set],early_stopping_rounds=20, eval_metric="mlogloss")

        list_to_save=[pipe,Label_Scaler,ML_algo]
        
        ML_algo.score(X_test,y_test_scaler)
        y_pred=ML_algo.predict(X_test)
        target_names = list(Label_Scaler.inverse_transform(range(0,len(test.article_class.unique()))))
        
        report=classification_report(y_test_scaler, y_pred, output_dict=True)
        report = pd.DataFrame(report)
        report.columns=target_names+list(report.columns[-3:])
        report.transpose().to_csv(DIR+"report.csv")
        
        cm=pd.DataFrame(confusion_matrix(Label_Scaler.inverse_transform(y_test_scaler), Label_Scaler.inverse_transform(y_pred), labels=target_names,normalize="true"))
        cm.index=target_names
        cm.columns=target_names
        cm.to_csv(DIR+"confusion_matrix.csv")

    elif algo=="Random Forest":
        train,test=train_test_split(df,test_size=0.2)
        word_vectorizer = TfidfVectorizer(
                            strip_accents='unicode',
                            stop_words=stopwords.words('french'),
                            ngram_range=(1, 1),
                            min_df=0.03,
                            max_df=0.90,
                            max_features=500)


        Label_Scaler=LabelEncoder()
        y_train_scaler=Label_Scaler.fit_transform(train.article_class)
        y_test_scaler=Label_Scaler.transform(test.article_class)

        pipe=Pipeline([
            ('col_selector', ColumnSelector(cols=('articles_lemmes'),drop_axis=True)),
            ('TF_IDF', word_vectorizer),
            ('RandomForest', RandomForestClassifier(n_estimators=300, max_depth=None))
        ])

        
        pipe.fit(train,y_train_scaler)
        list_to_save=[pipe,Label_Scaler]

        pipe.score(test,y_test_scaler)
        y_pred=pipe.predict(test.iloc[:,:-1])
        target_names = list(Label_Scaler.inverse_transform(range(0,len(test.article_class.unique()))))
        
        report=classification_report(y_test_scaler, y_pred, output_dict=True)
        report = pd.DataFrame(report)
        report.columns=target_names+list(report.columns[-3:])
        report.transpose().to_csv(DIR+"report.csv")
        
        cm=pd.DataFrame(confusion_matrix(Label_Scaler.inverse_transform(y_test_scaler), Label_Scaler.inverse_transform(y_pred), labels=target_names,normalize="true"))
        cm.index=target_names
        cm.columns=target_names
        cm.to_csv(DIR+"confusion_matrix.csv")


    elif algo=="k-means":
        nlp = spacy.load("en_core_web_lg")
        for i in nlp.pipe_names:
            if not(i in ['tok2vec', 'morphologizer','tagger','parser', 'attribute_ruler', 'lemmatizer']):
                nlp.disable_pipe(i)
        print(nlp.pipe_names)
        word_vectorizer = TfidfVectorizer(
                                            strip_accents='unicode',
                                            stop_words=stopwords.words('french'),
                                            ngram_range=(1, 1),
                                            min_df=0.03,
                                            max_df=0.90,
                                            max_features=500)
        ML_algo=KMeans(n_clusters=nb_clusters)
        pipe=Pipeline([
            ('col_selector', ColumnSelector(cols=('articles_lemmes'),drop_axis=True)),
            ('TF_IDF', word_vectorizer),
            ('Kmeans', ML_algo)])
        pipe.fit(df)
        clustering=pipe.predict(df)
        df['prediction']=clustering
        clusters_topics=[]
        clusters_titles=[]
        data=[]
        mapping_dict={}
        for text in df['articles_lemmes']:
            doc = nlp(text)
            filtered=" ".join([token.lemma_ for token in doc if not(token.is_oov or token.is_stop) and (token.is_alpha or token.is_punct) and len(token)>1 and token.pos_ in ["ADJ","ADV","NOUN"] ])
            data.append(filtered)
        tfidf_vectorizer = TfidfVectorizer(
                                            strip_accents='unicode',
                                            stop_words=stopwords.words('french'),
                                            ngram_range=(1, 1),
                                            min_df=0.03,
                                            max_df=0.90,
                                            max_features=500)
        tfidf = tfidf_vectorizer.fit_transform(data)
        for cluster in df['prediction'].unique():
            data_cluster=tfidf[df['prediction']==cluster]
            nmf = NMF(n_components=1,alpha=.1, l1_ratio=.5).fit(data_cluster)
            tfidf_feature_names = tfidf_vectorizer.get_feature_names()
            title,df_topic=plot_top_words(nmf, tfidf_feature_names, 25)
            df_topic["cluster_nb"]=cluster
            df_topic["cluster_title"]=title
            
            mapping_dict[cluster]=title
            clusters_topics.append(df_topic)
        pd.concat(clusters_topics,axis=0).to_csv(DIR+"topics.csv")
        df.to_csv(DIR+"dataframe.csv")
        list_to_save=[pipe,mapping_dict]
    
    pkl_filename = DIR+algo+'.pkl'
    with open(pkl_filename, 'wb') as file:
        pickle.dump(list_to_save, file)


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

def online_prediction(path,model_path,prediction_type):
    df=create_dataset(path,'prediction')
    for file in os.listdir(model_path):
        if file.endswith(".pkl"):
            model_path=os.path.join(model_path,file)
        
    with open(model_path,'rb') as f:
        pkl=pickle.load(f)
    if prediction_type=="Clustering":
        pipe,mapping_dict=pkl[0],pkl[1]
        print(mapping_dict)
        predictions_encoded=pipe.predict(df)
        print(predictions_encoded)
        predictions_mapped=[mapping_dict[prediction] for prediction in predictions_encoded]
        print(predictions_mapped)
        df['prediction_mapped']=predictions_mapped
        print(df)
        df['prediction']=predictions_encoded
        df[['content_text_join','prediction','prediction_mapped']].to_csv(os.path.join(path,'results.csv'),header=['text','prediction','titre'])

    elif prediction_type=="Random Forest":
        pipe,LabelScaler=pkl[0],pkl[1]
        predictions=pipe.predict(df)
        predictions_encoded=LabelScaler.inverse_transform(predictions)
        df['prediction']=predictions_encoded
        df[['content_text_join','prediction']].to_csv(os.path.join(path,'results.csv'),header=['text','prediction'])

    elif prediction_type=="XGBoost":
        pipe,LabelScaler,ML_algo=pkl[0],pkl[1],pkl[2]
        preprocessed=pipe.transform(df)
        predictions=ML_algo.predict(preprocessed)
        predictions_encoded=LabelScaler.inverse_transform(predictions)
        df['prediction']=predictions_encoded
        df[['content_text_join','prediction']].to_csv(os.path.join(path,'results.csv'),header=['text','prediction'])

