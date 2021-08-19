
from django import forms
from .models import *

class mutiple_choice_form(forms.Form):
    datasets = forms.ChoiceField()
    def __init__(self,*args,**kwargs):
        super(mutiple_choice_form,self).__init__(*args,**kwargs)
        results=list((i[0],i[2]) for i in dataset_model.objects.values_list()) 
        self.fields['datasets'].choices =  results

class dataset_form(forms.ModelForm):
    class Meta:
        model=dataset_model
        fields=['dataset_path','name']

    def clean(self):
        data=self.cleaned_data
        dataset_path=data.get("dataset_path")
        name=data.get("name")
        qs=dataset_model.objects.filter(dataset_path__icontains=dataset_path)
        if qs.exists():
            self.add_error("dataset_path",f"{dataset_path} est déjà utilisé")
        qs=dataset_model.objects.filter(name__icontains=name)
        if qs.exists():
            self.add_error("name",f"{name} est déjà utilisé")