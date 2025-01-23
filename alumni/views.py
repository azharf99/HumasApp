from io import BytesIO
from typing import Any
from django.core.exceptions import PermissionDenied
from django.forms import BaseModelForm
from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.urls import reverse, reverse_lazy
from alumni.models import Alumni, Files, CSVFiles
from alumni.forms import AlumniForm, FilesForm, CSVFilesForm
from django.utils import timezone
from utils.whatsapp import send_WA_create_update_delete, send_WA_general
from userlog.models import UserLog
from pandas import read_excel, read_csv
from xlsxwriter import Workbook

class AlumniDashboardView(ListView):
    model = Alumni
    template_name = 'alumni/alumni_dashboard.html'
    queryset = Alumni.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["jumlah_alumni_putra"] = self.queryset.filter(gender="L")
        c["jumlah_alumni_putri"] = self.queryset.filter(gender="P")
        c["jumlah_alumni_tahun_ini"] = self.queryset.filter(graduate_year=timezone.now().year)
        c["jumlah_alumni_putra_tahun_ini"] = self.queryset.filter(gender="L", graduate_year=timezone.now().year)
        c["jumlah_alumni_putri_tahun_ini"] = self.queryset.filter(gender="P", graduate_year=timezone.now().year)
        c["jumlah_alumni_universitas"] = self.queryset.filter(Q(undergraduate_university__isnull=False)|Q(postgraduate_university__isnull=False)|Q(doctoral_university__isnull=False))
        c["jumlah_alumni_putra_universitas"] = self.queryset.filter(Q(gender="L") & Q(undergraduate_university__isnull=False)|Q(postgraduate_university__isnull=False)|Q(doctoral_university__isnull=False))
        c["jumlah_alumni_putri_universitas"] = self.queryset.filter(Q(gender="P",) & Q(undergraduate_university__isnull=False)|Q(postgraduate_university__isnull=False)|Q(doctoral_university__isnull=False))
        c["logs"] = UserLog.objects.order_by("-created_at")[:10]
        c["sebaran_wilayah"] = Alumni.objects.values('city', 'province').annotate(dcount=Count('city'))
        c["sebaran_universitas_sarjana"] = self.queryset.exclude(undergraduate_university__in=[0, '']).values('undergraduate_university').annotate(dcount=Count('undergraduate_university')).order_by('-dcount')[:10]
        c["sebaran_universitas_magister"] = self.queryset.values('postgraduate_university').annotate(dcount=Count('postgraduate_university')).order_by()
        c["sebaran_universitas_doktoral"] = self.queryset.values('doctoral_university').annotate(dcount=Count('doctoral_university')).order_by()
        return c


class AlumniIndexView(ListView):
    model = Alumni
    paginate_by = 50



class AlumniSearchView(ListView):
    model = Alumni
    template_name = 'alumni/alumni_search.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        query = request.GET.get("query")
        queryset = None
        if query:
            data = Alumni.objects.filter(Q(nis__icontains=query)|
                                         Q(name__icontains=query)|
                                         Q(nisn__icontains=query)|
                                         Q(group__icontains=query)|
                                         Q(graduate_year__icontains=query)|
                                         Q(undergraduate_university__icontains=query))
            if len(data) > 0:
                messages.success(request, f"{len(data)} Data Berhasil Ditemukan!")
            else:
                messages.error(request, "Data Tidak Ditemukan!")
            queryset = data
        self.object_list = queryset
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["query"] = self.request.GET.get("query")
        return c


