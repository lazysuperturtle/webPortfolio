from dateutil.relativedelta import relativedelta
from testapp.settings import EMAIL_HOST_USER
from eventhandler.models import User, Event
from datetime import datetime, timedelta
from django.core.mail import send_mail
from dateutil.tz import tzlocal
from threading import Thread
import functools
import time
import pytz

def thread(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_thread = Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        new_thread.start()
        return new_thread
    return wrapper

@thread
def check_events():
    while True:
        objects = Event.objects.all().filter(completed=False)
        now = datetime.now(tzlocal())
        for event in objects:
            rest_time = relativedelta(event.finish_date, now)
            days, hours, minutes = rest_time.days, rest_time.hours, rest_time.minutes
            if days <= 0 and hours <= 0 and ( minutes <= 60 and minutes >= 59):
                user = User.objects.get(pk=event.author_id)
                user_mail = user.mail
                print("SEND")
                send_mail("Event notification", f"Your event {event.title} will be in an hour", EMAIL_HOST_USER, [user_mail], fail_silently=False )
                # print("Some error with email sending")
            elif days<=0 and hours<=0 and minutes<=0:
                event.completed = True
                event.save()
            else:
                pass

        time.sleep(30)

if __name__ == '__main__':
    check_events()
