from random import shuffle
from datetime import datetime
from django.shortcuts import render
from django.views import View
from .models import Recipe

from jedzonko.models import Recipe, Plan, RecipePlan, DayName

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
        last_plan = Plan.objects.order_by('created').last()
        recipes_plan = RecipePlan.objects.all().filter(plan_id=last_plan.id).order_by('day_name_id', 'order')
        ctx = {'recipes_count': recipes_count,
               'last_plan': last_plan}
        ctx_last_plan = {}
        for recipe_plan in recipes_plan:
            # get a day
            day_name = DayName.objects.get(pk=recipe_plan.day_name_id)
            # get a recipe name
            recipe_name = Recipe.objects.get(pk=recipe_plan.recipe_id)
            # check day name
            if day_name.get_name_display() not in ctx_last_plan:
                # if day not exists
                # create key with name of day
                ctx_last_plan[day_name.get_name_display()] = {recipe_plan.order : {'meal': recipe_plan.meal_name,
                                                                        'recipe_name': recipe_name.name,
                                                                        'id_recipe': recipe_plan.recipe_id,}}
            else:
                # update values for day
                ctx_last_plan[day_name.get_name_display()].update({recipe_plan.order : {'meal': recipe_plan.meal_name,
                                                                        'recipe_name': recipe_name.name,
                                                                        'id_recipe': recipe_plan.recipe_id,}})
        ctx['plans'] = ctx_last_plan
        # print(ctx['plans'].keys())
        return render(request, template_name='dashboard.html', context=ctx)


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
        return render(request, 'app-schedules.html')
