from django.db import models

class Crime(models.Model):
    crime_type = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.crime_typ