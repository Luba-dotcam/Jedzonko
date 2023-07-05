from random import shuffle
from datetime import datetime

from random import shuffle
from django.shortcuts import render
from django.views import View
from django.shortcuts import render
from .models import Recipe, Plan


class IndexView(View):
    def get(self, request):

        # ctx = {"actual_date": datetime.now()}
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
    def get(self, request):
        plan_count = Plan.objects.count()
        ctx = {
            'plan count': plan_count,
                   }
        return render(request, template_name='dashboard.html', context=ctx)

class RecipeView(View):
    def get(self, request):
        return render(request, "app-recipes.html")


class RecipeDetailsView(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        return render(request, 'app-recipe-details.html', context={"recipe": recipe})


class RecipeAddView(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')


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
