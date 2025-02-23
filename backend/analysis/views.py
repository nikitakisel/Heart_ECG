from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from analysis.models import ECGAnalysis
from analysis.serializers import ECGAnalysisSerializer


class ECGAnalysisViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ECGAnalysisSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        return ECGAnalysis.objects.filter(user_id=user.id)
