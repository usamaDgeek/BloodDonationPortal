from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from .signals import user_logged_in
from .utils import get_client_info, get_client_ip

User = settings.AUTH_USER_MODEL

class UserSessionManager(models.Manager):
    def create_new(self, user, session_key=None, ip_address=None, city_data=None, tlocation_X=None, tlocation_Y=None):
        session_new = self.model()
        session_new.user = user
        session_new.session_key = session_key
        if ip_address is not None:
            session_new.ip_address = ip_address
            if city_data:
                session_new.city_data = city_data
                try:
                    city = city_data['city']
                except:
                    city = None
                session_new.city = city
                try:
                    country = city_data['country_name']
                except:
                    country = None
                try:
                    tlocation_X = city_data['latitude']
                except:
                    tlocation_X = None
                try:
                    tlocation_Y = city_data['longitude']
                except:
                    tlocation_Y = None
            session_new.country = country
            session_new.tlocation_X = tlocation_X
            session_new.tlocation_Y = tlocation_Y
            session_new.save()
            return session_new
        return None

class UserSession(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    session_key     = models.CharField(max_length=60, null=True, blank=True)
    ip_address      = models.GenericIPAddressField(null=True, blank=True)
    city_data       = models.TextField(null=True, blank=True)
    city            = models.CharField(max_length=120, null=True, blank=True)
    country         = models.CharField(max_length=120, null=True, blank=True)
    tlocation_X       = models.FloatField(verbose_name="Current Location X-axis", blank=True, null=True)
    tlocation_Y       = models.FloatField(verbose_name="Current Location Y-axis", blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = UserSessionManager()

    def __str__(self):
        city = self.city
        country = self.country
        if city and country:
            return f"{city}, {country}"
        elif city and not country:
            return f"{city}"
        elif country and not city:
            return f"{country}"
        return self.user.username


def user_logged_in_receiver(sender, request, *args, **kwargs):
    user = sender
    ip_address = get_client_ip(request)
    city_data = get_client_info(request)
    request.session['CITY'] = str(city_data.get('city', 'New York'))
    session_key = request.session.session_key
    UserSession.objects.create_new(
        user=user,
        session_key=session_key,
        ip_address=ip_address,
        city_data=city_data,
        tlocation_X=city_data['latitude'],
        tlocation_Y=city_data['longitude'],
    )


class BloodCatalog(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=120)
    nature = models.CharField(verbose_name="Select Source Type", max_length=10)
    contact_no = models.CharField(verbose_name="Contact Number", max_length=14)
    tlocation_X = models.FloatField(verbose_name="Current Location X-axis", blank=True, null=True)
    tlocation_Y = models.FloatField(verbose_name="Current Location Y-axis", blank=True, null=True)
    Address = models.CharField(max_length=300)
    plocation_X = models.FloatField(verbose_name="Permanent Location X-axis", blank=True, null=True)
    plocation_Y = models.FloatField(verbose_name="Permanent Location Y-axis", blank=True, null=True)
    time_from = models.TimeField(verbose_name="Time: Available from (for donation)/Needed from(for reception)", help_text="Format: 00:00:00")
    time_to = models.TimeField(verbose_name="Time: Available to (for donation)/Needed to (for reception)", help_text="Format: 00:00:00")
    date = models.DateField(verbose_name="Date: on blood available/needed", help_text="Format: yyyy-mm-dd")
    last_transaction = models.DateField(verbose_name="Date of Last donation/reception", help_text="Format: yyyy-mm-dd")
    group = models.CharField(verbose_name="Blood Group", max_length=3)
    bags = models.IntegerField(verbose_name="Number of Blood Bags")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("bloodcatalog:detail", kwargs={"pk": self.pk})

user_logged_in.connect(user_logged_in_receiver)
