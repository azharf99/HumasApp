from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your models here.


class UserLog(models.Model):
    user = models.CharField(max_length=200)
    action_flag = models.CharField(max_length=200)
    app = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.action_flag} {self.app}"
        
    def get_absolute_url(self):
        return reverse("userlog:userlog-index")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("User Log")
        verbose_name_plural = _("User Logs")
        db_table = "user_logs"
        indexes = [
            models.Index(fields=["id",]),
        ]
