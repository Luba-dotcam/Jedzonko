from random import shuffle
from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from .models import Recipe, Plan

from jedzonko.models import Recipe

class IndexView(View):
  
    def get(self, request):
        recipes_all = list(Recipe.objects.all())
        shuffle(recipes_all)
        total_count = len(recipes_all)
        ctx = {"actual_date": datetime.now(),
           'total_count': total_count,
           'recipes_1_name': recipes_all[0].name,
           'recipes_1_description': recipes_all[0].description,
           'recipes_2_name': recipes_all[1].name,
           'recipes_2_description': recipes_all[1].description,
           'recipes_3_name': recipes_all[2].name,
           'recipes_3_description': recipes_all[2].description
           }
        return render(request, "index.html", ctx)


class DashboardView(View):
    plan_count = Plan.objects.count()
        recipes_count = Recipe.objects.count()
        context = {
            'plan_count': plan_count,
            'recipes_count': recipes_count
        }
        return render(request, 'dashboard.html', context=context)


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
        description_preparing = request.POST.get('description_preparing')
        if (name != '' and
            description != '' and
            preparation_time != '' and
            description_preparing != '' and
            ingredients != ''):
            Recipe.objects.create(name=name,
                                  description=description,
                                  ingredients=ingredients,
                                  description_preparing=description_preparing,
                                  preparation_time=preparation_time,
                                  votes=0)
            return redirect('recipe-list')
        else:
            return render(request, template_name='app-add-recipe.html',
                          context={'error': 'Wszystkie pola muszą zostać uzupełnione'}
                          )
      
class RecipeDetailsView(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        return render(request, 'app-recipe-details.html', context={"recipe": recipe})


class RecipeModifyView(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        return render(request, 'app-edit-recipe.html', context={"recipe": recipe})


class PlanDetailsView(View):
    def get(self, request, plan_id):
        plan = Plan.objects.get(id=plan_id)
        return render(request, 'app-details-schedules.html', context={"plan": plan})


class PlanAddView(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')


class PlanAddRecipeView(View):
    def get(self, request):
        return render(request, 'app-schedules-meal-recipe.html')


class PlanView(View):
    def get(self, request):
        return render(request, 'app-schedules.html')