class AlumniCreateView(LoginRequiredMixin, CreateView):
    model = Alumni
    form_class = AlumniForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Input Data Gagal! :( Ada kesalahan input!")
        return super().form_invalid(form)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save(commit=False)
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = "CREATE",
            app = "ALUMNI",
            message = f"berhasil menambahkan data alumni atas nama {self.object.name} angkatan {self.object.group}"
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menambahkan', f'data alumni {self.object.name} angkatan {self.object.group}', 'alumni/')
        messages.success(self.request, "Update Data Berhasil! :)")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Create"
        c["query"] = self.request.GET.get("query")
        return c

class AlumniQuickUploadView(LoginRequiredMixin, CreateView):
    model = Files
    form_class = FilesForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save(commit=False)
        df = read_excel(self.object.file, na_filter=False, dtype={"NIS": str, "NISN": str, "HP/WA": str, "HP ORANG TUA": str})
        row, _ = df.shape
        try:
            for i in range(row):
                Alumni.objects.update_or_create(
                    name = df.iloc[i, 2],
                    group = df.iloc[i, 3],
                    defaults=dict(
                        nis = df.iloc[i, 0],
                        nisn = df.iloc[i, 1],
                        group = df.iloc[i, 3],
                        birth_place = df.iloc[i, 4],
                        birth_date = df.iloc[i, 5] or None,
                        gender = df.iloc[i, 6],
                        address = df.iloc[i, 7],
                        city = df.iloc[i, 8],
                        province = df.iloc[i, 9],
                        state = df.iloc[i, 10],
                        phone = df.iloc[i, 11],
                        last_class = df.iloc[i, 12],
                        graduate_year = df.iloc[i, 13],
                        undergraduate_department = df.iloc[i, 14],
                        undergraduate_university = df.iloc[i, 15],
                        undergraduate_university_entrance = df.iloc[i, 16],
                        postgraduate_department = df.iloc[i, 17],
                        postgraduate_university = df.iloc[i, 18],
                        postgraduate_university_entrance = df.iloc[i, 19],
                        doctoral_department = df.iloc[i, 20],
                        doctoral_university = df.iloc[i, 21],
                        doctoral_university_entrance = df.iloc[i, 22],
                        job = df.iloc[i, 23],
                        company_name = df.iloc[i, 24],
                        married = df.iloc[i, 25],
                        father_name = df.iloc[i, 26],
                        mother_name = df.iloc[i, 27],
                        family_phone = df.iloc[i, 28],
                        photo = df.iloc[i, 29],
                    )
                )
        except Exception as e:
            messages.error(self.request, f"Error: {e}.")
            return HttpResponseRedirect(reverse("alumni:alumni-quick-upload"))
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = "CREATE",
            app = "ALUMNI",
            message = f"berhasil impor data excel alumni"
        )
        messages.success(self.request, "Selamat, Impor data excel alumni berhasil!")
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'mengimpor dari excel', 'data alumni', 'alumni/')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Import Excel Alumni"
        return c
    

class AlumniCSVQuickUploadView(LoginRequiredMixin, CreateView):
    model = CSVFiles
    form_class = CSVFilesForm
    template_name = 'alumni/files_form.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save(commit=False)
        df = read_csv(self.object.file, na_filter=False, dtype={"NIS": str, "NISN": str, "HP/WA": str, "HP ORANG TUA": str})
        row, _ = df.shape
        try:
            for i in range(row):
                Alumni.objects.update_or_create(
                    nis = df.iloc[i, 0],
                    nisn = df.iloc[i, 1],
                    name = df.iloc[i, 2],
                    defaults=dict(
                        nis = df.iloc[i, 0],
                        nisn = df.iloc[i, 1],
                        name = df.iloc[i, 2],
                        group = df.iloc[i, 3],
                        birth_place = df.iloc[i, 4],
                        birth_date = df.iloc[i, 5],
                        gender = df.iloc[i, 6],
                        address = df.iloc[i, 7],
                        city = df.iloc[i, 8],
                        province = df.iloc[i, 9],
                        state = df.iloc[i, 10],
                        phone = df.iloc[i, 11],
                        last_class = df.iloc[i, 12],
                        graduate_year = df.iloc[i, 13],
                        undergraduate_department = df.iloc[i, 14],
                        undergraduate_university = df.iloc[i, 15],
                        undergraduate_university_entrance = df.iloc[i, 16],
                        postgraduate_department = df.iloc[i, 17],
                        postgraduate_university = df.iloc[i, 18],
                        postgraduate_university_entrance = df.iloc[i, 19],
                        doctoral_department = df.iloc[i, 20],
                        doctoral_university = df.iloc[i, 21],
                        doctoral_university_entrance = df.iloc[i, 22],
                        job = df.iloc[i, 23],
                        company_name = df.iloc[i, 24],
                        married = df.iloc[i, 25],
                        father_name = df.iloc[i, 26],
                        mother_name = df.iloc[i, 27],
                        family_phone = df.iloc[i, 28],
                        photo = df.iloc[i, 29],
                    )
                )
        except:
            messages.error(self.request, "Data pada Excel TIDAK SESUAI FORMAT! Mohon sesuaikan dengan format yang ada. Hubungi Administrator jika kesulitan.")
            return HttpResponseRedirect(reverse("alumni:alumni-quick-upload-csv"))
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = "CREATE",
            app = "ALUMNI",
            message = f"berhasil impor data csv alumni"
        )
        messages.success(self.request, "Selamat, Impor data CSV alumni berhasil!")
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'mengimpor dari csv', 'data alumni', 'alumni/')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Import CSV Alumni"
        return c
    
    
