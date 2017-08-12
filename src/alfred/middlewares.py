from re import compile
from datetime import datetime
from django.db import connection, reset_queries
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
	EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware(MiddlewareMixin):
	"""
	Middleware that requires a user to be authenticated to view any page other
	than LOGIN_URL. Exemptions to this requirement can optionally be specified
	in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
	you can copy from your urls.py).

	Requires authentication middleware and template context processors to be
	loaded. You'll get an error if they aren't.
	"""
	def process_request(self, request):
		assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
		if not request.user.is_authenticated():
			path = request.path_info.lstrip('/')
			if not any(m.match(path) for m in EXEMPT_URLS):
				return HttpResponseRedirect(settings.LOGIN_URL)


class QueryAnalyticsMiddleware(object):


	def __init__(self):
		super(self.__class__, self).__init__()
		self.__reset()

	def __reset(self):
		self.start = None
		self.end = None
		self.time_taken = 0
		self.queries = 0
		reset_queries()

	def __log(self, request):
		if self.start and self.end:
			self.time_taken = self.end - self.start
			qa_string = "[%s] - %s - %s "
			qa_string += "query" if self.queries == 1 else "queries"
			qa_string += " - %ss"
			print qa_string % (
				request.method,
				request.path,
				self.queries,
				self.time_taken.total_seconds()
			)
		else:
			qa_string = "[%s] - %s - Time cannot be recorded, "
			qa_string += "query" if self.queries == 1 else "queries"
			qa_string += " - %ss"
			print qa_string % (
				request.method,
				request.path,
				self.queries
			)

	def process_request(self, request):
		self.start = datetime.now()
		self.queries = len(connection.queries)
		return None

	def process_response(self, request, response):
		self.end = datetime.now()
		self.queries = len(connection.queries)
		self.__log()
		self.__reset()
		return response
