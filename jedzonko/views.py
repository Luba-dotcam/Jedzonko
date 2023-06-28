from datetime import datetime

from django.shortcuts import render
from django.views import View
from .models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


class DashboardView(View):

    def get(self, request):
        if request.method == 'GET':
            recipes_count = Recipe.objects.count()
            return render(request, template_name='dashboard.html', context={'recipes_count': recipes_count})
        else:
            return render(request, template_name='dashboard.html')

class RecipeView(View):
    def get(self, request):
        return render(request, "app-recipes.html")

