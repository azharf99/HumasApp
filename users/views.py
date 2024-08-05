from django import http
from django.core.handlers.wsgi import WSGIRequest
from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from userlog.models import UserLog
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import urls
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.db.models.query import QuerySet
from django.contrib import messages
from django.template.response import TemplateResponse
from users.models import Teacher
from users.forms import ProfileUpdateForm, UserCreateForm, UserUpdateForm, UserPasswordUpdateForm
from utils.whatsapp import send_whatsapp_login
from typing import Any

# Create your views here.
class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    
    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        if self.request.POST.get("remember"):
            self.request.session.set_expiry(1209600)
        else:
           self.request.session.set_expiry(0)

        UserLog.objects.create(
                user=form.get_user().teacher,
                action_flag="LOGIN",
                app="EKSKUL",
                message="Berhasil melakukan login ke aplikasi"
            )
        send_whatsapp_login(form.get_user().teacher.no_hp, 'login', 'Selamat datang di Aplikasi PMBP')
        return super().form_valid(form)


class MyProfileView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.teacher.id == self.kwargs.get("pk") or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()
    
    def get_queryset(self) -> QuerySet[Any]:
        return get_object_or_404(Teacher, user_id=self.request.user.id)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['name'] = "Overview"
        return context

class MyProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = ProfileUpdateForm
    template_name = "registration/profile_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.teacher.id == self.kwargs.get("pk") or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['teacher'] = self.get_queryset()
        context['name'] = "Edit Profile"
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="CHANGE",
            app="PROFILE",
            message="Berhasil mengubah data diri di halaman profil",
        )
        return super().form_valid(form)

class MyLogoutView(LogoutView):

    def post(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> TemplateResponse:
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="LOGOUT",
            app="EKSKUL",
            message="Berhasil logout dari aplikasi",
        )
        send_whatsapp_login(request.user.teacher.no_hp, 'logout', 'Kami sedih anda tinggalkan :(, namun tidak apa-apa, jangan lupa kembali ya')
        return super().post(request, *args, **kwargs)
    

class UserListView(LoginRequiredMixin, ListView):
    model = User


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy("user-list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.id == self.kwargs.get("pk") or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()
    

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("user-list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.id == self.kwargs.get("pk") or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c
    

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("user-list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.id == self.kwargs.get("pk") or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordUpdateForm
    success_url = reverse_lazy("user-change-password-done")


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.id == self.kwargs.get("pk") or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = get_object_or_404(User, id=self.kwargs.get("pk"))
        return kwargs


class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name ="registration/password_change_done.html"
    

class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher


class TeacherCreateView(LoginRequiredMixin, CreateView):
    model = Teacher
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("teacher-list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    

class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("teacher-list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.teacher.id == self.kwargs.get("pk") or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c
    

class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    model = Teacher
    success_url = reverse_lazy("teacher-list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.teacher.id == self.kwargs.get("pk") or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()