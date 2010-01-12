from django.http import Http404

def by_method(**handlers):
    """Call different functions on different HTTP methods.

Let's create our mock handlers

    >>> def get(request):
    ...     print 'get', request.method
    >>> def post(request):
    ...     print 'post', request.method

    >>> handler = by_method(GET=get, PUT=post, POST=post)

    >>> class Request:
    ...     pass
    >>> request = Request()

    >>> request.method = 'GET'
    >>> handler(request)
    get GET
    >>> request.method = 'PUT'
    >>> handler(request)
    post PUT
    >>> request.method = 'POST'
    >>> handler(request)
    post POST
    >>> request.method = 'DELETE'
    >>> handler(request)        # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    Http404: The requested resource for DELETE does not exist

    """
    def decorator(request, *args, **kwargs):
        handler = handlers.get(request.method)
        if handler is None:
            raise Http404('The requested resource for %s does not exist' % \
                request.method)
        else:
            return handler(request, *args, **kwargs)
    return decorator
