from datetime import datetime

from django.shortcuts import render
from django.views import View
from random import shuffle

from jedzonko.models import Recipe

class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


class DashboardView(View):

    def get(self, request):
        return render(request, template_name='dashboard.html')


class RecipeView(View):
    def get(self, request):
        return render(request, "app-recipes.html")


class RecipeAddView(View):
    def get(self, request):
        return render(request, template_name='app-add-recipe.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        ingredients = request.POST.get('ingredients')
        # code below "to unlock later"
        # descritpion_preparing = request.POST.get('descritpion_preparing')

        Recipe.objects.create(name=name,
                              description=description,
                              ingredients=ingredients,
                              preparation_time=preparation_time,
                              votes=0)
        return render(request, template_name='app-add-recipe.html')
