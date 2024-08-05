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
from users.views import MyLoginView, MyLogoutView, MyProfileView, MyProfileUpdateView, UserCreateView, UserListView, UserUpdateView, UserDeleteView,\
                        UserDetailView, UserPasswordChangeView, UserPasswordChangeDoneView
from alumni.views import AlumniDashboardView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='app-index'),
    path('accounts/', UserListView.as_view(), name="user-list"),
    path('accounts/<int:pk>/', UserDetailView.as_view(), name="user-detail"),
    path('accounts/<int:pk>/password/', UserPasswordChangeView.as_view(), name="user-change-password"),
    path('accounts/password/done', UserPasswordChangeDoneView.as_view(), name="user-change-password-done"),
    path('accounts/create/', UserCreateView.as_view(), name="user-create"),
    path('accounts/update/<int:pk>/', UserUpdateView.as_view(), name="user-update"),
    path('accounts/delete/<int:pk>/', UserDeleteView.as_view(), name="user-delete"),
    path('accounts/login/', MyLoginView.as_view(), name="login"),
    path('accounts/profile/', MyProfileView.as_view(), name="profile"),
    path('accounts/profile/<int:pk>/', MyProfileUpdateView.as_view(), name="profile-update"),
    path('accounts/logout/', MyLogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls),
    path('alumni/', include("alumni.urls")),
    path('dashboard/', AlumniDashboardView.as_view(), name="dashboard"),
    path('login/', MyLoginView.as_view(), name="login"),
    path('private/', include("private.urls")),
    path('students/', include("students.urls")),
    path('teachers/', include("users.urls")),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
