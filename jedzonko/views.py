import random
from datetime import datetime
from django.views import View
from django.shortcuts import render
from .models import Recipe

class IndexView(View):
    def get(self, request):
        recipes_all = list(Recipe.objects.all())
        random.shuffle(recipes_all)
        ctx = {"actual_date": datetime.now(),
           'recipes_1_name': recipes_all[0].name,
           'recipes_1_description': recipes_all[0].description,
           'recipes_2_name': recipes_all[1].name,
           'recipes_2_description': recipes_all[1].description,
           'recipes_3_name': recipes_all[2].name,
           'recipes_3_description': recipes_all[2].description
           }
        return render(request, "index.html", ctx)

class RecipeView(View):
    def get(self, request):
        return render(request, "app-recipes.html")



