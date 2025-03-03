"""
URL configuration for HumasApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import ListView
from galleries.models import Gallery

from .views import DashboardView

class IndexView(ListView):
    model = Gallery

urlpatterns = [
    path('', IndexView.as_view(template_name="index.html"), name='app-index'),
    path('accounts/', include("users.urls")),
    path('admin/', admin.site.urls),
    path('alumni/', include("alumni.urls")),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('logs/', include("userlog.urls")),
    path('private/', include("private.urls")),
    path('students/', include("students.urls")),
    path('tahfidz/', include("tahfidz.urls")),
    path('galleries/', include("galleries.urls")),
]

if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
