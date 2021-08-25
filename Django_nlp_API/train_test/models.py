from django.db import models

class Algo(models.Model):
    algo_name=models.CharField(max_length=200)
    algo_type=models.CharField(max_length=200)
    dataset=models.CharField(max_length=200)
    def __str__(self):
        return str(self.algo_name)
    class Meta:
        ordering = ['algo_name']