from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib import messages
from django.db.models import Q, Count
from django.urls import reverse, reverse_lazy
from utils.mixins import GeneralAuthPermissionMixin, GeneralContextMixin, GeneralDownloadExcelView, GeneralFormDeleteMixin, GeneralFormValidateMixin
from alumni.models import Alumni, Files, CSVFiles
from alumni.forms import AlumniForm, FilesForm, CSVFilesForm
from django.utils import timezone
from utils.whatsapp_albinaa import send_WA_create_update_delete
from userlog.models import UserLog
from pandas import read_excel, read_csv

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


class AlumniIndexView(GeneralContextMixin, ListView):
    model = Alumni
    paginate_by = 50



class AlumniSearchView(GeneralContextMixin, ListView):
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
                                         Q(undergraduate_university__icontains=query)|
                                         Q(undergraduate_university_entrance__icontains=query)|
                                         Q(undergraduate_department__icontains=query))
            if len(data) > 0:
                messages.success(request, f"{len(data)} Data Berhasil Ditemukan!")
            else:
                messages.error(request, "Data Tidak Ditemukan!")
            queryset = data
        self.object_list = queryset
        context = self.get_context_data()
        return self.render_to_response(context)


class AlumniCreateView(GeneralFormValidateMixin, CreateView):
    model = Alumni
    form_class = AlumniForm
    form_name = "Create"
    app_name = "Alumni"
    type_url = 'alumni/'
    permission_required = 'alumni.add_alumni'
    

class AlumniQuickUploadView(GeneralAuthPermissionMixin, CreateView):
    model = Files
    form_class = FilesForm
    permission_required = 'alumni.add_alumni'
    form_name = "Import Excel Alumni"

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
    

class AlumniCSVQuickUploadView(GeneralAuthPermissionMixin, CreateView):
    model = CSVFiles
    form_class = CSVFilesForm
    template_name = 'alumni/files_form.html'
    permission_required = 'alumni.add_alumni'
    form_name = "Import CSV Alumni"


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
    
    
class AlumniDetailView(GeneralAuthPermissionMixin, DetailView):
    model = Alumni
    permission_required = 'alumni.view_alumni'


class AlumniUpdateView(GeneralFormValidateMixin, UpdateView):
    model = Alumni
    form_class = AlumniForm
    app_name = "Alumni"
    form_name = "Update"
    type_url = 'alumni/'
    permission_required = 'alumni.change_alumni'


class AlumniDeleteView(GeneralFormDeleteMixin):
    model = Alumni
    success_url = reverse_lazy("alumni:alumni-index")
    app_name = 'Alumni'
    type_url = 'alumni/'
    permission_required = 'alumni.delete_alumni'
    


class AlumniDownloadExcelView(GeneralDownloadExcelView):
    app_name = 'Alumni'
    permission_required = 'alumni.view_alumni'
    template_name = 'alumni/download.html'
    header_names = ['No', 'NIS', 'NISN', 'Nama', 'Angkatan', 'Tahun Lulus']
    filename = 'Daftar Alumni SMA IT Al Binaa.xlsx'
    queryset = Alumni.objects.all()
    
