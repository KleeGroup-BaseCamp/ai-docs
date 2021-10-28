import json
import logging

from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import *
from .serializers import *

# Get an instance of a logger
logger = logging.getLogger(__name__)

class DatasetModelViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        dataset_models = DatasetModel.objects.all().order_by('id')
        serializer = DatasetModelsSerializer(dataset_models, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DatasetModelsSerializer(data=request.data)
        if serializer.is_valid():
            if  DatasetModel.objects.filter(name=serializer.validated_data['name']).exists():
                return Response("Already exists", status=status.HTTP_208_ALREADY_REPORTED)
            else:
                df=create_dataset(serializer.validated_data['dataset_path'],serializer.validated_data['name'])
                df.drop('content_text_join',axis=1,inplace=True)
                json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
                for dic in json_list:
                    DatasetEntry.objects.get_or_create(**dic)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        dataset = DatasetModel.objects.get(name=request.data["name"])
        DatasetEntry.objects.filter(article_dataset=request.data["name"]).delete()
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DatasetEntryViewSet(APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    # queryset = dataset_entry.objects.all().order_by('id')
    # serializer_class = Dataset_entry_Serializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        dataset_entries = DatasetEntry.objects.all()
        serializer = DatasetEntrySerializer(dataset_entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DatasetEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)