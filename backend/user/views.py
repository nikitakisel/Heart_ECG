from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user.models import PacienteProfile
from user.models import PersonalProfile
from user.serializers import RegisterSerializer


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.validated_data['is_active'] = True
            institution = serializer.validated_data.pop('institution')
            subdivision = serializer.validated_data.pop('subdivision')
            role = serializer.validated_data.pop('role')
            user = User.objects.create_user(**serializer.validated_data)

            if serializer.validated_data['is_staff']:
                if role == 'nurse':
                    user.is_nurse = True
                elif role == 'doctor':
                    user.is_doctor = True

                profile = PersonalProfile.objects.create(
                    institution=institution,
                    subdivision=subdivision,
                )
                profile_ct = ContentType.objects.get_for_model(PersonalProfile)
            else:
                profile = PacienteProfile.objects.create()
                profile_ct = ContentType.objects.get_for_model(PacienteProfile)

            user.profile_id = profile.id
            user.profile_type = profile_ct
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
