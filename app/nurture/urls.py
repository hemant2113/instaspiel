from django.conf.urls import url
from . import views

app_name='company'

urlpatterns = [
	url(r'^nurture$',views.NurtureApi.as_view()),
	url(r'^nurtureurl/list/(?P<nurture_id>[0-9]+)$',views.UrlByNurture.as_view()),
	url(r'^nurture/list/(?P<company_id>[0-9]+)$',views.NurtureDataByCompanyId.as_view()),
	url(r'^nurture/(?P<nurture_id>[0-9]+)$',views.NurtureApi.as_view()),
	url(r'^nurture/url/(?P<nurtureurl_id>[0-9]+)$',views.NurtureUrlApi.as_view()),
	url(r'^nurture/url$',views.NurtureUrlApi.as_view()),
]