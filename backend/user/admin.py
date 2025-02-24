from django.contrib import admin

from user.models import PacienteProfile
from user.models import PersonalProfile
from user.models import User

admin.site.register(PacienteProfile)
admin.site.register(PersonalProfile)
admin.site.register(User)
