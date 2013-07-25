from django.db import models
from datetime import datetime

class Discussion(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey("elvis.Project")

    created = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        app_label = "elvis"
