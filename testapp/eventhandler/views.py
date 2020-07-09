from eventhandler.mailsender import main as event_check
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from eventhandler.models import User, Event
from django.http import HttpResponse
from dateutil.tz import tzlocal
import datetime
import random
import string
import pytz
import json

def get_user_from_session(request):
    if request:
        user_id = request.session.get("logged_user_id")
        if user_id != None:
            user = User.objects.get(id=user_id)
            return user

    return None

#main views
def reg(request):
    if len(request.POST) > 0:
        fname = request.POST.get("fname", None)
        sname = request.POST.get("sname", None)
        mail = request.POST.get("mail", None)
        password = request.POST.get("password", None)
        print(fname, sname, mail, password)
        if all((fname!="", sname!="", mail!="", password!="")):
            new_user = User(fname=fname, sname=sname, mail=mail, password=password)
            new_user.save()
            return redirect("/login")

    return render(request, "register.html")

def log(request):
    if len(request.POST) > 0:
        if "email" in request.POST and "password" in request.POST:
            email = request.POST["email"]
            password = request.POST["password"]
            print(email, password)
            try:
                user = User.objects.get(mail=email)
            except:
                return render(request, "login.html")
            if user.password == password:
                request.session["logged_user_id"] = user.id
                return redirect("/main")


    return render(request, "login.html")


def main(request):
    user_sess = get_user_from_session(request)
    if user_sess:
        user = User.objects.get(pk=user_sess.id)
        user_data = {
            "fname":user.fname,
            "sname":user.sname,
            "events":user.events.all().filter(completed=False).order_by("finish_date"),
            "events_completed":user.events.all().filter(completed=True).order_by("-finish_date"),
        }
        return render(request, "main.html", user_data)
    return redirect("/login")


#ajax executed

def is_datevalid(date):
    now_time = datetime.datetime.now(tzlocal())
    date_diff = relativedelta(date, now_time)
    print(now_time, date, date_diff)
    print(date_diff.years, date_diff.months, date_diff.days, date_diff.hours, date_diff.minutes, date_diff.seconds)
    if any(( date_diff.years < 0, date_diff.months < 0, date_diff.days<0, \
             date_diff.hours < 0, date_diff.minutes < 0, date_diff.seconds<0 )):
        print("denis")
        return False
    return True

def add_event(request):
    user = get_user_from_session(request)
    if user:
        if len(request.GET) > 0:
            title = request.GET.get("title", None)
            date = request.GET.get("date", None)
            time = request.GET.get("time", None)
            if all((title, date, time)):
                dt = f"{date} {time}"
                date_time = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")
                timezone_date_time = datetime.datetime(date_time.year, date_time.month, date_time.day, \
                                                       date_time.hour, date_time.minute, date_time.second, \
                                                       tzinfo=tzlocal())
                if is_datevalid(timezone_date_time):

                    url_id = ''.join(random.choice( string.ascii_letters+string.ascii_uppercase+string.digits) for _ in range(8) )
                    new_event = Event(title=title, finish_date=timezone_date_time, url=url_id, author_id=user.id)
                    new_event.save()

                    user.events.add(new_event)
                    user.save()

                    return render(request, "generatedEvent.html", {"event":new_event})
                else:
                    data = json.dumps({"error":"Please set a valid date"})
                    return HttpResponse(data, content_type="application/json")


            data = json.dumps({"error":"Plese give all event values"})
            return HttpResponse(data, content_type="application/json")

        data = json.dumps({"erorr":"Some problems with your session"})
        return HttpResponse(data, content_type="application/json")

    return redirect("/login")


def remove_event(request):
    user = get_user_from_session(request)
    if user:
        if len(request.GET) > 0:
            event_url = request.GET.get("event_url", None)
            if event_url:
                event = Event.objects.get(url=event_url)
                event.delete()
                data = json.dumps({"resp":True, "event_url":event_url})
                return HttpResponse(data, content_type="application/json")

            data = json.dumps({"error":"Some problems with request"})
            return HttpResponse(data, content_type="application/json")

        data = json.dumps({"erorr":"Some problems with your session"})
        return HttpResponse(data, content_type="application/json")

def update_event(request):
    user = get_user_from_session(request)
    if user:
        if len(request.GET) > 0:
            title = request.GET.get("title", None)
            date = request.GET.get("date", None)
            time = request.GET.get("time", None)
            event_url = request.GET.get("event_url", None)

            if all((title, date, time, event_url)):
                dt = f"{date} {time}"
                date_time = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")
                timezone_date_time = datetime.datetime(date_time.year, date_time.month, date_time.day, \
                                                       date_time.hour, date_time.minute, date_time.second, \
                                                       tzinfo=tzlocal())
                if is_datevalid(date_time):

                    event_to_update = Event.objects.get(url=event_url)
                    event_to_update.title = title
                    event_to_update.finish_date = timezone_date_time
                    event_to_update.save()
                    data = json.dumps({"resp":True, "event_url":event_url})

                    return HttpResponse(data, content_type="application/json")
                else:
                    data = json.dumps({"resp":False, "error":"Please set a valid date"})
                    return HttpResponse(data, content_type="application/json")

            data = json.dumps({"resp":False, "error":"Plesea give all event values"})
            return HttpResponse(data, content_type="application/json")

        data = json.dumps({"resp":False, "erorr":"Some problems with your session"})
        return HttpResponse(data, content_type="application/json")

def get_events_by_period(request):
    user = get_user_from_session(request)
    if user:
        if len(request.GET) > 0:
            print("req")
            period = request.GET.get("period", None)
            if period:
                print("per")

                user_events = Event.objects.filter(author_id=user.id)
                today = datetime.datetime.today()
                if period == "daily":
                    period_posted_events = user_events.filter(added_date__range=(today, today))
                elif period == "weekly":
                    a_week_ago = today - relativedelta(days=7)
                    period_posted_events = user_events.filter(added_date__range=(a_week_ago,today))
                elif period == "monthly":
                    a_month_ago = today - relativedelta(months=1)
                    period_posted_events = user_events.filter(added_date__range=(a_month_ago, today))
                else:
                    period_posted_events = user_events

                return render(request, "listbyPeriod.html", {"events": period_posted_events.filter(completed=False), "events_completed": period_posted_events.filter(completed=True)})

        data = json.dumps({"resp":False, "error":"Some problems with request"})
        return HttpResponse(data, content_type="application/json")

    data = json.dumps({"resp":False, "erorr":"Some problems with your session"})
    return HttpResponse(data, content_type="application/json")

def find_events(request):
    user = get_user_from_session(request)
    if user:
        if len(request.GET) > 0:
            find_query = request.GET.get("event_query", None)
            if find_query:
                finded_events = Event.objects.filter(title__contains=find_query)
                return render(request, "listbyPeriod.html", {"events": finded_events.filter(completed=False), "events_completed": finded_events.filter(completed=True)})
            else:
                data = json.dumps({"resp":False, "error":"Invalid find query"})
                return HttpResponse(data, content_type="application/json")

        data = json.dumps({"resp":False, "error":"Some problems with request"})
        return HttpResponse(data, content_type="application/json")

    data = json.dumps({"resp":False, "erorr":"Some problems with your session"})
    return HttpResponse(data, content_type="application/json")

event_check.check_events()
