from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AnonymousUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.create_user(username, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

def serialize_public(user):
    if isinstance(user, AnonymousUser):
        # TODO: uniqify this somehow
        return {
            'username': 'Anonymous',
            'image': None,
        }
    else:
        return {
            'username': user.username,
            'image': None, #TODO
        }


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True,
            error_messages={'unique': "An account with that username already exists."})
    email = models.EmailField("Email address", blank=True, null=True,
            unique=True, default=None)
    twitter_handle = models.CharField(max_length=100, blank=True, null=True,
            unique=True, default=None)
    linkedin_profile = models.CharField(max_length=100, blank=True, null=True,
            unique=True, default=None)
    share_info = models.BooleanField(default=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] # Used only by createsuperuser management command

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        return super(User, self).save(*args, **kwargs)

    def clean(self):
        if self.email:
            self.email = UserManager.normalize_email(self.email)
        if self.twitter_handle:
            self.twitter_handle = self.twitter_handle.lower()

    def serialize_public(self):
        return serialize_public(self)

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username
