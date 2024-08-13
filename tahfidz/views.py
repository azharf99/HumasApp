from typing import Any
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from pandas import read_csv, read_excel
from alumni.forms import CSVFilesForm, FilesForm
from alumni.models import CSVFiles, Files
from students.models import Student
from tahfidz.models import Tahfidz
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from tahfidz.forms import TahfidzForm
from userlog.models import UserLog
from utils.whatsapp import send_WA_create_update_delete
from numpy import int8


# Tahfidz Controllers
class TahfidzIndexView(ListView):
    model = Tahfidz

class TahfidzCreateView(LoginRequiredMixin, CreateView):
    model = Tahfidz
    form_class = TahfidzForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Input Data Gagal! :( Ada kesalahan input!")
        return super().form_invalid(form)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="CREATE",
                app="TAHFIDZ",
                message=f"berhasil menambahkan data tahfidz santri {self.object}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data tahfidz santri {self.object}', 'tahfidz/')
        messages.success(self.request, "Input Data Berhasil! :)")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c
    

class TahfidzQuickUploadView(LoginRequiredMixin, CreateView):
    model = Files
    form_class = FilesForm
    template_name = 'tahfidz/tahfidz_form.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        df = read_excel(self.object.file, na_filter=False, dtype={"NIS": str})
        row, _ = df.shape
        for i in range(row):
            try:
                Tahfidz.objects.update_or_create(
                    santri = Student.objects.get(nis=df.iloc[i, 0]),
                    defaults=dict(
                        hafalan = df.iloc[i, 2],
                        pencapaian_sebelumnya = df.iloc[i, 3],
                        pencapaian_sekarang = df.iloc[i, 4],
                        catatan = df.iloc[i, 5],
                    )
                )
            except:
                messages.error(self.request, "Data pada Excel TIDAK SESUAI FORMAT! Mohon sesuaikan dengan format yang ada. Hubungi Administrator jika kesulitan.")
                return HttpResponseRedirect(reverse("tahfidz:tahfidz-quick-create"))
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="CREATE",
                app="TAHFIDZ",
                message="berhasil impor file Excel data tahfidz santri"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'impor file Excel', 'data tahfidz santri', 'tahfidz/')
        messages.success(self.request, "Import Data Excel Berhasil! :)")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Import Excel"
        return c
    

class TahfidzQuickCSVUploadView(LoginRequiredMixin, CreateView):
    model = CSVFiles
    form_class = CSVFilesForm
    template_name = 'tahfidz/tahfidz_form.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        df = read_csv(self.object.file, na_filter=False, dtype={"NIS": str})
        row, _ = df.shape
        for i in range(row):
            try:
                Tahfidz.objects.update_or_create(
                    santri = Student.objects.get(nis=df.iloc[i, 0]),
                    defaults=dict(
                        hafalan = df.iloc[i, 2],
                        pencapaian_sebelumnya = df.iloc[i, 3],
                        pencapaian_sekarang = df.iloc[i, 4],
                        catatan = df.iloc[i, 5],
                    )
                )
            except:
                messages.error(self.request, "Data pada CSV TIDAK SESUAI FORMAT! Mohon sesuaikan dengan format yang ada. Hubungi Administrator jika kesulitan.")
                return HttpResponseRedirect(reverse("tahfidz:tahfidz-quick-create-csv"))
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="CREATE",
                app="STUDENT",
                message="berhasil impor file CSV data tahfidz santri"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'impor file CSV', 'data tahfidz santri', 'tahfidz/')
        messages.success(self.request, "Import Data CSV Berhasil! :)")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Import Excel"
        return c
    

class TahfidzDetailView(LoginRequiredMixin, DetailView):
    model = Tahfidz

class TahfidzUpdateView(LoginRequiredMixin, UpdateView):
    model = Tahfidz
    form_class = TahfidzForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Update Data Gagal! :( Ada kesalahan input!")
        return super().form_invalid(form)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="UPDATE",
                app="TAHFIDZ",
                message=f"berhasil update data tahfidz santri {self.object}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'update', f'data tahfidz santri {self.object}', 'tahfidz/')
        messages.success(self.request, "Update Data Berhasil! :)")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class TahfidzDeleteView(LoginRequiredMixin, DeleteView):
    model = Tahfidz
    success_url = reverse_lazy("tahfidz:tahfidz-index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="DELETE",
                app="STUDENT",
                message=f"berhasil menghapus data tahfidz santri {self.obj}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'data tahfidz santri {self.obj}', 'tahfidz/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)