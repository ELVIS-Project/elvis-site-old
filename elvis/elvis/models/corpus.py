from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class Corpus(models.Model):
    old_id = models.IntegerField(db_index=True)
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    #created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    updated = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.title)

    class Meta:
        verbose_name_plural = "corpora"
        app_label = "elvis"
