from django.db import models

# Create your models here.

class Bhavdata(models.Model):
    code = models.TextField()
    name = models.TextField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()

    def __str__(self):
        return self.name