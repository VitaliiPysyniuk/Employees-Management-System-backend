from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_kwargs):
        extra_kwargs.setdefault('role', 'ad')
        extra_kwargs.setdefault('is_active', True)

        if extra_kwargs.get('role') != 'ad':
            raise ValueError('User role has to be \'administrator\'.')
        if extra_kwargs.get('is_active') is not True:
            raise ValueError('User has to be active.')
        return self.create_user(email, password, **extra_kwargs)
