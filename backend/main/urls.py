from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from analysis.views import ECGAnalysisViewSet
from medical_institutions.views import MedicalInstitutionViewSet
from user.views import RegisterView
from user.views import UserProfileViewSet

router = SimpleRouter()

router.register(r'analysis', ECGAnalysisViewSet, basename='analysis')
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(
    r'medical-institutions',
    MedicalInstitutionViewSet,
    basename='medical_institutions',
)

api_namespace = router.urls
api_namespace += [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = [
    path('api/', include((api_namespace, 'api'), namespace='api')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
