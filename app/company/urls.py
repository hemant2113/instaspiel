from django.conf.urls import url
from . import views

app_name='company'

urlpatterns = [
	url(r'^company$',views.CompanyApi.as_view()),
	url(r'^company/(?P<company_id>[0-9]+)$',views.CompanyApi.as_view()),
	]