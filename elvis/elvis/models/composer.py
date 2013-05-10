from django.db import models


class Composer(models.Model):
    old_id = models.IntegerField()
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    death_date = models.DateField()

    class Meta:
        app_label = "elvis"
