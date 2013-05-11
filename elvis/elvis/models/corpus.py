from django.db import models
from django.contrib.auth.models import User


class Corpus(models.Model):
    old_id = models.IntegerField()
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"{0}".format(self.title)

    class Meta:
        verbose_name_plural = "corpora"
        app_label = "elvis"
