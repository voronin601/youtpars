from django.db import models

# Create your models here.
class data(models.Model):
    name = models.CharField(max_length = 150)
    n = models.CharField(max_length = 100)
    date = models.CharField(max_length = 100)
    watch = models.IntegerField()
    ava = models.CharField(max_length = 300)

#data.objects.create(name = "test", n = 1, date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), watch = 1)