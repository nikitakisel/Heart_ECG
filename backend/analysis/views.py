from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from analysis.models import Analysis
from analysis.serializers import AnalysisSerializer


class AnalysisViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AnalysisSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        return Analysis.objects.filter(user_id=user.id)
