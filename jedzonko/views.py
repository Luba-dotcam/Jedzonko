from random import shuffle
from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.core.paginator import Paginator
from jedzonko.models import Recipe, Plan, RecipePlan, DayName



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
    def get(self, request):
        plan_count = Plan.objects.count()
        recipes_count = Recipe.objects.count()
        last_plan = Plan.objects.order_by('created').last()
        recipes_plan = RecipePlan.objects.filter(plan_id=last_plan.id).order_by('day_name_id', 'order')
        ctx = {'plan_count': plan_count,
               'recipes_count': recipes_count,
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
                          context={'error': 'Wszystkie pola muszą zostać uzupełnione'})
          
          
class RecipeDetailsView(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        ingredients = recipe.ingredients.split(',')
        return render(request, 'app-recipe-details.html', context={"recipe": recipe, 'ingredients': ingredients})

    def post(self, request, recipe_id):
        r_id = request.POST.get('recipe_id')
        recipe = Recipe.objects.get(pk=r_id)
        if 'increase_button' in request.POST:
            recipe.votes += 1
        elif 'decrease_button' in request.POST:
            recipe.votes -= 1
        recipe.save()
        return redirect('recipe-details', recipe.id)

class RecipeModifyView(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        return render(request, 'app-edit-recipe.html', context={"recipe": recipe})


class PlanDetailsView(View):
    def get(self, request, plan_id):
        plan = Plan.objects.get(id=plan_id)
        day_names = DayName.objects.order_by('order')
        recipe_plans = plan.recipeplan_set.all().order_by('day_name__order', 'order')
        return render(request, 'app-details-schedules.html',
                      context={"plan": plan, 'day_names': day_names, 'recipe_plans': recipe_plans})


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
        plans = Plan.objects.order_by('name')
        recipes = Recipe.objects.order_by('name')
        days = DayName.objects.order_by('order')
        return render(request, 'app-schedules-meal-recipe.html', context={'plans': plans,
                                                                          'recipes': recipes,
                                                                          'days': days,
                                                                          })

    def post(self, request):
        meal_name = request.POST.get('meal_name')
        order = request.POST.get('order')
        day_name_id = request.POST.get('day_name_id')
        plan_id = request.POST.get('plan_id')
        recipe_id = request.POST.get('recipe_id')
        if plan_id != '' and meal_name != '' and order != '' and recipe_id != '' and day_name_id != '':
            RecipePlan.objects.create(
                meal_name=meal_name,
                order=order,
                day_name_id=day_name_id,
                plan_id=plan_id,
                recipe_id=recipe_id
            )
            return redirect('plan-details', plan_id)
        return redirect('plan-add-recipe')


class PlanView(View):
    def get(self, request):
        plans = Plan.objects.order_by('name')
        paginator = Paginator(plans, 50)
        page_number = request.GET.get('page')
        plans = paginator.get_page(page_number)
        return render(request, 'app-schedules.html', {'plans': plans})
