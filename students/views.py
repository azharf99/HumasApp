from typing import Any
from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from pandas import read_csv, read_excel
from alumni.forms import CSVFilesForm, FilesForm
from alumni.models import CSVFiles, Files
from students.models import Student, Class
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from students.forms import ClassUpdateForm, StudentUpdateForm
from userlog.models import UserLog
from utils.whatsapp import send_WA_create_update_delete
from numpy import int8

# Class Controllers
class ClassIndexView(ListView):
    model = Class

class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    form_class = ClassUpdateForm

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
                app="CLASS",
                message=f"berhasil menambahkan data kelas {self.obj}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data kelas {self.obj}', 'students/', 'class/')
        messages.success(self.request, "Input Data Berhasil! :)")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c

class ClassDetailView(LoginRequiredMixin, DetailView):
    model = Class

class ClassUpdateView(LoginRequiredMixin, UpdateView):
    model = Class
    form_class = ClassUpdateForm

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
                app="CLASS",
                message=f"berhasil update data kelas {self.obj}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'update', f'data kelas {self.obj}', 'students/', 'class/')
        messages.success(self.request, "Update Data Berhasil! :)")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = Class
    success_url = reverse_lazy("student:class-index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="DELETE",
                app="CLASS",
                message=f"berhasil menghapus data kelas {self.obj}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'data kelas {self.obj}', 'students/', 'class/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)


# Student Controllers
class StudentIndexView(ListView):
    model = Student

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentUpdateForm

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
                app="STUDENT",
                message=f"berhasil menambahkan data santri {self.obj}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data santri {self.obj}', 'students/')
        messages.success(self.request, "Input Data Berhasil! :)")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c
    

class StudentQuickUploadView(LoginRequiredMixin, CreateView):
    model = Files
    form_class = FilesForm
    template_name = 'students/student_form.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        df = read_excel(self.object.file, na_filter=False, dtype={"NIS": str, "NISN": str, "NOMOR_HP": str, "KELAS": int8})
        row, _ = df.shape
        for i in range(row):
            try:
                Student.objects.update_or_create(
                    nis = df.iloc[i, 0],
                    nisn = df.iloc[i, 1],
                    nama_siswa = df.iloc[i, 2],
                    defaults=dict(
                        kelas = Class.objects.get(pk=df.iloc[i, 3]),
                        jenis_kelamin = df.iloc[i, 4],
                        alamat = df.iloc[i, 5],
                        tempat_lahir = df.iloc[i, 6],
                        tanggal_lahir = df.iloc[i, 7],
                        email = df.iloc[i, 8],
                        nomor_hp = df.iloc[i, 9],
                        status = df.iloc[i, 10],
                        foto = df.iloc[i, 11],
                    )
                )
            except:
                messages.error(self.request, "Data pada Excel TIDAK SESUAI FORMAT! Mohon sesuaikan dengan format yang ada. Hubungi Administrator jika kesulitan.")
                return HttpResponseRedirect(reverse("student:student-quick-create"))
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="CREATE",
                app="STUDENT",
                message="berhasil impor file Excel data santri"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'impor file Excel', 'data santri', 'students/')
        messages.success(self.request, "Import Data Excel Berhasil! :)")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Import Excel"
        return c
    

class StudentQuickCSVUploadView(LoginRequiredMixin, CreateView):
    model = CSVFiles
    form_class = CSVFilesForm
    template_name = 'students/student_form.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        df = read_csv(self.object.file, na_filter=False, dtype={"NIS": str, "NISN": str, "NOMOR_HP": str, "KELAS": int8})
        row, _ = df.shape
        for i in range(row):
            try:
                Student.objects.update_or_create(
                    nis = df.iloc[i, 0],
                    nisn = df.iloc[i, 1],
                    nama_siswa = df.iloc[i, 2],
                    defaults=dict(
                        kelas = Class.objects.get(pk=df.iloc[i, 3]),
                        jenis_kelamin = df.iloc[i, 4],
                        alamat = df.iloc[i, 5],
                        tempat_lahir = df.iloc[i, 6],
                        tanggal_lahir = df.iloc[i, 7],
                        email = df.iloc[i, 8],
                        nomor_hp = df.iloc[i, 9],
                        status = df.iloc[i, 10],
                        foto = df.iloc[i, 11],
                    )
                )
            except:
                messages.error(self.request, "Data pada CSV TIDAK SESUAI FORMAT! Mohon sesuaikan dengan format yang ada. Hubungi Administrator jika kesulitan.")
                return HttpResponseRedirect(reverse("student:student-quick-create-csv"))
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="CREATE",
                app="STUDENT",
                message="berhasil impor file CSV data santri"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'impor file CSV', 'data santri', 'students/')
        messages.success(self.request, "Import Data CSV Berhasil! :)")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Import Excel"
        return c
    

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentUpdateForm

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
                app="STUDENT",
                message=f"berhasil update data santri {self.obj}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'update', f'data santri {self.obj}', 'students/')
        messages.success(self.request, "Update Data Berhasil! :)")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student:student-index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini!")
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
                user=self.request.user.teacher,
                action_flag="DELETE",
                app="STUDENT",
                message=f"berhasil menghapus data santri {self.obj}"
            )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'data santri {self.obj}', 'students/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)