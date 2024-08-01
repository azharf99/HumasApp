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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from users.views import MyLoginView, MyLogoutView, MyProfileView, MyProfileUpdateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='app-index'),
    path('admin/', admin.site.urls),
    path('alumni/', include("alumni.urls")),
    path('login/', MyLoginView.as_view(), name="login"),
    path('accounts/login/', MyLoginView.as_view(), name="login"),
    path('accounts/profile/', MyProfileView.as_view(), name="profil"),
    path('accounts/profile/<int:pk>/', MyProfileUpdateView.as_view(), name="profil-edit"),
    path('accounts/profile/<int:pk>/', MyProfileUpdateView.as_view(), name="password-edit"),
    path('accounts/logout/', MyLogoutView.as_view(), name="logout"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
