from django.db import models


class MedicalInstitution(models.Model):
    name = models.CharField('название', max_length=500)
    address = models.CharField('адрес', max_length=200)
    phone = models.CharField('номер телефона', max_length=15)
    website = models.URLField('веб-сайт', null=True, blank=True)
    email = models.EmailField('электронная почта', null=True, blank=True)

    class Meta:
        verbose_name = 'медицинское учреждение'
        verbose_name_plural = 'медицинские учреждения'

    def __str__(self) -> str:
        return self.name
