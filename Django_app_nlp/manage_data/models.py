from django.db import models



class dataset_model(models.Model):

    dataset_path = models.CharField(max_length=200)
    name= models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

class dataset_entry(models.Model):
    article_name=models.CharField(max_length=200)
    articles_nb_pages=models.IntegerField(default=0)
    articles_nb_text=models.IntegerField(default=0)
    article_text=models.TextField()
    articles_lemmes=models.TextField()
    article_class=models.CharField(max_length=200)
    articles_Non_Alphanumeric=models.IntegerField(default=0)
    article_dataset= models.CharField(max_length=200)
    def __str__(self):
        return str(self.article_name)
    class Meta:
        ordering = ['article_dataset']

