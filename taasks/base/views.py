import mimetypes
import os
import posixpath
import stat
import urllib

from django.http import (Http404, HttpResponse, HttpResponseRedirect,
    HttpResponseNotModified)
from django.template import Template, RequestContext
from django.utils.http import http_date
from django.views.static import was_modified_since

def serve_static(request, path, document_root):
    """Serve JS and CSS files as Django templates.
    Enables Django tag usage within templates. Meant to replace {% url %} tags.
    Mostly a copy of django.views.static.serve.
    """
    # Clean up given path to only allow serving files below document_root.
    path = posixpath.normpath(urllib.unquote(path))
    path = path.lstrip('/')
    newpath = ''
    for part in path.split('/'):
        if not part:
            # Strip empty path components.
            continue
        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # Strip '.' and '..' in path.
            continue
        newpath = os.path.join(newpath, part).replace('\\', '/')
    if newpath and path != newpath:
        return HttpResponseRedirect(newpath)
    fullpath = os.path.join(document_root, newpath)
    if os.path.isdir(fullpath):
        #if show_indexes:
        #    return directory_index(newpath, fullpath)
        raise Http404, "Directory indexes are not allowed here."
    if not os.path.exists(fullpath):
        raise Http404, '"%s" does not exist' % fullpath
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]):
        return HttpResponseNotModified()
    mimetype = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
    # Treat the file as a django template
    template = Template(open(fullpath, 'rb').read())
    context = RequestContext(request)
    # Render the template giving the current request
    contents = template.render(context)
    response = HttpResponse(contents, mimetype=mimetype)
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    response["Content-Length"] = len(contents)
    return response

