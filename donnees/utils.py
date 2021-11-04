import io
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import base64
import urllib
import pandas as pd
import os 
import fitz
import re
from wordcloud import WordCloud
from stop_words import get_stop_words
import spacy
import logging
import ocrmypdf

from django.shortcuts import render

from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib.colors import Normalize

# Get an instance of a logger
logger = logging.getLogger(__name__)

def extract(path,pages_to_extract=None):
    with fitz.open(path) as doc:
        if pages_to_extract is None:
            pages_to_extract=range(doc.page_count)
        text = " ".join([doc.get_page_text(i) for i in pages_to_extract])
        text = text.replace('\x00','').strip()
        page_count=doc.page_count
    return text,page_count,len(text)

def create_dataset(path,key):
    #['tok2vec', 'morphologizer', 'parser', 'attribute_ruler', 'lemmatizer', 'ner']
    nlp = spacy.load("fr_core_news_lg")
    for i in nlp.pipe_names:
        if not(i in ['tok2vec', 'lemmatizer', 'morphologizer']):
            nlp.disable_pipe(i)

    tuples=[]
    count_elem=0

    for elem in os.listdir(path):
        if os.path.isdir(os.path.join(path,elem)):
            count_elem+=1
    if count_elem>1:
        for dossier in os.listdir(path):
            if not("." in dossier) and os.path.isdir(os.path.join(path,dossier)):
                for file in os.listdir(os.path.join(path,dossier)):
                    if file.endswith(".pdf"):
                        try:
                            text, nb_pages, nb_text = extract(os.path.join(path,dossier,file))
                            s = text.replace("\n"," ")
                            s = re.sub('[^0-9`-z?-ZÀ-ÁÈ-ËÒ-ÖÙ-Üà-âç-ëî-ïñ-öù-ü]+', ' ', s)
                            if len(s)>nlp.max_length:
                                s = s[:nlp.max_length]
                            doc = nlp(s)
                            lemmatized=" ".join([token.lemma_ for token in doc if not(token.is_oov or token.is_stop) and (token.is_alpha or token.is_punct) and len(token)>1 ])
                            tuples.append((os.path.join(path, dossier, file), nb_pages, nb_text, text, s, lemmatized, dossier))
                        except Exception:
                            logging.exception(f"Error while extracting {path}")

        df = pd.DataFrame(tuples, columns =['article_name','articles_nb_pages','articles_nb_text','content_text_join','article_text','articles_lemmes', 'article_class'])
        df['articles_Non_Alphanumeric'] = df['content_text_join'].str.count(r'[^0-9`-z?-ZÀ-ÁÈ-ËÒ-ÖÙ-Üà-âç-ëî-ïñ-öù-ü-\t\r\n\v\040]')
        df['article_dataset'] = key
    else:
        nb_total_files = len(os.listdir(path))
        nb_processed_file = 0
        logger.info(f"Nb files to process : {nb_total_files} Path: {path}")
        for file in os.listdir(path):
            if file.endswith(".pdf"):
                try:
                    logger.info(f"Processing ({nb_processed_file}/{nb_total_files}) {path}")
                    text, nb_pages, nb_text = extract(os.path.join(path,file))
                    s = text.replace("\n"," ")
                    s = re.sub('[^0-9`-z?-ZÀ-ÁÈ-ËÒ-ÖÙ-Üà-âç-ëî-ïñ-öù-ü]+', ' ', s)
                    if len(s) > nlp.max_length:
                        s = s[:nlp.max_length]
                    doc = nlp(s)
                    lemmatized = " ".join([token.lemma_ for token in doc if not(token.is_oov or token.is_stop) and (token.is_alpha or token.is_punct) and len(token)>1])
                    tuples.append((os.path.join(path,file), nb_pages, nb_text, text, s, lemmatized, "a_determiner"))
                except Exception:
                    logging.exception(f"Error while extracting {path}")
            nb_processed_file = nb_processed_file + 1

        df = pd.DataFrame(tuples, columns = ['article_name', 'articles_nb_pages', 'articles_nb_text', 'content_text_join', 'article_text', 'articles_lemmes', 'article_class'])
        df['articles_Non_Alphanumeric'] = df['content_text_join'].str.count(r'[^0-9`-z?-ZÀ-ÁÈ-ËÒ-ÖÙ-Üà-âç-ëî-ïñ-öù-ü-\t\r\n\v\040]')
        df['article_dataset'] = key

    path_preprocess='./cache/preprocessed/'
    if not(os.path.exists(path_preprocess)):
        os.makedirs(path_preprocess)

    for index,row in df.iterrows():
        if row.articles_nb_text<250 or row.articles_Non_Alphanumeric/row.articles_nb_text>0.5 :
            print("ocr")
            ocrmypdf.ocr(input_file=row.article_name, output_file=path_preprocess+'preprocessed.pdf',output_type="pdf"\
                         ,remove_background=False, deskew=True, language='eng+fra', sidecar=path_preprocess+'side.txt')
            with open(path_preprocess+"side.txt",'r') as f:
                text = f.read()
                df.loc[index,'content_text_join'] = text
                s=text.replace("\n"," ")
                s = re.sub('[^0-9`-z?-ZÀ-ÁÈ-ËÒ-ÖÙ-Üà-âç-ëî-ïñ-öù-ü]+', ' ', s)
                if len(s)>nlp.max_length:
                    s=s[:nlp.max_length]
                doc = nlp(s)
                lemmatized=" ".join([token.lemma_ for token in doc if not(token.is_oov or token.is_stop) and (token.is_alpha or token.is_punct) and len(token)>1])
                df.loc[index,'content_text_join'] = text
                df.loc[index,'article_text'] = s
                df.loc[index,'articles_lemmes'] = lemmatized
    
    return df

