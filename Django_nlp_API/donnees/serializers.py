from rest_framework import serializers
from .models import *


class Dataset_models_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = dataset_model
        fields = ['dataset_path','name']
    def create(self, validated_data):
        return dataset_model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.dataset_path = validated_data.get('dataset_path', instance.dataset_path)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
        
class Dataset_entry_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = dataset_entry
        fields = ['article_name', 'articles_nb_pages', 'articles_nb_text', 'article_text', 'articles_lemmes',
         'article_class', 'articles_Non_Alphanumeric','article_dataset']
    def create(self, validated_data):
        return dataset_entry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.article_name = validated_data.get('article_name', instance.article_name)
        instance.articles_nb_pages = validated_data.get('articles_nb_pages', instance.articles_nb_pages)
        instance.articles_nb_text = validated_data.get('articles_nb_text', instance.articles_nb_text)
        instance.article_text = validated_data.get('article_text', instance.article_text)
        instance.articles_lemmes = validated_data.get('articles_lemmes', instance.articles_lemmes)
        instance.article_class = validated_data.get('article_class', instance.article_class)
        instance.articles_Non_Alphanumeric = validated_data.get('articles_Non_Alphanumeric', instance.articles_Non_Alphanumeric)
        instance.article_dataset = validated_data.get('article_dataset', instance.article_dataset)
        instance.save()
        return instance