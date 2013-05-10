import os
from django.db import models
from django.contrib.auth.models import User


class Attachment(models.Model):
    @property
    def attachment_path(self):
        return os.path.join("attachments", self.pk)

    attachment = models.FileField(upload_to=attachment_path, null=True, max_length=255)
    uploader = models.ForeignKey(User)

    class Meta:
        app_label = "elvis"
