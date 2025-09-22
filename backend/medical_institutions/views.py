from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from medical_institutions.models import MedicalInstitution
from medical_institutions.serializers import MedicalInstitutionSerializer


class MedicalInstitutionViewSet(ListModelMixin, GenericViewSet):
    queryset = MedicalInstitution.objects.order_by('name')
    serializer_class = MedicalInstitutionSerializer
