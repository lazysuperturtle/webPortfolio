from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from eventhandler import views as eventapp


urlpatterns = [
    path('admin/', admin.site.urls),
    url("^$", eventapp.log),
    url("^register$", eventapp.reg),
    url("^login$", eventapp.log),
    url("^main$", eventapp.main),
    url("^ajax/addEvent$", eventapp.add_event),
    url("^ajax/updateEvent$", eventapp.update_event),
    url("^ajax/deleteEvent$", eventapp.remove_event),
    url("^ajax/sortByPeriod$", eventapp.get_events_by_period),
    url("^ajax/findEvent$", eventapp.find_events),
]
