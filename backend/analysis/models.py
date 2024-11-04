from django.db import models

from analysis.helpers import get_random_slug
from user.models import User


class Analysis(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='analysis',
    )
    name = models.CharField('название', max_length=200)
    slug = models.CharField(
        max_length=32,
        db_index=True,
        unique=True,
        default=get_random_slug,
    )
    image = models.ImageField(
        'изображение',
        upload_to='analysis/',
        null=True,
        blank=True,
    )
    result_image = models.ImageField(
        'обработанное изображение',
        upload_to='analysis_results/',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = verbose_name_plural = 'analysis'

    def __str__(self):
        return self.name
