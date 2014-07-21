from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponseForbidden

def user_passes_test_redirect_forbidden(test_func):
	"""
	Decorator for views that checks that the user passes the given test,
	redirecting to a forbidden page if necessary. The test should be a callable
	that takes the user object and returns True if the user passes.
	"""

	def decorator(view_func):
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			if test_func(request.user):
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponseForbidden('You do not have required group permission to view this page')
		return _wrapped_view
	return decorator


def group_required(*group_names):
	"""
	Decorator for views that checks that the user has required group, redirecting
	to the log-in page if necessary.
	"""

	def check_group(user):
		if user.is_authenticated():
			return bool(user.groups.filter(name__in=group_names))
		else:
			return False

	return user_passes_test_redirect_forbidden(check_group)
			
