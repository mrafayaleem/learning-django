from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.http import urlquote
from django.utils import timezone


class DubizzleUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff=False):
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff, last_login=now
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password):
        return self._create_user(email, password)

    def create_superuser(self, email, password):
        return self._create_user(email, password=password, is_staff=True)


class DubizzleUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user class for Dubizzle.
    """
    MOTHER_CALL = (
        (0, 'Habibi (M)'), (1, 'Habibti (F)'),
    )

    COUNTRIES = (
        (0, 'Pakistan'), (1, 'United States'),
    )

    COMPANY_CALL = (
        (0, 'Student/Intern'), (1, 'Junior'), (2, 'Mid-level')
    )

    ACADEMIC = (
        (0, 'Bachelors Degree'), (1, 'Masters Degree'),
    )

    email = models.EmailField('Email Address', unique=True, db_index=True)
    first_name = models.CharField(verbose_name='First Name', max_length=30, default='')
    last_name = models.CharField(verbose_name='Last Name', max_length=30, default='')
    mother_call = models.IntegerField(choices=MOTHER_CALL, default=0)
    dob = models.DateField(auto_now_add=True)
    passport = models.IntegerField(choices=COUNTRIES, default=0)
    company_call = models.IntegerField(choices=COMPANY_CALL, default=0)
    academics = models.IntegerField(choices=ACADEMIC, default=0)

    ocassional_updates = models.BooleanField(default=True)
    amazing_offers = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = DubizzleUserManager()

    def __unicode__(self):
        return self.email

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


