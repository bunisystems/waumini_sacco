from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.cache import cache

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('index')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			print("Working:", allowed_roles)
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return render(request, 'sacco/access.html')
		return wrapper_func
	return decorator

def clear_cache(view_func):
	def wrapper(request, *args, **kwargs):
		cache.clear()
		print("cache cleared")
		return view_func(request, *args, **kwargs)
	return wrapper
