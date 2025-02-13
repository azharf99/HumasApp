from typing import Any
from alumni.models import Alumni
from django.db.models import Q, Count
from django.utils import timezone
from django.views.generic import ListView
from private.models import Private, Subject
from students.models import Student
from userlog.models import UserLog




class DashboardView(ListView):
    model = Alumni
    template_name = 'dashboard.html'
    queryset = Alumni.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        c = super().get_context_data(**kwargs)
        
        c["jumlah_santri"] = Student.objects.filter(status="Aktif")
        c["jumlah_santri_putra"] = c["jumlah_santri"].filter(status="Aktif", jenis_kelamin="L").count()
        c["jumlah_santri_putri"] = c["jumlah_santri"].filter(status="Aktif", jenis_kelamin="P").count()
        c["jumlah_private"] = Private.objects.all()
        c["jumlah_private_bulan_ini"] = c["jumlah_private"].filter(tanggal_bimbingan__month=timezone.now().month).count()
        c["jumlah_private_bulan_lalu"] = c["jumlah_private"].filter(tanggal_bimbingan__month=timezone.now().month-1).count()
        c["jumlah_mapel_private"] = Subject.objects.select_related("pelajaran").all()
        c["jumlah_mapel_private_aktif"] = c["jumlah_private"].values_list("pelajaran").distinct()
        c["jumlah_mapel_private_nonaktif"] = Subject.objects.exclude(pk__in=c["jumlah_mapel_private_aktif"]).count()
        c["jumlah_alumni_putra"] = self.queryset.filter(gender="L")
        c["jumlah_alumni_putri"] = self.queryset.filter(gender="P")
        c["jumlah_alumni_tahun_ini"] = self.queryset.filter(graduate_year=timezone.now().year)
        c["jumlah_alumni_putra_tahun_ini"] = self.queryset.filter(gender="L", graduate_year=timezone.now().year)
        c["jumlah_alumni_putri_tahun_ini"] = self.queryset.filter(gender="P", graduate_year=timezone.now().year)
        c["jumlah_alumni_universitas"] = self.queryset.exclude(undergraduate_university__isnull=True)
        c["jumlah_alumni_putra_universitas"] = self.queryset.filter(gender="L").exclude(undergraduate_university__isnull=True)
        c["jumlah_alumni_putra_non_univ"] = self.queryset.filter(gender="L", undergraduate_university="")
        c["jumlah_alumni_putri_universitas"] = self.queryset.filter(gender="P").exclude(undergraduate_university__isnull=True)
        c["jumlah_alumni_putri_non_univ"] = self.queryset.filter(gender="P", undergraduate_university="")
        c["logs"] = UserLog.objects.order_by("-created_at")[:10]
        c["sebaran_universitas_sarjana"] = self.queryset.exclude(undergraduate_university__in=[0, '']).values('undergraduate_university')\
                                                        .annotate(dcount=Count('undergraduate_university')).order_by('-dcount')[:20]

        return c