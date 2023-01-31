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
    path('introduction_form/', views.general_design, name='general_for_now'),
    path('second_slide/', views.second_slide, name='second'),
    path('third_slide/', views.third_slide, name='third'),
    path('fourth_slide/', views.fourth_slide, name='fourth'),
    path('fifth_slide/', views.fifth_slide, name='fourth'),
    path('sixth_slide/', views.sixth_slide, name='six'),
    path('register_player/', views.register_player, name='register_player'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out')
]
