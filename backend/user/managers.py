from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    def get_by_natural_key(self, value):
        if '@' in value:
            return self.get(email__iexact=value)
        return self.get(username__iexact=value)

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        normalized_email = self.normalize_email(email) if email else None
        user = self.model(
            username=username,
            email=normalized_email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)
