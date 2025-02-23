from django.contrib import admin

from analysis.models import (
    BABloodAnalysis,
    ECGAnalysis,
    OAKAnalysis,
    OAMAnalysis,
)

admin.site.register(
    (BABloodAnalysis, ECGAnalysis, OAKAnalysis, OAMAnalysis),
)
