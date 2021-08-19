from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import *
from .utils import *
import matplotlib.pyplot as plt
import numpy as np
from .forms import *
import json
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.decomposition import PCA


def dataset_create_view(request):
    form=dataset_form(request.POST or None)
    context={"form":form}
    if form.is_valid():
        dataset_path=form.cleaned_data['dataset_path']
        dataset_name=form.cleaned_data['name']
        df=create_dataset(dataset_path,dataset_name)
        df.drop('content_text_join',axis=1,inplace=True)
        json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
        for dic in json_list:
            dataset_entry.objects.get_or_create(**dic)
        dataset_object=form.save()
        context['form']=dataset_form()
        context['created']=True
    return render(request,"enter_data.html", context)

def dataset_explore_view(request):
    form=mutiple_choice_form(request.POST or None)
    context={"form":form}
    if form.is_valid():
        context['form']=mutiple_choice_form()
        context['created']=True
        dataset_id=form.cleaned_data['datasets']
        dataset_name=dataset_model.objects.get(pk=dataset_id) 
        dataset=dataset_entry.objects.filter(article_dataset__lte=dataset_name).values()
        df = pd.DataFrame(dataset)
        text=" ".join(list(df["articles_lemmes"].str.lower()))
        fig=create_wordcloud(text).figure
        uri=generate_uri(fig)
        context["wordcloud"]=uri
        fig_2D,fig_3D=create_VIZ_PCA(df)
        uri=generate_uri(fig_2D)
        context["fig_2D"]=uri
        uri=generate_uri(fig_3D)
        context["fig_3D"]=uri

    return render(request,"explore.html", context)

    

def enter_data(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        path = str(request.POST.get('dataset_path'))
        name= str(request.POST.get('dataset_name'))
        # if not(dataset.objects.filter(item=path).exists()):
        #     dataset.objects.create(item=path)

        return JsonResponse({'data': path}, 
                            safe=False)

    



