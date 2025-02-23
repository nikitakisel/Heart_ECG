from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from analysis.core import AnalysisAbstractModel


class ECGAnalysis(AnalysisAbstractModel):
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
        verbose_name = verbose_name_plural = 'ЭКГ'


class OAKAnalysis(AnalysisAbstractModel):
    hemoglobin = models.PositiveBigIntegerField('гемоглобин (г/л)')
    erythrocytes = models.PositiveIntegerField('эритроциты (х1012/л)')
    hematocrit = models.FloatField(
        'гематокрит (%)',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
    )
    platelets = models.PositiveIntegerField('тромбоциты (х109/л)')
    leukocytes = models.FloatField('лейкоциты (х109/л)')
    esr = models.PositiveIntegerField('скорость оседания эритроцитов (мм/ч)')
    lymphocytes = models.FloatField('лимфоциты (109/л)')
    monocytes = models.FloatField('моноциты (109/л)')
    thrombocytocrit = models.FloatField(
        'тромбоцитокрит (%)',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
    )
    granulocytes = models.FloatField(
        'гранулоциты (%)',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
    )
    avg_erythrocytes_volume = models.FloatField(
        'средний объем эритроцита (фл)',
    )
    avg_hemoglobin_content = models.FloatField(
        'среднее содержание гемоглобина (пг)',
    )
    avg_hemoglobin_concentration = models.PositiveIntegerField(
        'средняя концентрация гемоглобина (г/л)',
    )
    erythrocytes_distribution_index = models.FloatField(
        'индекс распределения эритроцитов (%)',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
    )
    avg_platelets_volume = models.FloatField('средний объем тромбоцита (фл)')
    distribution_width = models.FloatField(
        'ширина распределения (%)',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
    )

    class Meta:
        verbose_name = verbose_name_plural = 'ОАК'


class OAMAnalysis(AnalysisAbstractModel):
    color = models.CharField('цвет', max_length=100)
    transparency = models.CharField('прозрачность', max_length=100)
    relative_density = models.FloatField('относительная плотность')
    ph = models.FloatField('pH')
    leukocytes = models.BooleanField('лейкоциты', default=False)
    nitrites = models.BooleanField('нитриты', default=False)
    protein = models.BooleanField('белок', default=False)
    glucose = models.BooleanField('глюкоза', default=False)
    ketones = models.BooleanField('кетоны', default=False)
    bilirubin = models.BooleanField('билирубин', default=False)
    ascorbic_acid = models.BooleanField(
        'аскорбиновая кислота',
        default=False,
    )
    urobilinogen = models.BooleanField(
        'уробилиноген',
        default=False,
    )
    erythrocytes = models.BooleanField('эритроциты', default=False)

    class Meta:
        verbose_name = verbose_name_plural = 'ОАМ'


class BABloodAnalysis(AnalysisAbstractModel):
    total_protein = models.FloatField('общий белок (г/л)')
    albumen = models.FloatField('альбумин (г/л)')
    urea = models.FloatField('мочевина (ммоль/л)')
    creatinine = models.FloatField('креатинин (ммоль/л)')
    total_bilirubin = models.FloatField('общий билирубин (ммоль/м)')
    direct_bilirubin = models.FloatField('прямой билирубин (ммоль/л)')
    indirect_bilirubin = models.FloatField('непрямой билирубин (ммоль/л)')
    glucose = models.FloatField('глюкоза (ммоль/г)')
    c_reactive_protein = models.PositiveIntegerField(
        'С-Реактивный белок (мг/л)',
    )
    asat = models.FloatField('АсАт')
    alat = models.FloatField('АлАт')
    calcium = models.FloatField('кальций (ммоль/г)')
    sodium = models.FloatField('натрий (ммоль/г)')
    potassium = models.FloatField('калий (ммоль/г)')
    chlorides = models.FloatField('хлориды (ммоль/л)')

    class Meta:
        verbose_name = verbose_name_plural = 'БХ Крови'
