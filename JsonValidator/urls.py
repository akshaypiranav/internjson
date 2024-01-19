#INTERN AKSHAY PIRANAV B
#@akshaypiranavb@gmail.com
from django.contrib import admin
from django.urls import path
from APP import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home")
]