class AlumniDetailView(LoginRequiredMixin, DetailView):
    model = Alumni

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied


class AlumniUpdateView(LoginRequiredMixin, UpdateView):
    model = Alumni
    form_class = AlumniForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Update Data Gagal! :( Ada kesalahan input!")
        return super().form_invalid(form)
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save(commit=False)
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = "UPDATE",
            app = "ALUMNI",
            message = f"berhasil update data alumni atas nama {self.object.name} angkatan {self.object.group}"
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'update', f'data alumni {self.object.name} angkatan {self.object.group}', 'alumni/')
        messages.success(self.request, "Update Data Berhasil! :)")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c["form_name"] = "Update"
        return c


class AlumniDeleteView(LoginRequiredMixin, DeleteView):
    model = Alumni
    success_url = reverse_lazy("alumni:alumni-index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.obj = self.get_object()
        UserLog.objects.create(
            user = self.request.user.teacher,
            action_flag = "DELETE",
            app = "ALUMNI",
            message = f"berhasil menghapus data alumni atas nama {self.obj.name} angkatan {self.obj.group}"
        )
        send_WA_create_update_delete(self.request.user.teacher.no_hp, 'menghapus', f'data alumni {self.obj.name} angkatan {self.obj.group}', 'alumni/')
        messages.success(self.request, "Data Berhasil Dihapus! :)")
        return super().post(request, *args, **kwargs)
    


class AlumniDownloadExcelView(LoginRequiredMixin, ListView):
    model = Alumni
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'NIS', 'NISN', 'Nama', 'Angkatan', 'Tahun Lulus'])
        row = 1
        for data in self.get_queryset():
            worksheet.write_row(row, 0, [row, f"{data.nis}", f"{data.nisn}", data.name, data.group, data.graduate_year])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)

        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DOWNLOAD",
            app="ALUMNI",
            message="berhasil download daftar alumni dalam format Excel"
        )
        send_WA_general(request.user.teacher.no_hp, 'download', 'file Excel data alumni')
        return FileResponse(buffer, as_attachment=True, filename='Daftar Alumni SMA IT Al Binaa.xlsx')
    
    
class AlumniFilterDownloadExcelView(LoginRequiredMixin, ListView):
    model = Alumni
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_superuser:
            raise PermissionDenied
        query = self.kwargs.get("query")
        queryset = self.get_queryset().filter(Q(nis__icontains=query)|Q(name__icontains=query)|Q(nisn__icontains=query)|Q(group__icontains=query)|Q(graduate_year__icontains=query))
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'NIS', 'NISN', 'Nama', 'Angkatan', 'Tahun Lulus'])
        row = 1
        for data in queryset:
            worksheet.write_row(row, 0, [row, f"{data.nis}", f"{data.nisn}", data.name, data.group, data.graduate_year])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)

        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DOWNLOAD",
            app="ALUMNI",
            message="berhasil download list search alumni dalam format Excel"
        )
        send_WA_general(request.user.teacher.no_hp, 'download', 'file search Excel data alumni')
        return FileResponse(buffer, as_attachment=True, filename='List Search Alumni SMA IT Al Binaa.xlsx')