from django.db import models
from django.contrib.auth.models import User


class Movement(models.Model):
    old_id = models.IntegerField()
    title = models.CharField(max_length=255)
    uploader = models.ForeignKey(User)
    corpus = models.ForeignKey("elvis.Corpus")
    composer = models.ForeignKey("elvis.Composer")
    date_of_composition = models.DateField(blank=True, null=True)
    number_of_voices = models.IntegerField(blank=True, null=True)
    tags = models.ManyToManyField("elvis.Tag", blank=True, null=True)
    attachments = models.ManyToManyField("elvis.Attachment", blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        app_label = "elvis"
