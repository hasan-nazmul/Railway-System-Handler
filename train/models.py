from django.db import models

# Create your models here.
class Train(models.Model):
    departure = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    train_name = models.CharField(max_length=50)
    departure_time = models.TimeField()
    train_image = models.ImageField(upload_to='train_images/', default='default.jpg')