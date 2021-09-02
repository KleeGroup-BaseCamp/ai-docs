from django.shortcuts import render
from rest_framework import viewsets,permissions
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from donnees.models import *
from .utils import *
import pandas as pd
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import csv
import shutil

class AlgoViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        Algos = Algo.objects.all().order_by('id')
        serializer = Algo_Serializer(Algos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Algo_Serializer(data=request.data)
        if serializer.is_valid():
            if  Algo.objects.filter(algo_name=serializer.validated_data['algo_name']).exists():
                return Response("Already exists", status=status.HTTP_208_ALREADY_REPORTED)
            else:
                df = pd.DataFrame.from_records(
                    dataset_entry.objects.filter(article_dataset=serializer.validated_data['dataset']).values_list(
                                            'article_name','articles_nb_pages','articles_nb_text','article_text','articles_lemmes', 'article_class')
                )
                df.columns=['article_name','articles_nb_pages','articles_nb_text','article_text','articles_lemmes', 'article_class']
                if serializer.validated_data['algo_type']=='k-means':
                    ML_algo=train_algo(df,serializer.validated_data['algo_type'],serializer.validated_data['algo_name'],nb_clusters=request.data.get('cluster'))
                    serializer.save()
                
                else:
                    ML_algo=train_algo(df,serializer.validated_data['algo_type'],serializer.validated_data['algo_name'])
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        # print(request.data,request.data["name"])
        # dataset = dataset_model.objects.get(name=request.data["name"])
        # print(dataset)
        # dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PredictViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        if list(request.data.keys())[1]=="algo_name":
            folder,algo_name=request.data.values()
            model_path='./models/'+algo_name+"/"
            if "k-means.pkl" in os.listdir(model_path):
                prediction_type="Clustering"
            elif "Random Forest.pkl" in os.listdir(model_path):
                prediction_type="Random Forest"
            elif "XGBoost.pkl" in os.listdir(model_path):
                prediction_type="XGBoost"
            DIR='./cache/'+folder+"/"
            online_prediction(DIR,model_path,prediction_type)
        else:
            file_name=list(request.data.keys())[1]
            folder,pdf=list(request.data.values())
            DIR='./cache/'+folder+"/"
            try:
                os.makedirs(DIR)
            except:
                pass    
            path = default_storage.save(DIR+file_name, ContentFile(pdf.read()))
        return Response(folder, status=status.HTTP_201_CREATED)
        

    def get_results(self, request):
        
        print(request.query_params["uuid"])
        response = HttpResponse(content_type='text/csv',
                                headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
                                )
        DIR_RESULTS=os.path.join("./cache/",request.query_params["uuid"])
        df=pd.read_csv(DIR_RESULTS+"/results.csv")
        print(df.head())
        writer = csv.writer(response)
        for i,row in df.iterrows():
            print(row)
            writer.writerow(row)
        shutil.rmtree(DIR_RESULTS)
        return response