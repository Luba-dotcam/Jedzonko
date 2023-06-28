from datetime import datetime

from django.shortcuts import render
from django.views import View

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




class RecipeDetailsView(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        context = {
            'recipe': recipe
        }
        return render(request, 'app-recipe-details.html', context)


class RecipeAddView(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')

class RecipeModifyView(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        context = {
            'recipe': recipe
        }
        return render(request, 'app-edit-recipe.html', context)


class PlanDetailsView(View):
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        context = {
            'plan': plan
        }
        return render(request, 'app-details-schedules.html.html', context)


class PlanAddView(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

class PlanAddRecipeView(View):
    def get(self, request):
        return render(request, 'app-schedules-meal-recipe.html')



