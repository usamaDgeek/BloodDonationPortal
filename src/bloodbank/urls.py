from django.conf.urls import url
from bloodbank.views import (
    BloodCatalogListView,
    BloodCatalogDetailView,
    BloodCatalogCreateView,
    BloodCatalogUpdateView,
)

urlpatterns = [
    url(r'^$', BloodCatalogListView.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/$', BloodCatalogDetailView.as_view(), name="detail"),
    url(r'^create/$', BloodCatalogCreateView.as_view(), name="create"),
    url(r'^update/(?P<pk>\d+)/$', BloodCatalogUpdateView.as_view(), name="update"),
]
