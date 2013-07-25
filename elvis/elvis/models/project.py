from django.db import models
from datetime import datetime

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField("elvis.UserProfile", blank=True, null=True)
    attachments = models.ManyToManyField("elvis.Attachment", blank=True, null=True)

    created = models.DateTimeField(default=datetime.now, blank=True)


    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        app_label = "elvis"
