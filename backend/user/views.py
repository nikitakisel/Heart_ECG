from django.contrib.contenttypes.models import ContentType
from rest_framework import status, viewsets, decorators
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user.models import PacienteProfile
from user.models import PersonalProfile
from user.serializers import RegisterSerializer
from user.serializers import CurrentUserPacienteProfileSerializer


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['is_active'] = True
            institution = serializer.validated_data.pop('institution', None)
            subdivision = serializer.validated_data.pop('subdivision', None)
            role = serializer.validated_data.pop('role', None)
            passport_series = serializer.validated_data.pop(
                'passport_series',
                None,
            )
            passport_number = serializer.validated_data.pop(
                'passport_number',
                None,
            )
            email_value = serializer.validated_data.get('email')
            user = User.objects.create_user(**serializer.validated_data)

            # Ensure email persisted
            if email_value and user.email != email_value:
                user.email = email_value
                user.save(update_fields=['email'])

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

            user.profile.passport_series = passport_series
            user.profile.passport_number = passport_number
            user.profile.save()

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @decorators.action(
        detail=False,
        methods=['get', 'put', 'patch'],
        url_path='me',
    )
    def me(self, request: Request):
        user = request.user

        if request.method in ['PUT', 'PATCH']:
            serializer = CurrentUserPacienteProfileSerializer(
                instance=user,
                data=request.data,
                partial=(request.method == 'PATCH'),
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = CurrentUserPacienteProfileSerializer(
                instance=user,
                context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
