"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin

from jedzonko.views import IndexView, RecipeView, DashboardView, RecipeDetailsView, RecipeAddView, RecipeModifyView, \
    PlanDetailsView, PlanAddView, PlanAddRecipeView, PlanView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('recipe/list/', RecipeView.as_view(), name='recipe_list'),
    path('main/', DashboardView.as_view()),
    path('recipe/<int:recipe_id>/', RecipeDetailsView.as_view(), name='recipe-details'),
    path('recipe/add/', RecipeAddView.as_view(), name='recipe-add'),
    path('recipe/modify/<int:id>/', RecipeModifyView.as_view(), name='recipe-modify'),
    path('plan/<int:plan_id>/', PlanDetailsView.as_view(), name='plan-details'),
    path('plan/add/', PlanAddView.as_view(), name='plan-add'),
    path('plan/add-receipe/', PlanAddRecipeView.as_view(), name='plan-add-recipe'),
    path('plan/list/', PlanView.as_view()),


]
