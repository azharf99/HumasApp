from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse

from students.models import Student
from users.models import Teacher

# Create your models here.
year_now = timezone.now().year
month_now = timezone.now().month

class Subject(models.Model):
    nama_pelajaran = models.CharField(_("Mata Pelajaran"), max_length=100)
    pembimbing = models.ManyToManyField(Teacher, verbose_name=_("Pembimbing"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_pelajaran

    def get_absolute_url(self):
        return reverse("private:subject-index")
    
    class Meta:
        ordering = ["nama_pelajaran"]
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        db_table = "subjects"
        indexes = [
            models.Index(fields=["id","nama_pelajaran",]),
        ]

class Group(models.Model):
    nama_kelompok = models.CharField(_("Nama Kelompok"), max_length=255)
    jenis_kelompok = models.CharField(_("Jenis Kelompok"), max_length=255, blank=True, null=True)
    pelajaran = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Pelajaran"))
    jadwal = models.CharField(_("Jadwal"), max_length=255, blank=True, null=True)
    waktu = models.CharField(_("Waktu"), max_length=255, blank=True, null=True)
    santri = models.ManyToManyField(Student, blank=True, verbose_name=_("Santri"), help_text=_("Ketik nama yang ingin dicari dan pilih. Kamu bisa memilih lebih dari 1 (satu). Untuk menghapusnya, klik nama yang ingin dihapus hingga berwarna biru/terang, lalu tekan delete atau backspace."))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Kel. {self.nama_kelompok} {self.pelajaran} {self.jadwal} {self.waktu}"


    def get_absolute_url(self):
        return reverse("private:group-index")
    
    class Meta:
        ordering = ["nama_kelompok", "pelajaran"]
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        db_table = "groups"
        indexes = [
            models.Index(fields=["id",]),
        ]

class Private(models.Model):
    pembimbing = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=_("Pembimbing"))
    pelajaran = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Pelajaran"))
    tanggal_bimbingan = models.DateField(verbose_name=_("Tanggal"))
    waktu_bimbingan = models.TimeField(verbose_name=_("Waktu"))
    catatan_bimbingan = models.TextField(max_length=200, blank=True, verbose_name=_("Catatan"))
    kelompok = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    kehadiran_santri = models.ManyToManyField(Student, verbose_name=_("Kehadiran Peserta"), help_text="Pada PC, tekan CTRL + Clik untuk memilih lebih dari satu (1).")
    foto = models.ImageField(upload_to='privat/laporan', default='no-image.png', help_text="Format foto .jpg atau .jpeg", verbose_name=_("Bukti Foto"))
    tahun_ajaran = models.CharField(_("Tahun Ajaran"), max_length=50, default=f"{year_now if month_now > 6 else year_now - 1 }/{year_now + 1 if month_now > 6 else year_now}", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pelajaran} ({self.tanggal_bimbingan})"
    

    def get_absolute_url(self):
        return reverse("private:private-index")
    
    class Meta:
        ordering = ["-tanggal_bimbingan"]
        verbose_name = _("Private")
        verbose_name_plural = _("Private")
        db_table = "private"
        indexes = [
            models.Index(fields=["id","tanggal_bimbingan",]),
        ]