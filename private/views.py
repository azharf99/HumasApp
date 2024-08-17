from typing import Any
from django.conf import settings
from django.contrib import messages
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from private.models import Private, Subject
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from private.forms import PrivateUpdateForm, SubjectUpdateForm
from userlog.models import UserLog
from utils.whatsapp import send_WA_create_update_delete
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.utils import timezone


# Private Controllers
class PrivateIndexView(ListView):
    model = Private

class PrivateCreateView(LoginRequiredMixin, CreateView):
    model = Private
    form_class = PrivateUpdateForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="CREATE",
            app="PRIVATE",
            message=f"berhasil menambahkan data privat {self.object}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data privat {self.object}', 'private/')
        messages.success(self.request, "Input Laporan Berhasil!")
        return HttpResponseRedirect(self.get_success_url())
    
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
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="UPDATE",
            app="PRIVATE",
            message=f"berhasil mengubah data privat {self.object}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'mengubah', f'data privat {self.object}', 'private/')
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
    success_url = reverse_lazy("private:private-index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.get_object().pembimbing == request.user.teacher or request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="DELETE",
            app="USERS",
            message=f"berhasil menghapus data privat {self.obj}",
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
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.obj = form.save(commit=False)
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="CREATE",
            app="SUBJECT",
            message=f"berhasil menambahkan data mapel {self.obj}",
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
        raise PermissionDenied
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.obj = form.save(commit=False)
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="UPDATE",
            app="SUBJECT",
            message=f"berhasil update data mapel {self.obj}",
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
    success_url = reverse_lazy("private:subject-index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="DELETE",
            app="SUBJECT",
            message=f"berhasil menghapus data mapel {self.obj}",
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'data mapel {self.obj}', 'private/', 'subjects/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)
    


class PrivatePrintView(LoginRequiredMixin, ListView):
    model = Private
    template_name = 'private/private_print.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        return Private.objects.filter(tanggal_bimbingan__month=timezone.now().month, tanggal_bimbingan__year=timezone.now().year).values("pembimbing__nama_guru").annotate(dcount=Count("pelajaran"))
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        MONTHS = {
            1: "Januari",
            2: "Februari",
            3: "Maret",
            4: "April",
            5: "Mei",
            6: "Juni",
            7: "Juli",
            8: "Agustus",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Desember",
        }
        c["tahun_ajaran"] = settings.TAHUN_AJARAN
        c["bulan_privat"] = MONTHS.get(timezone.now().month)
        c["jumlah_privat"] = Private.objects.filter(tanggal_bimbingan__month=timezone.now().month, tanggal_bimbingan__year=timezone.now().year).all()
        return c
    