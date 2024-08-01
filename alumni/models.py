from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your models here.

class Alumni(models.Model):
    nis = models.CharField(_("NIS"), max_length=255, blank=True, null=True)
    nisn = models.CharField(_("NISN"), max_length=255, blank=True, null=True)
    name = models.CharField(_("Nama Lengkap"), max_length=255, help_text=("Dilengkapi gelar jika ada"))
    group = models.CharField(_("Angkatan"), max_length=255, blank=True, null=True)
    birth_place = models.CharField(_("Tempat Lahir"), max_length=255, blank=True, null=True)
    birth_date = models.DateField(_("Tanggal Lahir"), blank=True, null=True)
    gender = models.CharField(_("Jenis Kelamin (L/P)"), max_length=1, choices=(("L", "Laki-laki"), ("P", "Perempuan")), default="L", blank=True, null=True)
    address = models.CharField(_("Alamat"), max_length=500, blank=True, null=True)
    city = models.CharField(_("Kota"), max_length=100, blank=True, null=True)
    province = models.CharField(_("Provinsi"), max_length=100, blank=True, null=True)
    state = models.CharField(_("Negara"), max_length=100, default="Indonesia", blank=True, null=True)
    phone = models.CharField(_("Whatsapp"), max_length=255, blank=True, null=True)
    last_class = models.CharField(_("Kelas Terakhir"), max_length=255, blank=True, null=True)
    graduate_year = models.CharField(_("Tahun Lulus"), max_length=4, blank=True, null=True)
    undergraduate_department = models.CharField(_("Jurusan Sarjana (S1)"), max_length=255, blank=True, null=True)
    undergraduate_university = models.CharField(_("Universitas Sarjana (S1)"), max_length=255, blank=True, null=True)
    undergraduate_university_entrance = models.CharField(_("Jalur Masuk Sarjana (S1)"), max_length=255, blank=True, null=True)
    postgraduate_department = models.CharField(_("Jurusan Magister (S2)"), max_length=255, blank=True, null=True)
    postgraduate_university = models.CharField(_("Universitas Magister (S2)"), max_length=255, blank=True, null=True)
    postgraduate_university_entrance = models.CharField(_("Jalur Masuk Magister (S2)"), max_length=255, blank=True, null=True)
    doctoral_department = models.CharField(_("Jurusan Doktoral (S3)"), max_length=255, blank=True, null=True)
    doctoral_university = models.CharField(_("Universitas Doktoral (S3)"), max_length=255, blank=True, null=True)
    doctoral_university_entrance = models.CharField(_("Jalur Masuk Doktoral (S3)"), max_length=255, blank=True, null=True)
    job = models.CharField(_("Pekerjaan"), max_length=255, blank=True, null=True)
    company_name = models.CharField(_("Nama Perusahaan"), max_length=255, blank=True, null=True)
    married = models.CharField(_("Status Pernikahan"), max_length=20, choices=(("Ya", "Sudah"), ("Tidak", "Belum")), default="Tidak", blank=True, null=True)
    father_name = models.CharField(_("Nama Ayah"), max_length=255, blank=True, null=True)
    mother_name = models.CharField(_("Nama Ibu"), max_length=255, blank=True, null=True)
    family_phone = models.CharField(_("Telpon Orang Tua"), max_length=255, blank=True, null=True)
    photo = models.ImageField(_("Foto Alumni"), upload_to='alumni', blank=True, null=True, default='blank-profile.png')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} | Angkatan {self.group}"
    

    def get_absolute_url(self):
        return reverse("alumni:alumni-detail", args={self.id})
    

    class Meta:
        ordering = ["-group", "name"]
        verbose_name = _("Alumni")
        verbose_name_plural = _("Alumni")
        db_table = "alumni"
        indexes = [
            models.Index(fields=["id", "name"]),
        ]



class Files(models.Model):
    file = models.FileField(upload_to='files/excel', help_text="Format .xlsx", verbose_name=_("File (Excel)"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.file}"
    

    def get_absolute_url(self):
        return reverse("alumni:alumni-quick-upload")
    

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("File")
        verbose_name_plural = _("Files")
        db_table = "files"
        indexes = [
            models.Index(fields=["id",]),
        ]

class CSVFiles(models.Model):
    file = models.FileField(upload_to='files/csv', help_text="Format .csv", verbose_name=_("File (CSV)"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.file}"
    

    def get_absolute_url(self):
        return reverse("alumni:alumni-quick-upload-csv")
    

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("CSV_File")
        verbose_name_plural = _("CSV_Files")
        db_table = "csv_files"
        indexes = [
            models.Index(fields=["id",]),
        ]