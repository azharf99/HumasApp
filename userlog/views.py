from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from userlog.models import UserLog
from userlog.forms import UserlogCreateForm
from utils.whatsapp import send_WA_create_update_delete


# Create your views here.

class UserLogListView(LoginRequiredMixin, ListView):
    model = UserLog
    paginate_by = 50

class UserLogCreateView(LoginRequiredMixin, CreateView):
    model = UserLog
    form_class = UserlogCreateForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Input Data Gagal! :( Ada kesalahan input!")
        return super().form_invalid(form)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.obj = form.save(commit=False)
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="CREATE",
                app="USERLOG",
                message=f"Berhasil menambahkan log {self.obj}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'log {self.obj}', 'logs/')
        messages.success(self.request, "Input Data Berhasil! :)")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c


class UserLogDetailView(LoginRequiredMixin, DetailView):
    model = UserLog


class UserLogUpdateView(LoginRequiredMixin, UpdateView):
    model = UserLog
    form_class = UserlogCreateForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Update Data Gagal! :( Ada kesalahan input!")
        return super().form_invalid(form)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.obj = form.save(commit=False)
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="UPDATE",
                app="USERLOG",
                message=f"Berhasil update log {self.obj}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'update', f'log {self.obj}', 'logs/')
        messages.success(self.request, "Update Data Berhasil! :)")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c
    
class UserLogDeleteView(LoginRequiredMixin, DeleteView):
    model = UserLog

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="DELETE",
                app="USERLOG",
                message=f"Berhasil menghapus log {self.obj}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'log {self.obj}', 'logs/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)