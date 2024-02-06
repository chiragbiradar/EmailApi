
from django.contrib import admin
from django.urls import path
from emailapp.views import sendemail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sendemail, name="sendemail"),
]
