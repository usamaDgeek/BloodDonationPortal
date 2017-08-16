from django.conf.urls import url
from .views import (
    BloodCatalogCreateAPIView,
    BloodCatalogListAPIView,
    BloodCatalogDetailAPIView,
    BloodCatalogUpdateAPIView,
    UserCreateAPIView,
    UserLoginAPIView,
    UserLogoutAPIView
)

urlpatterns = [
    url(r'^create/', BloodCatalogCreateAPIView.as_view(), name="create"),
    url(r'^$', BloodCatalogListAPIView.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/$', BloodCatalogDetailAPIView.as_view(), name="detail"),
    url(r'^update/(?P<pk>\d+)/$', BloodCatalogUpdateAPIView.as_view(), name="update"),
    url(r'^register/$', UserCreateAPIView.as_view(), name="register"),
    url(r'^login/$', UserLoginAPIView.as_view(), name="login"),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name="logout"),
]
