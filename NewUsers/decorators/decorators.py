from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps

def anonymous_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')
        else:
            return view_func(request, *args, **kwargs)
    return wrapped_view