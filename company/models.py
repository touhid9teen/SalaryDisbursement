from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    foundation_year = models.DateField()
    is_active = models.BooleanField(default=True)
    email = models.EmailField()
    website = models.URLField()
    discription = models.TextField()