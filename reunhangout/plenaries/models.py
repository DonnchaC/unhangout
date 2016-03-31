from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from richtext.utils import sanitize

from jsonfield import JSONField
from timezone_field import TimeZoneField

class Series(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(help_text="Short name for URL")
    organizer = models.CharField(max_length=100, default="", blank=True)
    image = models.ImageField(upload_to="series", blank=True, null=True)
    description = models.TextField(default="", blank=True)
    start_date = models.DateTimeField(_("Start date (UTC)"))
    end_date = models.DateTimeField(_("End date (UTC)"))
    time_zone = TimeZoneField(default='America/New_York',
           help_text=_("Default time zone to display times in."))

    admins = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def safe_description(self):
        return sanitize(self.description)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Series")

# Create your models here.
class Plenary(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(help_text=_("Short name for URL"))
    organizer = models.CharField(max_length=100, default="", blank=True)
    image = models.ImageField(upload_to="plenaries", blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    public = models.BooleanField(default=False,
        help_text=_("Check to display this plenary on the public events list"))
    description = models.TextField(default="", blank=True,)
    whiteboard = models.TextField(default="", blank=True)
    time_zone = TimeZoneField(default='America/New_York',
        help_text=_("Default time zone to display times in."))

    embeds = JSONField(blank=True, null=True)
    history = JSONField(blank=True, null=True)
    open = models.BooleanField(default=False,
            help_text=_("Check to allow people to chat in this plenary"))
    breakouts_open = models.BooleanField(default=False,
            help_text=_("Check to allow people to join breakouts associated with this plenary"))

    admins = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def safe_description(self):
        return sanitize(self.description)

    def safe_whiteboard(self):
        return sanitize(self.whiteboard)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("plenaries")
