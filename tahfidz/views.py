from typing import Any
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from pandas import read_csv, read_excel
from utils.mixins import GeneralAuthPermissionMixin, GeneralContextMixin, GeneralFormDeleteMixin, GeneralFormValidateMixin
from alumni.forms import CSVFilesForm, FilesForm
from alumni.models import CSVFiles, Files
from students.models import Student
from tahfidz.models import Tahfidz
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from tahfidz.forms import TahfidzForm
from userlog.models import UserLog
from utils.whatsapp_albinaa import send_WA_create_update_delete
from numpy import int8


# Tahfidz Controllers
class TahfidzIndexView(GeneralContextMixin, ListView):
    model = Tahfidz

class TahfidzCreateView(GeneralFormValidateMixin, CreateView):
    model = Tahfidz
    form_class = TahfidzForm
    form_name = "Create"
    app_name = "Tahfidz"
    type_url = 'tahfidz/'
    permission_required = 'tahfidz.add_tahfidz'

class TahfidzQuickUploadView(GeneralAuthPermissionMixin, CreateView):
    model = Files
    form_class = FilesForm
    permission_required = 'tahfidz.add_tahfidz'
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
                        pembimbing = df.iloc[i, 6],
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
    

class TahfidzQuickCSVUploadView(GeneralAuthPermissionMixin, CreateView):
    model = CSVFiles
    form_class = CSVFilesForm
    permission_required = 'tahfidz.add_tahfidz'
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
                        pembimbing = df.iloc[i, 6],
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
        c["form_name"] = "Import CSV"
        return c
    

class TahfidzDetailView(GeneralAuthPermissionMixin, DetailView):
    model = Tahfidz
    permission_required = 'tahfidz.view_tahfidz'

class TahfidzUpdateView(GeneralFormValidateMixin, UpdateView):
    model = Tahfidz
    form_class = TahfidzForm
    form_name = "Update"
    app_name = "Tahfidz"
    type_url = 'tahfidz/'
    permission_required = 'tahfidz.change_tahfidz'

class TahfidzDeleteView(GeneralFormDeleteMixin):
    model = Tahfidz
    success_url = reverse_lazy("tahfidz:tahfidz-index")
    app_name = "Tahfidz"
    type_url = 'tahfidz/'
    permission_required = 'tahfidz.delete_tahfidz'