from django.shortcuts import render
from rest_framework import viewsets,permissions
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from donnees.models import *
from .utils import *
import pandas as pd


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
                print(df.head())
                full_train,full_test=create_TF_IDF(df)
                ML_algo=train_algo(full_train,full_test,serializer.validated_data['algo_type'],serializer.validated_data['algo_name'])
                eval_algo(full_test,ML_algo,serializer.validated_data['algo_name'])
                # serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        # print(request.data,request.data["name"])
        # dataset = dataset_model.objects.get(name=request.data["name"])
        # print(dataset)
        # dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)