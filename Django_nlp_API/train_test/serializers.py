from rest_framework import serializers
from .models import *


class Algo_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Algo
        fields = ['algo_name','algo_type','dataset']
    def create(self, validated_data):
        return Algo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.algo_name = validated_data.get('algo_name', instance.algo_name)
        instance.algo_type = validated_data.get('algo_type', instance.algo_type)
        instance.dataset = validated_data.get('dataset', instance.dataset)
        instance.save()
        return instance
