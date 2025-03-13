from django.db import models


# Create your models here.
class USD(models.Model):
    Time = models.CharField(max_length=40)
    Value = models.FloatField()

    def __str__(self):
        return str(self.Value)
