from random import shuffle
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe, Plan


class IndexView(View):
  
    def get(self, request):
        recipes_all = list(Recipe.objects.all())
        shuffle(recipes_all)
        ctx = {"actual_date": datetime.now(),
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
        plans = Plan.objects.order_by('name')
        paginator = Paginator(plans, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'app-schedules.html', {'page_obj': page_obj})
