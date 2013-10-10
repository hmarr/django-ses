from django.db import models

__all__ = (
    'SESStat',
)

class SESStat(models.Model):
    date = models.DateField(unique=True, db_index=True)
    delivery_attempts = models.PositiveIntegerField()
    bounces = models.PositiveIntegerField()
    complaints = models.PositiveIntegerField()
    rejects = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'SES Stat'
        ordering = ['-date']

    def __unicode__(self):
        return self.date.strftime("%Y-%m-%d")
