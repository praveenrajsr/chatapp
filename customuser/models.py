from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.apps import apps


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password, email=None, username=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone:
            raise ValueError('The given phone number must be set')
        if email:
            email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        try:
            user = self.model(phone=phone, email=email, **extra_fields)
        except:
            user = self.model(phone=phone, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, email=None, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(phone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=50, default='Anonymous')

    email = models.EmailField(
        max_length=254, unique=True, null=True, blank=True)

    phone = models.CharField(max_length=255, unique=True)

    username = None

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = ['email']

    is_premium = models.BooleanField(default=False)

    expires_on = models.DateField(null=True, blank=True)

    gender = models.CharField(max_length=10, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    date_joined = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.phone

    def get_short_name(self):
        # The user is identified by their email address
        return self.phone

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Gallery(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    images = models.ImageField(
        upload_to='gallery/', default='assets/images/user.png')
    is_profile_photo = models.BooleanField(default=False)
