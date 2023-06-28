from datetime import datetime

from django.shortcuts import render
from django.views import View


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

