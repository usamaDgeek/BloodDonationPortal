from .models import BloodCatalog
from .forms import BloodCatalogCreateForm, RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import googlemaps
from bloodbank.utils import get_client_info, get_client_ip
from .signals import user_logged_in
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)


class BloodCatalogListView(ListView):
    queryset = BloodCatalog.objects.all()


class BloodCatalogDetailView(DetailView):
    queryset = BloodCatalog.objects.all()


class BloodCatalogCreateView(LoginRequiredMixin, CreateView):
    form_class = BloodCatalogCreateForm
    template_name = "bloodbank/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)

        gm = googlemaps.Client(key='AIzaSyAqOazqPcP8E-_s-Vp7MRbP3UMUgS2xfQw')
        geocode_result = gm.geocode(instance.Address)[0]
        lat = geocode_result['geometry']['location']['lat']
        lng = geocode_result['geometry']['location']['lng']

        instance.owner = self.request.user
        instance.plocation_X = lat
        instance.plocation_Y = lng

        tloc = get_client_info(request=self.request)
        tip = get_client_ip(request=self.request)
        tcnt = tloc['country_name']
        tcty = tloc['city']
        tlat = tloc['latitude']
        tlng = tloc['longitude']
        instance.tlocation_X = tlat
        instance.tlocation_Y = tlng
        instance.city = tcty
        instance.country = tcnt
        instance.ip_address = tip

        return super(BloodCatalogCreateView, self).form_valid(form)


class BloodCatalogUpdateView(LoginRequiredMixin, UpdateView):
    queryset = BloodCatalog.objects.all()
    form_class = BloodCatalogCreateForm
    template_name = "bloodbank/form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)

        gm = googlemaps.Client(key='AIzaSyAqOazqPcP8E-_s-Vp7MRbP3UMUgS2xfQw')
        geocode_result = gm.geocode(instance.Address)[0]
        lat = geocode_result['geometry']['location']['lat']
        lng = geocode_result['geometry']['location']['lng']

        instance.owner = self.request.user
        instance.plocation_X = lat
        instance.plocation_Y = lng

        tloc = get_client_info(request=self.request)
        tip = get_client_ip(request=self.request)
        tcnt = tloc['country_name']
        tcty = tloc['city']
        tlat = tloc['latitude']
        tlng = tloc['longitude']
        instance.tlocation_X = tlat
        instance.tlocation_Y = tlng
        instance.city = tcty
        instance.country = tcnt
        instance.ip_address = tip

        return super(BloodCatalogUpdateView, self).form_valid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = "/login"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)


class LoginView(DefaultLoginView):

    def form_valid(self, form):
        done = super(LoginView, self).form_valid(form)
        if self.request.user.is_authenticated():
            user_logged_in.send(self.request.user, request=self.request)
        return done
