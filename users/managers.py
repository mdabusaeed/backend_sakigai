from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('This Email field must be set')
        email = self.normalize_email(email)
        # Remove is_staff and is_superuser from extra_fields if they exist
        extra_fields.pop('is_staff', None)
        extra_fields.pop('is_superuser', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser = True')

        # Remove is_staff and is_superuser from extra_fields before calling create_user
        is_staff = extra_fields.pop('is_staff')
        is_superuser = extra_fields.pop('is_superuser')
        
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user