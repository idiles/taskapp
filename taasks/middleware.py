import traceback

from django.conf import settings
from django.http import HttpResponseServerError

class AJAXSimpleExceptionResponse:
    def process_exception(self, request, exception):
        if settings.DEBUG:
            if request.is_ajax():
                import sys, traceback
                (exc_type, exc_info, tb) = sys.exc_info()
                response = "%s\n" % exc_type.__name__
                response += "%s\n\n" % exc_info
                response += "TRACEBACK:\n"    
                for tb in traceback.format_tb(tb):
                    response += "%s\n" % tb
                return HttpResponseServerError(response)


# class ConsoleExceptionMiddleware:
#     def process_exception(self, request, exception):
#         import traceback
#         import sys
#         exc_info = sys.exc_info()
#         print '*' * 80
#         print '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
#         print '*' * 80


class WsgiLogErrors(object):
    def process_exception(self, request, exception):
        tb_text = traceback.format_exc()
        url = request.build_absolute_uri()
        request.META['wsgi.errors'].write(url + '\n' + str(tb_text) + '\n')


class ForceDefaultLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies

    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    def process_request(self, request):
        if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
            del request.META['HTTP_ACCEPT_LANGUAGE']
