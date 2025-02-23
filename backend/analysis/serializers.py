from django.core.files.base import ContentFile
from rest_framework import serializers

from analysis.main import analyse
from analysis.models import ECGAnalysis
from user.serializers import UserSerializer


class ECGAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=False, read_only=True)
    slug = serializers.CharField(read_only=True)
    result_image = serializers.FileField(read_only=True)

    class Meta:
        model = ECGAnalysis
        fields = (
            ECGAnalysis.user.field.name,
            ECGAnalysis.slug.field.name,
            ECGAnalysis.name.field.name,
            ECGAnalysis.image.field.name,
            ECGAnalysis.result_image.field.name,
        )

    def create(self, validated_data):
        validated_data.pop('user', None)
        image_file = validated_data.get('image')
        processed_image_bytes = analyse(image_file)
        analysis = ECGAnalysis.objects.create(
            user=self.context['request'].user,
            result_image=ContentFile(
                processed_image_bytes,
                name=image_file.name,
            ),
            **validated_data,
        )
        return analysis
