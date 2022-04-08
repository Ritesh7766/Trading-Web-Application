# Custom decorators
from functools import wraps


def logout_required(current_user, redirect):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If user is already logged in redirect to home page.
            if current_user.is_authenticated:
                return redirect('/')
            return func(*args, **kwargs)
        return wrapper
    return decorate


def login_required(current_user, redirect):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If user is not logged in redirect to home page.
            if not current_user.is_authenticated:
                return redirect('/')
            return func(*args, **kwargs)
        return wrapper
    return decorate