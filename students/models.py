from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

# Create your models here.
class Class(models.Model):
    nama_kelas = models.CharField(max_length=20, unique=True, verbose_name=_("Nama Kelas"))
    tahun_ajaran = models.CharField(max_length=20, verbose_name=_("Tahun Ajaran"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nama_kelas} | {self.tahun_ajaran}"

    def get_absolute_url(self):
        return reverse("student:class-index")

    class Meta:
        ordering = ["nama_kelas"]
        verbose_name = _("Class")
        verbose_name_plural = _("Classes")
        db_table = "class"
        indexes = [
            models.Index(fields=["nama_kelas", "id",]),
        ]

class Student(models.Model):
    nis = models.CharField(max_length=20, unique=True, verbose_name=_("NIS"))
    nisn = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("NISN"))
    nama_siswa = models.CharField(max_length=100,verbose_name=_("Nama"))
    kelas = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name=_("Kelas"))
    jenis_kelamin = models.CharField(max_length=10, choices=(("L", "Laki-Laki"), ("P", "Perempuan")), default="L", verbose_name=_("Jenis kelamin"))
    alamat = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Alamat"))
    tempat_lahir = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Tempat Lahir"))
    tanggal_lahir = models.DateField(blank=True, null=True, verbose_name=_("Tanggal Lahir"))
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name=_("Email"))
    nomor_hp = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Whatsapp"))
    status = models.CharField(max_length=20, blank=True, default="Aktif", verbose_name=_("Status"))
    foto = models.ImageField(upload_to='student', blank=True, null=True, default='blank-profile.png', help_text="Format foto .jpg/.jpeg", verbose_name=_("Foto"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.kelas} | {self.nama_siswa}"

    def get_absolute_url(self):
        return reverse("student:student-index")

    class Meta:
        ordering = ["kelas", "nama_siswa"]
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        db_table = "students"
        indexes = [
            models.Index(fields=["nis", "id",]),
        ]