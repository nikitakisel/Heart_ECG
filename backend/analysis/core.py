from django.db import models

from analysis.helpers import get_random_slug
from core.models import TimestampedAbstractModel
from user.models import User


class AnalysisAbstractModel(TimestampedAbstractModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    name = models.CharField('название', max_length=200)
    slug = models.CharField(
        max_length=32,
        db_index=True,
        unique=True,
        default=get_random_slug,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
