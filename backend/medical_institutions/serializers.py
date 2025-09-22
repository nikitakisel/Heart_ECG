from rest_framework import serializers

from medical_institutions.models import MedicalInstitution


class MedicalInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInstitution
        fields = (
            'id',
            MedicalInstitution.name.field.name,
            MedicalInstitution.address.field.name,
            MedicalInstitution.phone.field.name,
            MedicalInstitution.website.field.name,
            MedicalInstitution.email.field.name,
        )
