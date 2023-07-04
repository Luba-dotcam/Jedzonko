from random import shuffle
from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Recipe, Plan


from jedzonko.models import Recipe

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
            recipes_count = Recipe.objects.count()
            return render(request, template_name='dashboard.html', context={'recipes_count': recipes_count})


class RecipeView(View):
    def get(self, request):
        recipes_list = Recipe.objects.all().order_by('-votes', '-created').values()
        # definicja stronicowania, przekazujemy pobrane elementy oraz liczbę elementów na stronę
        paginator = Paginator(recipes_list, 50)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "app-recipes.html", context={'recipes': recipes})

      
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

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name != '' and description != '':
            plan = Plan.objects.create(
                name=name,
                description=description
            )
            return redirect('plan-details', plan.id)
        else:
            return render(request, 'app-add-schedules.html',
                          context={'error': 'Wszystkie pola muszą zostać uzupełnione'}
                          )


class PlanAddRecipeView(View):
    def get(self, request):
        return render(request, 'app-schedules-meal-recipe.html')


class PlanView(View):
    def get(self, request):
        return render(request, 'app-schedules.html')
