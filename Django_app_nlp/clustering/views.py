from django.shortcuts import render
from django.http import JsonResponse
from .forms import *
import pandas as pd
def clustering_create_view(request):
    form=mutiple_choice_form_algo(request.POST or None)
    context={"form":form}
    if form.is_valid():
        print(form.cleaned_data['datasets'])
        context['created']=True
        dataset_id=form.cleaned_data['datasets']
        dataset_name=dataset_model.objects.get(pk=dataset_id) 
        dataset=dataset_entry.objects.filter(article_dataset__lte=dataset_name).values()
        df = pd.DataFrame(dataset)
        print(df.head())

    return render(request,"clustering.html", context)

def clustering_results_create_view(request):
    return render(request,"clustering_results.html")

def home(request):
    return render(request, "home.html")


def compute(request):
    a = request.POST.get("a")
    b = request.POST.get("b")
    result = int(a) + int(b)
    return JsonResponse({"operation_result": result})