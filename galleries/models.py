from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

# Create your models here.
class Gallery(models.Model):
    title = models.CharField(_("Judul Galeri"), max_length=255, blank=True)
    image = models.FileField(upload_to='gallery/activity', help_text="Format .jpg/.png", verbose_name=_("Gambar"))
    caption = models.CharField(_("Caption Gambar"), max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Galeri {self.title if self.title else self.id}"
    

    def get_absolute_url(self):
        return reverse("galleries:gallery-list")
    

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")
        db_table = "galleries"
        indexes = [
            models.Index(fields=["id",]),
        ]