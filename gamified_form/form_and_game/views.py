from django.shortcuts import render

# Create your views here.


def general_design(request):
    return render(request, 'a_form.html')
