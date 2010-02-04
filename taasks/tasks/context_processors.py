from datetime import datetime

from models import Project, Task, TaskInterval, TaskRegexp

def timer(request):
    print request.user.is_authenticated()
    if request.user.is_authenticated():
        today = datetime.now().date()
        duration = TaskInterval.get_hours(request.user, today)
        running = TaskInterval.is_running(request.user)
        info = dict(hours_today='%.2f' % duration, running=running)
        return dict(timer=info)
    return dict()
    