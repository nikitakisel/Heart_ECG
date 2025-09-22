from rest_framework import serializers

from user.models import User
from user.models import PacienteProfile
from analysis.models import ECGAnalysis


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            User.id.field.name,
            User.username.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.patronymic.field.name,
            User.email.field.name,
        )


class RegisterSerializer(serializers.ModelSerializer):
    institution = serializers.CharField(required=False, allow_null=True)
    subdivision = serializers.CharField(required=False, allow_null=True)
    role = serializers.CharField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True)
    passport_series = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    passport_number = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    class Meta:
        model = User
        fields = (
            User.username.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.patronymic.field.name,
            User.email.field.name,
            User.password.field.name,
            User.is_staff.field.name,
            'institution',
            'subdivision',
            'role',
            'passport_series',
            'passport_number',
        )


class PacienteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteProfile
        fields = (
            PacienteProfile.height.field.name,
            PacienteProfile.weight.field.name,
            PacienteProfile.passport_series.field.name,
            PacienteProfile.passport_number.field.name,
            PacienteProfile.registration.field.name,
            PacienteProfile.cmi_policy.field.name,
            PacienteProfile.systolic_blood_pressure.field.name,
            PacienteProfile.diastolic_blood_pressure.field.name,
            PacienteProfile.health_status.field.name,
            PacienteProfile.skin_and_mucous_membrane.field.name,
            PacienteProfile.subcutaneous_fat.field.name,
            PacienteProfile.lymphatic_system.field.name,
            PacienteProfile.musculoskeletal_system.field.name,
            PacienteProfile.respiratory_system.field.name,
            PacienteProfile.cardiovascular_system.field.name,
            PacienteProfile.digestive_system.field.name,
            PacienteProfile.genitourinary_system.field.name,
            PacienteProfile.endocrine_system.field.name,
            PacienteProfile.nervous_system.field.name,
            PacienteProfile.past_illnesses.field.name,
            PacienteProfile.disability.field.name,
            PacienteProfile.education.field.name,
            PacienteProfile.profession.field.name,
            PacienteProfile.family_status.field.name,
            PacienteProfile.has_children.field.name,
        )


class CurrentUserPacienteProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    last_name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        required=False,
    )
    first_name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        required=False,
    )
    patronymic = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        required=False,
    )
    email = serializers.EmailField(
        allow_null=True,
        allow_blank=True,
        required=False,
    )
    sex = serializers.ChoiceField(
        choices=[('m', 'мужской'), ('w', 'женский')],
        required=False,
    )
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    profile = PacienteProfileSerializer()
    analyses = serializers.ListField(
        child=serializers.DictField(),
        read_only=True,
    )

    def to_representation(self, instance):
        user = instance
        data = {
            'id': user.id,
            'username': user.username,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'patronymic': user.patronymic,
            'email': user.email,
            'sex': user.sex,
            'date_of_birth': user.date_of_birth,
            'profile': (
                PacienteProfileSerializer(user.profile).data
                if isinstance(user.profile, PacienteProfile)
                else None
            ),
        }

        from analysis.serializers import ECGAnalysisSerializer

        analyses_qs = ECGAnalysis.objects.filter(
            user_id=user.id,
        ).order_by('-id')
        data['analyses'] = ECGAnalysisSerializer(
            analyses_qs,
            many=True,
            context=self.context,
        ).data
        return data

    def update(self, instance, validated_data):
        user = instance
        profile_data = validated_data.pop('profile', {})

        for field in [
            'first_name',
            'last_name',
            'patronymic',
            'email',
            'sex',
            'date_of_birth',
        ]:
            if field in validated_data:
                setattr(user, field, validated_data[field])
        user.save()

        if not isinstance(user.profile, PacienteProfile):
            raise serializers.ValidationError(
                'Профиль доступен только пациентам.',
            )

        profile: PacienteProfile = user.profile
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()

        return user
