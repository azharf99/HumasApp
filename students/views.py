from typing import Any
from django.forms import BaseModelForm

from django.http import HttpResponse, HttpResponseRedirect
from pandas import read_csv, read_excel
from alumni.forms import CSVFilesForm, FilesForm
from alumni.models import CSVFiles, Files
from students.models import Student, Class
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from students.forms import ClassUpdateForm, StudentUpdateForm

# Class Controllers
class ClassIndexView(ListView):
    model = Class

class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    form_class = ClassUpdateForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c

class ClassDetailView(LoginRequiredMixin, DetailView):
    model = Class

class ClassUpdateView(LoginRequiredMixin, UpdateView):
    model = Class
    form_class = ClassUpdateForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = Class


# Student Controllers
class StudentIndexView(ListView):
    model = Student

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentUpdateForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        return c
    

class StudentQuickUploadView(LoginRequiredMixin, CreateView):
    model = Files
    form_class = FilesForm
    template_name = 'students/student_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        df = read_excel(self.object.file, na_filter=False, dtype={"NIS": str, "NISN": str, "NOMOR_HP": str})
        row, _ = df.shape
        for i in range(row):
            Student.objects.update_or_create(
                nis = df.iloc[i, 0],
                nisn = df.iloc[i, 1],
                nama_siswa = df.iloc[i, 2],
                defaults=dict(
                    kelas = df.iloc[i, 0],
                    jenis_kelamin = df.iloc[i, 1],
                    alamat = df.iloc[i, 2],
                    tempat_lahir = df.iloc[i, 3],
                    tanggal_lahir = df.iloc[i, 4],
                    email = df.iloc[i, 5],
                    nomor_hp = df.iloc[i, 7],
                    status = df.iloc[i, 8],
                    foto = df.iloc[i, 9],
                )
            )
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Import Excel"
        return c
    

class StudentQuickCSVUploadView(LoginRequiredMixin, CreateView):
    model = CSVFiles
    form_class = CSVFilesForm
    template_name = 'students/student_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        df = read_csv(self.object.file, na_filter=False, dtype={"NIS": str, "NISN": str, "NOMOR_HP": str})
        row, _ = df.shape
        for i in range(row):
            Student.objects.update_or_create(
                nis = df.iloc[i, 0],
                nisn = df.iloc[i, 1],
                nama_siswa = df.iloc[i, 2],
                defaults=dict(
                    kelas = df.iloc[i, 0],
                    jenis_kelamin = df.iloc[i, 1],
                    alamat = df.iloc[i, 2],
                    tempat_lahir = df.iloc[i, 3],
                    tanggal_lahir = df.iloc[i, 4],
                    email = df.iloc[i, 5],
                    nomor_hp = df.iloc[i, 7],
                    status = df.iloc[i, 8],
                    foto = df.iloc[i, 9],
                )
            )
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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student