from django.shortcuts import redirect

""" 
A decorator used to block users who are not logged-in from accessing pages
which require logged-in users
"""


def login_prohibited(view_function):
    def modified_view_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_url = redirect('general')
            return redirect(redirect_url)
        else:
            return view_function(request, *args, **kwargs)

    return modified_view_function


"""
A decorator used to allow only the users who belong to one of the groups
given in the parameter list to access the page
"""


def allowed_groups(allowed_groups_names=[]):
    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            group = request.user.get_group()
            # Take user to the page if they are allowed
            if group in allowed_groups_names:
                return view_function(request, *args, **kwargs)
            # else take them to their default page
            else:
                return redirect('login')
        return wrapper
    return decorator
