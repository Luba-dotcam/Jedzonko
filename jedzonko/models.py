from django.db import models



# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    preparation_time = models.PositiveIntegerField()
    votes = models.IntegerField(default=0)

    @classmethod
    def get_total_count(cls):
        return cls.objects.count()