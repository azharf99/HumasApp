from typing import Any
from django.contrib import messages
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from private.models import Private, Subject
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from private.forms import PrivateUpdateForm, SubjectUpdateForm
from userlog.models import UserLog
from utils.whatsapp import send_WA_create_update_delete

# Private Controllers
class PrivateIndexView(ListView):
    model = Private

class PrivateCreateView(LoginRequiredMixin, CreateView):
    model = Private
    form_class = PrivateUpdateForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.obj = form.save(commit=False)
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="CREATE",
            app="PRIVATE",
            message=f"Berhasil menambahkan data privat {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data privat {self.obj}', 'private/')
        messages.success(self.request, "Input Laporan Berhasil!")
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Input Laporan Gagal! Ada yang salah salam pengisian. Mohon dicek ulang atau hubungi Administrator.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c

class PrivateDetailView(LoginRequiredMixin, DetailView):
    model = Private

class PrivateUpdateView(LoginRequiredMixin, UpdateView):
    model = Private
    form_class = PrivateUpdateForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.get_object().pembimbing == request.user.teacher or request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.obj = form.save(commit=False)
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="UPDATE",
            app="PRIVATE",
            message=f"Berhasil menambahkan data privat {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data privat {self.obj}', 'private/')
        messages.success(self.request, "Update Laporan Berhasil!")
        return HttpResponseRedirect(reverse("private:private-detail", kwargs={"pk": self.kwargs.get("pk")}))
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Update Laporan Gagal! Ada yang salah salam pengisian. Mohon dicek ulang atau hubungi Administrator.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class PrivateDeleteView(LoginRequiredMixin, DeleteView):
    model = Private

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.get_object().pembimbing == request.user.teacher or request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="DELETE",
            app="USERS",
            message=f"Berhasil menghapus data privat {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'data privat {self.obj}', 'private/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)


# Subject Controllers
class SubjectIndexView(ListView):
    model = Subject

class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectUpdateForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.obj = form.save(commit=False)
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="CREATE",
            app="SUBJECT",
            message=f"Berhasil menambahkan data mapel {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data mapel {self.obj}', 'private/', 'subjects/')
        messages.success(self.request, "Input Mapel Berhasil!")
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Input Mapel Gagal!")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c

class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject

class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectUpdateForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.obj = form.save(commit=False)
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="UPDATE",
            app="SUBJECT",
            message=f"Berhasil update data mapel {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'update', f'data mapel {self.obj}', 'private/', 'subjects/')
        messages.success(self.request, "Update Mapel Berhasil!")
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Update Mapel Gagal!")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="DELETE",
            app="SUBJECT",
            message=f"Berhasil menghapus data mapel {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'data mapel {self.obj}', 'private/', 'subjects/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)