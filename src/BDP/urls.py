from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from rest_framework_jwt.views import (
    obtain_jwt_token,
    verify_jwt_token,
    refresh_jwt_token,
)
from bloodbank.views import RegisterView, LoginView
from bloodbank.urls import BloodCatalogListView

urlpatterns = [
    url(r'^$', BloodCatalogListView.as_view(), name="home"),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^bloodcatalog/', include("bloodbank.urls", namespace="bloodcatalog")),
    url(r'^api/', include("bloodbank.api.urls", namespace="bloodcatalog-api")),
    url(r'^token/obtain/', obtain_jwt_token, name="token-obtain"),
    url(r'^token/verify/', verify_jwt_token, name="token-verify"),
    url(r'^token/refresh/', refresh_jwt_token, name="token-refresh"),
]