def create_wordcloud(text):
    plt.figure()
    plt.axis("off")
    stopwords = set(get_stop_words('french'))
    wordcloud = WordCloud(stopwords=stopwords,max_words=100).generate(text)
    return plt.imshow(wordcloud.to_array())

def create_VIZ_PCA(df):
    labels=df["article_class"]
    le =LabelEncoder()
    encoded_labels=le.fit_transform(labels)
    vectorizer=TfidfVectorizer(min_df=0.01,max_df=0.95)
    TF_IDF_results=vectorizer.fit_transform(df["article_text"].values)
    X = TF_IDF_results.toarray()
    X_std = StandardScaler().fit_transform(X)
    model = PCA(n_components=3)
    y=encoded_labels
    x_pca=model.fit_transform(X_std)
    cNorm = Normalize(vmin=0,vmax=max(encoded_labels)+1) #normalise the colormap
    scalarMap = cm.ScalarMappable(norm=cNorm,cmap='hot') #map numbers to colors

    fig, ax = plt.subplots(figsize=(25,15))
    plt.title('2D_PCA')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    for label in labels.unique():
        ax.scatter(x_pca[labels==label,0], x_pca[labels==label,1],
                   c=scalarMap.to_rgba(le.transform([label])),label=label)
    plt.legend()
    fig_2D=fig
    fig = plt.figure(figsize=(25,15))
    ax = fig.add_subplot(111, projection='3d')
    for label in labels.unique():
        ax.scatter(x_pca[labels==label,0], x_pca[labels==label,1],x_pca[labels==label,2],
                   c=scalarMap.to_rgba(le.transform([label])),label=label)
    plt.legend()
    xAxisLine = ((min(x_pca[:,0]), max(x_pca[:,0])), (0, 0), (0,0))
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r')
    yAxisLine = ((0, 0), (min(x_pca[:,1]), max(x_pca[:,1])), (0,0))
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r')
    zAxisLine = ((0, 0), (0,0), (min(x_pca[:,2]), max(x_pca[:,2])))
    ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r')
    
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")
    ax.set_title("3D_PCA")
    fig_3D=fig
    
    return fig_2D,fig_3D

def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('graph')
    plt.plot(x,y)
    plt.xticks(rotation=45)
    
    graph=get_graph()
    return graph

def generate_uri(fig):

    # Store image in a string buffer
    buffer = io.BytesIO()
    fig.savefig(buffer,format='png')
    buffer.seek(0)
    string=base64.b64encode(buffer.read())
    uri=urllib.parse.quote(string)

    # Send buffer in a http response the the browser with the mime type image/png set
    return uri

