from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_countries.fields import CountryField

class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, account_number, nationality, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have a username')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            account_number=account_number,
            nationality=nationality
        )

        user.set_password(password)
        
        user.save()
        return user

    


class UserAccount(AbstractBaseUser):
    first_name = models.CharField(max_length=250, blank= False)
    last_name = models.CharField(max_length=250, blank= False)
    email = models.EmailField(('email address'), unique = True)
    username = models.CharField(max_length=50, unique=True, blank=False, default='username')
    image = models.ImageField(blank=True)
    account_number = models.CharField(max_length=10)
    nationality = CountryField(blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]


    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

