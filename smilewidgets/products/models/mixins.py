from django.db import models


class DateFramedMixin(models.Model):
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    @staticmethod
    def date_intersections(date):
        end_date_filter = models.Q(date_end__gte=date) | models.Q(date_end__isnull=True)
        return models.Q(date_start__lte=date) & end_date_filter
