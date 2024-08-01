from django.core.handlers.wsgi import WSGIRequest
from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404, render
from userlog.models import UserLog
from django.views.generic import ListView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.db.models.query import QuerySet
from django.contrib import messages
from django.template.response import TemplateResponse
from users.models import Teacher
from users.forms import ProfileUpdateForm
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

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.kwargs.get("pk") != request.user.id:
            return HttpResponseForbidden("Maaf, anda tidak diizinkan mengubah data profil orang lain atau link yang anda masukan salah!")
        return super().get(request, *args, **kwargs)
    
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