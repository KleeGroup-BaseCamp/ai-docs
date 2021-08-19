from django.db import models
from manage_data.models import *
class ML_model(models.Model):
    dataset_path = models.CharField(max_length=200)
    name= models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)
        
class CookBook(models.Model):
    RECIPES = (
            (0, 'Hamburger'),
            (1, 'Pancake'))
    recipe_name = models.IntegerField(default=0,
            choices=RECIPES)
    ingridients = models.CharField(max_length=1024)
