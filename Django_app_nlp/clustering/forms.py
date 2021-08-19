
from django import forms
from .models import *
from manage_data.models import *
import json

class mutiple_choice_form_algo(forms.Form):
    datasets = forms.ChoiceField()
    ML_models=forms.ChoiceField()
    def __init__(self,*args,**kwargs):
        super(mutiple_choice_form_algo,self).__init__(*args,**kwargs)
        results=list((i[0],i[2]) for i in dataset_model.objects.values_list()) 
        ML_algos=[(0,'K-means')]
        self.fields['datasets'].choices =  results
        self.fields['ML_models'].choices=ML_algos

class mutiple_choice_form_args(forms.Form):
    arg_1 = forms.ChoiceField()
    def __init__(self,name,*args,**kwargs):
        super(mutiple_choice_form_args,self).__init__(*args,**kwargs)
        choices=[(i,i) for i in range(2,16)]+[(16,'auto')]
        self.fields['arg_1'].choices= choices
        self.fields['arg_1'].label = name