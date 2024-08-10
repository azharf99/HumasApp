from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from users.models import Teacher
from students.models import Student


# Create your models here.
class Subject(models.Model):
    nama_pelajaran = models.CharField(max_length=100, verbose_name=_("Mata Pelajaran"))
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

class Private(models.Model):
    pembimbing = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=_("Pembimbing"))
    pelajaran = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Pelajaran"))
    tanggal_bimbingan = models.DateField(verbose_name=_("Tanggal"))
    waktu_bimbingan = models.TimeField(verbose_name=_("Waktu"))
    catatan_bimbingan = models.TextField(max_length=200, blank=True, verbose_name=_("Catatan"))
    kelompok = models.CharField(_("Kelompok"), max_length=20, default="1")
    kehadiran_santri = models.ManyToManyField(Student, verbose_name=_("Kehadiran Peserta"))
    foto = models.ImageField(upload_to='ekskul/laporan', default='no-image.png', help_text="Format foto .jpg atau .jpeg", verbose_name=_("Bukti Foto"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tanggal_bimbingan} - {self.pelajaran}"
    

    def get_absolute_url(self):
        return reverse("private:private-create")
    
    class Meta:
        ordering = ["-tanggal_bimbingan"]
        verbose_name = _("Private")
        verbose_name_plural = _("Private")
        db_table = "private"
        indexes = [
            models.Index(fields=["id","tanggal_bimbingan",]),
        ]