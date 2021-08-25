from django.shortcuts import render
from rest_framework import viewsets,permissions
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .utils import *

class dataset_modelViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        dataset_models = dataset_model.objects.all().order_by('id')
        serializer = Dataset_models_Serializer(dataset_models, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Dataset_models_Serializer(data=request.data)
        if serializer.is_valid():
            if  dataset_model.objects.filter(name=serializer.validated_data['name']).exists():
                return Response("Already exists", status=status.HTTP_208_ALREADY_REPORTED)
            else:
                df=create_dataset(serializer.validated_data['dataset_path'],serializer.validated_data['name'])
                df.drop('content_text_join',axis=1,inplace=True)
                json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
                for dic in json_list:
                    dataset_entry.objects.get_or_create(**dic)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        print(request.data,request.data["name"])
        dataset = dataset_model.objects.get(name=request.data["name"])
        print(dataset)
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class dataset_entryViewSet(APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    # queryset = dataset_entry.objects.all().order_by('id')
    # serializer_class = Dataset_entry_Serializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        dataset_entries = dataset_entry.objects.all()
        serializer = Dataset_entry_Serializer(dataset_entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Dataset_entry_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)