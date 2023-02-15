"""gamified_form URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from form_and_game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('introduction_form/', views.introduction_form, name='introduction_form'),
    path('register_player/<sharer_code>/', views.register_player, name='register_player'),
    path('register_player/', views.register_player, name='register_player'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('introduction_form/slide_01/', views.introduction_form_functions.first_slide, name='introduction_form_slide_01'),
    path('introduction_form/slide_02/', views.introduction_form_functions.second_slide, name='introduction_form_slide_02'),
    path('introduction_form/slide_03/', views.introduction_form_functions.third_slide, name='introduction_form_slide_03'),
    path('introduction_form/slide_04/', views.introduction_form_functions.fourth_slide, name='introduction_form_slide_04'),
    path('introduction_form/slide_05/', views.introduction_form_functions.fifth_slide, name='introduction_form_slide_05'),
    path('introduction_form/slide_06/', views.introduction_form_functions.sixth_slide, name='introduction_form_slide_06'),
    path('introduction_form/slide_07/', views.introduction_form_functions.seventh_slide, name='introduction_form_slide_07'),
    path('introduction_form/conclusion_slide/',views.introduction_form_functions.conclusion_slide,name='introduction_form_conclusion_slide'),
    path('autres_form/',views.autres_form,name='autres_form'),
    path('game_home/',views.game_home,name='game_home'),
    path('conditions_generales/',views.conditions_generales,name='conditions_generales'),
    path('admin_home/',views.admin_page,name='admin_page'),
    path('',views.log_in,name='home'),
]
